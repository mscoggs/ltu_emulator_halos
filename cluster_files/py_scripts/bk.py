import numpy as np
import sys
import yt
import Pk_library as PKL
import MAS_library as MASL
import matplotlib.pyplot as plt
import readgadget
import pandas as pd
import redshift_space_library as RSL

from matplotlib import colors
CMAP = plt.cm.jet




def get_color(om):
    om_max = 0.5
    om_min = 0.1
    return CMAP((om-om_min)/(om_max-om_min))

dir_ = "/scratch/08288/tg875874/ltu_gobig/"
N=1536
dtype = np.float32

Np = N**3
grid  = 512*3
BoxSize = 3000.0
MAS     = "CIC"
verbose = True
axis = 0
threads = 20
ptypes = [1]
k1 = 0.1
k2 = 1.0
#theta = np.linspace(0,np.pi, 25)
theta = np.linspace(0,np.pi, 15)
k_list =  np.linspace(0.05,0.95, 10)
theta_single = np.array([np.pi/3.0])

THETA=False
SQUEEZE = False
HALOS = True

if(SQUEEZE):
    N=15
    k2 = np.linspace(1.0,1.0,N)*0.5
    k3 = k2
    ratios = np.logspace(-2.0,0.0,N)
    k1 = ratios*k2
    s = 1-k1/(2.0*k2)
    thetas = np.arccos(k1/(2*k2))

save_tail = ""



#squeeze params



