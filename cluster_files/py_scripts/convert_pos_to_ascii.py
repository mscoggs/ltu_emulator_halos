import numpy as np
import pandas as pd
import os
import sys

L = 3000.0
N = 1536
X_DIM = 4
TOTAL_BLOCKS=X_DIM**3

args = sys.argv
num = int(args[1])
OMEGA_M, h = float(args[2]), float(args[4])
print(OMEGA_M, h)

input_dir ="/scratch/08288/tg875874/ltu_gobig/sb"+str(num)+"/"


print("reading in pos and vel")
pos = np.float32(np.reshape(np.load(input_dir+"pos_out.npy"),(3,N**3)))
vel = np.float32(np.reshape(np.load(input_dir+"vel_out2.npy"),(3,N**3)))


print("making other arrays")
RHO_CRIT = 2.77536627e11*h*h #Msun/MPC^3
vol_box = np.power(L/h,3) #Mpc^3
total_mass = OMEGA_M * RHO_CRIT * vol_box
mass_per_particle = np.float32(total_mass / np.power(N,3))
print("MASS PER",mass_per_particle)
vmag = np.float32(np.sqrt(np.sum(np.power(vel.T,2),axis=1)))
energy = 0.5*vmag
mp = mass_per_particle*h
###NEED TO USE MSUN/H, SO MULTIPLY h on the line above and it should be ok
mass = np.float32(np.linspace(mp,mp,len(vmag)))
id_ = np.linspace(1,len(vmag), len(vmag)).astype(int)
type_ = np.linspace(0,0,len(vmag)).astype(int)



block_size = N**3/TOTAL_BLOCKS
for block in range(TOTAL_BLOCKS):
    print("working on block", block)
    a,b = int(block_size*block), int(block_size*(block+1))
    print(a,b)

    sub_df = pd.DataFrame((np.array((pos[0][a:b],pos[1][a:b],pos[2][a:b],vel[0][a:b],vel[1][a:b],vel[2][a:b],mass[a:b], energy[a:b],id_[a:b],type_[a:b]), dtype=np.float32).T),columns=["X", "Y", "Z", "VX", "VY", "VZ", "Mass", "Energy", "ID", "Type"])
    
    #if(chunk == 0): sub_df.to_csv(input_dir+"rockstar_ascii", sep=' ', index=False)
    #else: sub_df.to_csv(input_dir+"rockstar_ascii", sep=' ', mode='a', index=False, header=False)
    sub_df.to_csv(input_dir+"rockstar_in."+str(block)+".0.ascii", sep=' ', index=False, header=False)
