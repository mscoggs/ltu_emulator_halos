import numpy as np
import pandas as pd

for name in ["nbody", "emu"]
  pos = np.load("LtU-selected/pos_"+name+".npy")
  vel = np.load("LtU-selected/vel_nbody.npy")
  vel = np.reshape(vel,(3,512**3))
  pos = np.reshape(pos,(3,512**3))
  OMEGA_M, OMEGA_B, h = 0.3175, 0.049, 0.6711
  RHO_CRIT = 2.77536627e11*h*h #Msun/MPC^3
  vol_box = np.power(1000/h,3) #Mpc^3
  total_mass = OMEGA_M * RHO_CRIT * vol_box
  mass_per_particle = total_mass / np.power(512,3)
  vmag = np.sqrt(np.sum(np.power(vel.T,2),axis=1))
  energy = 0.5*vmag
  mp = mass_per_particle
  mass = np.linspace(mp,mp,len(vmag))
  id_ = np.linspace(1,len(vmag), len(vmag)).astype(int)
  type_ = np.linspace(1,1,len(vmag))
  data = np.array((pos[0],pos[1],pos[2],vel[0],vel[1],vel[2],mass, energy,id_,type_))
  df = pd.DataFrame(data.T,columns=["X", "Y", "Z", "VX", "VY", "VZ", "Mass", "Energy", "ID", "Type"])

  df.to_csv(name, sep=' ')
