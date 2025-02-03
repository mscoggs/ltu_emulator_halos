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
k_list =  np.linspace(0.05,0.95, 10)
theta_single = np.array([np.pi/3.0])




count = int(sys.argv[-1])
type_ =str(sys.argv[-2])

print("COUNT AND TYPE")
print(count, type_)

full_dir = dir_+"sb"+str(count)+"/"


if(type_ == "emu"):
    f = full_dir +"pos_out.npy"
    pos = np.load(f).astype(dtype)
    pos = (pos).reshape(3,Np).T
    delta = np.zeros((grid,grid,grid), dtype=dtype)
    MASL.MA(pos, delta, BoxSize, MAS, verbose=verbose)

elif(type_ == "nbod"):
    f = full_dir+"snapdir_004/snap_004"
    do_RSD = False
    delta = MASL.density_field_gadget(f, ptypes, grid, MAS, do_RSD, axis, verbose)

delta = delta/np.mean(delta, dtype=dtype)
delta -= 1.0
b_list, q_list = [],[]
for kv in k_list:
    k1 = kv
    k2 = kv
    print(k1,k2,theta_single)
    BBk = PKL.Bk(delta, BoxSize, k1,k2,theta_single, MAS, threads)
    b_list.append(BBk.B[0])
    q_list.append(BBk.Q[0])
b_list = np.array(b_list)
q_list = np.array(q_list)
df = pd.DataFrame({'k': k_list, 'Qk': q_list, 'Bk': b_list})
df.to_csv("data/Bk_"+str(type_)+"_k_"+str(count))


