import numpy as np
import math
import sys
import matplotlib.pyplot as plt
import yt
import glob
import shutil
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
from summarizer import WST

LH_NUMS = [ '324','1702','1026', '1951','1122', '944', '485', '1582', '592', '1323', '401', '406', '1608','391', '1710', '444', '1696', '926','694', '1515', '502'] 


def read_sim_params(lh_num, arg_names= ["h", "omega_m","omega_b", "n_s","mass_per_p","sigma_8"]):
    df = pd.read_csv("../../../LH_data/"+str(lh_num)+"_sim_params_full")
    params=[]
    for arg in arg_names: params.append(list(df[arg])[0])
    return params

def get_cosmo(lh_num):
    params = read_sim_params(lh_num, arg_names=["h", "omega_m","omega_b", "n_s","mass_per_p"])
    h,Om,Ob, n_s,mass_per_particle = params
    cosmo = cosmology.Planck15
    cosmo = cosmo.clone(h=h, Omega0_b = Ob, Omega0_cdm =Om-Ob, n_s=n_s)  
    return cosmo, mass_per_particle

def read_halos(lh_num):
    
    fnbody = BigFileCatalog('../../../LH_data/'+str(lh_num)+"_nbody_fof_halos")
    femu = BigFileCatalog('../../../LH_data/'+str(lh_num)+"_emu_fof_halos")
    mn  = np.array(fnbody["Mass"])
    me  = np.array(femu["Mass"])
    vn  = np.array(fnbody["Velocity"])
    ve  = np.array(femu["Velocity"])            
    pn  = np.array(fnbody["Position"])
    pe  = np.array(femu["Position"]) 
    return mn,me,vn,ve,pn,pe
    
    

lh_num = LH_NUMS[:1][0]
mn,me,vn,ve,pn,pe = read_halos(lh_num)
cosmo = get_cosmo(lh_num)

cat1 = Catalogue(pn, vn, 0,1000,cosmo,"name", mass=mn)
cat2 = Catalogue(pe, ve, 0,1000,cosmo,"name", mass=me)


print("Wavelet time")
print("loading WST")
wst_runner = WST(J_3d = 1, L_3d = 1, n_mesh=360)

print("running wst")
wst = wst_runner(catalogue=cat1)
print("sending to ds")
wst = wst_runner.to_dataset(wst)
print(wst)