for count in range(8):

    full_dir = dir_+"sb"+str(count)+"/"

    print("working on Emu Bk vs theta")

    if(not HALOS):
        f = full_dir +"pos_out.npy"
        pos = np.load(f).astype(dtype)
        pos = (pos).reshape(3,Np).T
        delta = np.zeros((grid,grid,grid), dtype=dtype)
        MASL.MA(pos, delta, BoxSize, MAS, verbose=verbose)
    else:
        ds = yt.load(full_dir + "rockstar_halos/halos_0.0.bin").all_data()
        pos = np.float32(np.array(ds["all", "particle_position"].to("Mpc/h")))
        mass = np.float32(np.array(ds["all", "particle_mass"].to("Msun/h")))
        #filt_ = np.where(mass>=1e13)
        filt_ = np.argsort(mass)[-500000:]
        mass = mass[filt_]
        pos = pos[filt_]
        w = np.power(mass/1e14,0.7)
        delta = np.zeros((grid,grid,grid), dtype=dtype)
        MASL.MA(pos, delta, BoxSize, "NGP", verbose=verbose, W=w)

    print("first_delta", np.mean(delta))
    delta = delta/np.mean(delta, dtype=dtype)
    delta -= 1.0


    if(THETA):
        BBk = PKL.Bk(delta, BoxSize, k1,k2,theta, MAS, threads)
        k0 = BBk.k
        Bk = BBk.B
        Qk = BBk.Q
        df = pd.DataFrame({'theta': theta, 'Qk': Qk, 'Bk': Bk})
        df.to_csv("data/Bk_emu_theta_"+str(count)+save_tail)

    elif(HALOS):

        BBk = PKL.Bk(delta, BoxSize, k1,k2,theta, MAS, threads)
        k0 = BBk.k
        Bk = BBk.B
        Qk = BBk.Q
        df = pd.DataFrame({'theta': theta, 'Qk': Qk, 'Bk': Bk})
        df.to_csv("data/Bk_emu_halos_"+str(count)+save_tail)

    elif(SQUEEZE):

        B_list, Q_list = [],[]
        for i in range(N):
            #if(i<13): continue
            print("working on step", i," out of", N)
            print("k1, k2, theta", k1[i],k2[i],np.array([thetas[i]]))

            BBk = PKL.Bk(delta, BoxSize, k1[i],k2[i],np.array([thetas[i]]), MAS, threads)
            B_list.append(BBk.B[0])
            Q_list.append(BBk.Q[0])

        B_list = np.array(B_list)
        Q_list = np.array(Q_list)
        df = pd.DataFrame({'thetas': thetas, "k1": k1, "k2": k2, "Qk": Q_list, "Bk": B_list})
        df.to_csv("data/Bk_emu_squeeze_"+str(count)+save_tail)


    else:
        print("WORKING ON EQUI")
        b_list, q_list = [],[]
        for kv in k_list:
            k1 = kv
            k2 = kv
            BBk = PKL.Bk(delta, BoxSize, k1,k2,theta_single, MAS, threads)
            b_list.append(BBk.B[0])
            q_list.append(BBk.Q[0])
            print(b_list,q_list)
        b_list = np.array(b_list)
        q_list = np.array(q_list)
        df = pd.DataFrame({'k': k_list, 'Qk': q_list, 'Bk': b_list})
        df.to_csv("data/Bk_emu_k_"+str(count)+save_tail)



    del pos


    
    print("working on Nbod")
    if(not HALOS):
        f = full_dir+"snapdir_004/snap_004"
        do_RSD = False
        delta = MASL.density_field_gadget(f, ptypes, grid, MAS, do_RSD, axis, verbose)
        delta = delta/np.mean(delta, dtype=dtype)
        delta -= 1.0
    else:
        ds = yt.load(full_dir + "rockstar_halos_gadget/halos_0.0.bin").all_data()
        pos = np.float32(np.array(ds["all", "particle_position"].to("Mpc/h")))
        mass = np.float32(np.array(ds["all", "particle_mass"].to("Msun/h")))
        #filt_ = np.where(mass>=1e13)
        filt_ = np.argsort(mass)[-500000:]
        mass = mass[filt_]
        pos = pos[filt_]
        w = np.power(mass/1e14,0.7)
        delta = np.zeros((grid,grid,grid), dtype=dtype)
        MASL.MA(pos, delta, BoxSize, "NGP", verbose=verbose, W=w)

    print("first_delta", np.mean(delta))
    delta = delta/np.mean(delta, dtype=dtype)
    delta -= 1.0

    if(THETA):
        BBk = PKL.Bk(delta, BoxSize, k1,k2,theta, MAS, threads)
        k0 = BBk.k
        Bk = BBk.B
        Qk = BBk.Q
        df = pd.DataFrame({'theta': theta, 'Qk': Qk, 'Bk': Bk})
        df.to_csv("data/Bk_nbod_theta_"+str(count)+save_tail)

    elif(HALOS):
        BBk = PKL.Bk(delta, BoxSize, k1,k2,theta, MAS, threads)
        k0 = BBk.k
        Bk = BBk.B
        Qk = BBk.Q
        df = pd.DataFrame({'theta': theta, 'Qk': Qk, 'Bk': Bk})
        df.to_csv("data/Bk_nbod_halos_"+str(count)+save_tail)


    elif(SQUEEZE):

        B_list, Q_list = [],[]
        for i in range(N):
            print("working on step", i," out of", N)
            BBk = PKL.Bk(delta, BoxSize, k1[i],k2[i],np.array([thetas[i]]), MAS, threads)
            B_list.append(BBk.B[0])
            Q_list.append(BBk.Q[0])

        B_list = np.array(B_list)
        Q_list = np.array(Q_list)
        df = pd.DataFrame({'thetas': thetas, "k1": k1, "k2": k2, "Qk": Q_list, "Bk": B_list})
        df.to_csv("data/Bk_nbod_squeeze_"+str(count)+save_tail)

    else:

        b_list, q_list = [],[]
        
        for kv in k_list:
            k1 = kv
            k2 = kv
            print(k1,k2,theta_single)
            print("this is delta")
            print(delta)
            BBk = PKL.Bk(delta, BoxSize, k1,k2,theta_single, MAS, threads)
            b_list.append(BBk.B[0])
            q_list.append(BBk.Q[0])
        b_list = np.array(b_list)
        q_list = np.array(q_list)
        df = pd.DataFrame({'k': k_list, 'Qk': q_list, 'Bk': b_list})
        df.to_csv("data/Bk_nbod_k_"+str(count)+save_tail)


