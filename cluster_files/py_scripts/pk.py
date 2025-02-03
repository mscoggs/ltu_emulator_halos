import numpy as np
import yt
import sys
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
threads = 10
ptypes = [1]
REAL = False
RSD = False
HALOS = True

save_tail = "_HIGHRES"

for count in range(8):

    full_dir = dir_+"sb"+str(count)+"/"

    '''
    print("working on LPT")
    f = full_dir +"ICs/ics"
    pos = readgadget.read_block(f, "POS ", ptypes)/1e3
    delta = np.zeros((grid,grid,grid), dtype=dtype)
    MASL.MA(pos, delta, BoxSize, MAS, verbose=verbose)
    del pos
    delta = delta/np.mean(delta, dtype=dtype)
    delta -= 1.0
    Pk = PKL.Pk(delta, BoxSize, axis, MAS, threads, verbose)
    k0 = Pk.k3D
    Pk00 = Pk.Pk[:,0]

    print("working on test")
    f = full_dir +"pos_out.npy"
    pos = np.load(f).astype(dtype)
    print(np.shape(pos))
    f = full_dir +"vel_out.npy"
    vel = np.load(f).astype(dtype)
    print(np.shape(vel))
    print("printing mean of abs, std")
    print(np.mean(np.abs(vel)))
    print(np.std((vel)))
    vel = np.ascontiguousarray((vel).reshape(3,Np).T)
    print("printing mean of abs, std")
    print(np.mean(np.abs(vel)))
    print(np.std((vel)))

    f = full_dir+"snapdir_004/snap_004"
    ptype = [1]
    vel = readgadget.read_block(f, "VEL ", ptype)
    print("printing mean of abs, std")
    print(np.mean(np.abs(vel)))
    print(np.std((vel)))
    print("END LOOP \n\n\n")


    continue

    '''


    if(REAL or RSD): 
        f = full_dir +"pos_out.npy"
        pos = np.load(f).astype(dtype)
        print(np.shape(pos))
        pos = (pos).reshape(3,Np).T
    
    if(REAL):
        print("working on Emu real")
        delta = np.zeros((grid,grid,grid), dtype=dtype)
        MASL.MA(pos, delta, BoxSize, MAS, verbose=verbose)
        delta = delta/np.mean(delta, dtype=dtype)
        delta -= 1.0
        Pk = PKL.Pk(delta, BoxSize, axis, MAS, threads, verbose)
        k0 = Pk.k3D
        Pk0 = Pk.Pk[:,0] #mono
        Pk2 = Pk.Pk[:,2] #quad
        df = pd.DataFrame({'k': k0, 'Pk0': Pk0, 'Pk2': Pk2})
        df.to_csv("data/Pk_emu_real_"+str(count)+save_tail)



    if(RSD):
        print("working on Emu redshift space")
        print(pos.data.contiguous)
        print(pos.data.c_contiguous)
        f = full_dir +"vel_out2.npy"
        vel = np.load(f).astype(dtype)
        print(np.shape(vel))
        vel = vel.reshape(3,Np).T
        print(vel.data.contiguous)
        print(vel.data.c_contiguous)
        vel = np.ascontiguousarray(vel)
        pos = np.ascontiguousarray(pos)
        redshift = 0.0
        Hubble = 100.0
        RSL.pos_redshift_space(pos, vel, BoxSize, Hubble, redshift, axis)
        del vel
        delta = np.zeros((grid,grid,grid), dtype=dtype)
        MASL.MA(pos, delta, BoxSize, MAS, verbose=verbose)
        delta = delta/np.mean(delta, dtype=dtype)
        delta -= 1.0
        Pk = PKL.Pk(delta, BoxSize, axis, MAS, threads, verbose)
        k0 = Pk.k3D
        Pk0 = Pk.Pk[:,0] #mono
        Pk2 = Pk.Pk[:,2] #quad
        df = pd.DataFrame({'k': k0, 'Pk0': Pk0, 'Pk2': Pk2})
        df.to_csv("data/Pk_emu_rsd_"+str(count)+save_tail)


    if(HALOS):

        print("working on Emu halos")
        delta = np.zeros((grid,grid,grid), dtype=dtype)
        ds = yt.load(full_dir + "rockstar_halos/halos_0.0.bin").all_data()
        pos = np.float32(np.array(ds["all", "particle_position"].to("Mpc/h")))
        mass = np.float32(np.array(ds["all", "particle_mass"].to("Msun/h")))
        #filt_ = np.where(mass >= 1e13)
        #filt_ = np.where(mass >= 1e13)
        #print(np.size(mass[filt_]))
        #print("^thats the total above 1e13")
        #filt_ = np.argsort(mass)[-1000000:]
        filt_ = np.argsort(mass)[-500000:]

        pos = pos[filt_]
        mass = mass[filt_]
        print(np.min(mass)/1e13)
        w = np.power(mass/1e14, 0.7)
        del ds
        MASL.MA(pos, delta, BoxSize, "NGP", verbose=verbose, W=w)
        delta = delta/np.mean(delta, dtype=dtype)
        delta -= 1.0
        Pk = PKL.Pk(delta, BoxSize, axis, MAS, threads, verbose)
        k0 = Pk.k3D
        Pk0 = Pk.Pk[:,0] #mono
        Pk2 = Pk.Pk[:,2] #quad
        df = pd.DataFrame({'k': k0, 'Pk0': Pk0, 'Pk2': Pk2})
        df.to_csv("data/Pk_emu_halos_"+str(count)+save_tail)
        del pos
        del mass





    f = full_dir+"snapdir_004/snap_004"
    if(REAL):
        print("working on Nbod real")
        do_RSD = False
        delta = MASL.density_field_gadget(f, ptypes, grid, MAS, do_RSD, axis, verbose)
        delta = delta/np.mean(delta, dtype=dtype)
        delta -= 1.0
        Pk = PKL.Pk(delta, BoxSize, axis, MAS, threads, verbose)
        k0 = Pk.k3D
        Pk0 = Pk.Pk[:,0] #mono
        Pk2 = Pk.Pk[:,2] #quad
        df = pd.DataFrame({'k': k0, 'Pk0': Pk0, 'Pk2': Pk2})
        df.to_csv("data/Pk_nbod_real_"+str(count)+save_tail)


    if(RSD):
        print("working on Nbod rsd")
        do_RSD = True
        delta = MASL.density_field_gadget(f, ptypes, grid, MAS, do_RSD, axis, verbose)
        delta = delta/np.mean(delta, dtype=dtype)
        delta -= 1.0
        Pk = PKL.Pk(delta, BoxSize, axis, MAS, threads, verbose)
        k0 = Pk.k3D
        Pk0 = Pk.Pk[:,0] #mono
        Pk2 = Pk.Pk[:,2] #quad
        df = pd.DataFrame({'k': k0, 'Pk0': Pk0, 'Pk2': Pk2})
        df.to_csv("data/Pk_nbod_rsd_"+str(count) +save_tail)


    if(HALOS):

        print("working on nbod halos")
        delta = np.zeros((grid,grid,grid), dtype=dtype)
        ds = yt.load(full_dir + "rockstar_halos_gadget/halos_0.0.bin").all_data()
        pos = np.float32(np.array(ds["all", "particle_position"].to("Mpc/h")))

        mass = np.float32(np.array(ds["all", "particle_mass"].to("Msun/h")))

        filt_ = np.where(mass >= 1e13)
        print(np.size(filt_))
        #filt_ = np.argsort(mass)[-1000000:]
        filt_ = np.argsort(mass)[-500000:]
        pos = pos[filt_]
        mass = mass[filt_]
        w = np.power(mass/1e14, 0.7)
        del ds
        MASL.MA(pos, delta, BoxSize, "NGP", verbose=verbose, W=w)
        delta = delta/np.mean(delta, dtype=dtype)
        delta -= 1.0
        Pk = PKL.Pk(delta, BoxSize, axis, MAS, threads, verbose)
        k0 = Pk.k3D
        Pk0 = Pk.Pk[:,0] #mono
        Pk2 = Pk.Pk[:,2] #quad
        df = pd.DataFrame({'k': k0, 'Pk0': Pk0, 'Pk2': Pk2})
        df.to_csv("data/Pk_nbod_halos_"+str(count)+save_tail)
        del pos
