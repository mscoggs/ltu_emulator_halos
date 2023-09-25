import numpy as np
import math
import sys
import matplotlib.pyplot as plt
import nbodykit
from nbodykit.lab import *
from nbodykit import setup_logging, style
from nbodykit.source.catalog import ArrayCatalog
COSMO = "0000"

LL =0.19
pos_particle_nbody = np.load("LtU-selected/pos_emu.npy")
vel_particle_nbody = np.load("LtU-selected/vel_emu.npy")
vel_particle_nbody = np.reshape(vel_particle_nbody,(3,512**3)).T
pos_particle_nbody = np.reshape(pos_particle_nbody,(3,512**3)).T
if("0000" in COSMO): 
    mass_per_particle = 6.565293600596489e11 #msun/h
    cosmo = cosmology.Planck15
elif("0001" in COSMO): 
    mass_per_particle = 4.423043468244375e11
    cosmo = cosmology.Planck15
    cosmo = cosmo.clone(h=0.8599, Omega0_b = 0.05557, Omega0_cdm =0.15833)  
else: print("COSMO ERROR")


mass = np.linspace(mass_per_particle, mass_per_particle, len(pos_particle_nbody))


f = ArrayCatalog({'Position' : pos_particle_nbody,'Velocity' : vel_particle_nbody, 'Mass' : mass }, BoxSize=[1000,1000,1000])



fof_output = nbodykit.algorithms.fof.FOF(f, LL, 20, )
z = 0
halos=fof_output.to_halos(particle_mass=mass_per_particle, cosmo=cosmo, redshift=z)
halos.save("fof_halos/lh0000_emu_ll19")
