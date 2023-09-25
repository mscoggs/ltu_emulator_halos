import numpy as np
import math
import sys
import matplotlib.pyplot as plt
import yt
import glob
import pandas as pd
from matplotlib import colors
from scipy import stats
CMAP = plt.cm.coolwarm
from scipy.optimize import curve_fit
from matplotlib import colors
from scipy import stats
from scipy.interpolate import UnivariateSpline
from scipy.interpolate import InterpolatedUnivariateSpline

#nbodykit-env imports

import nbodykit
from nbodykit.lab import *
from nbodykit import setup_logging, style
from nbodykit.source.catalog import ArrayCatalog
import bigfile
from nbodykit.source.catalog import BigFileCatalog
from pathlib import Path
from summarizer.data import Catalogue
from summarizer.two_point import TwoPCF 
from summarizer.two_point import Pk 
from summarizer.vpf import VPF 
from summarizer.cic import CiC 

import nbodykit.lab as nblab
from nbodykit.hod import Zheng07Model
from nbodykit import cosmology



def read_sim_params(lh_num, arg_names):
    df = pd.read_csv("../../../LH_data/"+str(lh_num)+"_sim_params_full")
    params=[]
    for arg in arg_names: params.append(list(df[arg])[0])
    return params
    

def run_FOF(lh_num, sim_str):
    base = "../../../LH_data/"+str(lh_num)+"_"+sim_str
    pos_file = base+"_pos.npy"
    vel_file = base+"_vel.npy"
    pos = np.reshape(np.load(pos_file),(3,512**3)).T
    vel = np.reshape(np.load(vel_file),(3,512**3)).T

    LL=0.2
    params = read_sim_params(lh_num, ["h", "omega_m","omega_b", "n_s","mass_per_p"])
    h,Om,Ob, n_s,mass_per_particle = params
    cosmo = cosmology.Planck15
    cosmo = cosmo.clone(h=h, Omega0_b = Ob, Omega0_cdm =Om-Ob, n_s=n_s)  
    mass = np.linspace(mass_per_particle, mass_per_particle, len(pos))

    f = ArrayCatalog({'Position' : pos,'Velocity' : vel, 'Mass' : mass }, BoxSize=[1000,1000,1000])
    nmin = 20#min(20,int(20*5e11/mass_per_particle)-1)
    print("Working on ", pos_file)
    print("Nmin =", nmin)
    print("Mass per particle =", mass_per_particle)



    fof_output = nbodykit.algorithms.fof.FOF(f, LL, nmin)
    halos=fof_output.to_halos(particle_mass=mass_per_particle, cosmo=cosmo, redshift=0)
    halos.save(base+"_fof_halos")

    particle_halo_ids = np.array(fof_output.labels)
    np.save(base+"_hid.npy", particle_halo_ids)
    

lh_nums = ['502','1702', '1026', '1122', '324', '944', '1951', '485', '1582', '592', '1323', '401', '406', '1608', '391', '1710', '444', '1696', '926', '694', '1515'] 
for lh_num in lh_nums:
    run_FOF(lh_num, "nbody")    
    run_FOF(lh_num, "emu")
