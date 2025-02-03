import numpy as np
import pandas as pd
import os
import sys

L = 3000.0
N = 1536
num = int(sys.argv[-1])
input_dir = "/scratch/08288/tg875874/ltu_gobig/sb"+str(num)+"/"


'''
print("reading")
pos = np.load(input_dir+"dis_out.npy").reshape(3, N**3)
pos = [pos[1], pos[0], pos[2]]

print("making g")
dx = L/N
g = np.linspace(0.0, L-dx, N, dtype=np.float32)
g = np.vstack(list(map(np.ravel,np.meshgrid(g,g,g))))
#g = np.array([g[1],g[0], g[2]])
#g = g.reshape(3,N,N,N)

pos = np.float32(pos+g)

del g

print("correcting bounds")
pos[np.where(pos>L)] -= L
pos[np.where(pos<0.0)] += L
#np.save(input_dir+"pos_out.npy", pos)
print("saving")
np.save(input_dir+"pos_out.npy", pos)

'''
vel = np.load(input_dir+"vel_out.npy").reshape(3, N**3)
vel = [vel[1], vel[0], vel[2]]
print("saving")
np.save(input_dir+"vel_out2.npy", vel)

