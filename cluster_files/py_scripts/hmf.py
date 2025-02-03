import yt
import pandas as pd
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

CMAP = plt.cm.jet

def get_raw_hmf(masses):
    log_mass = np.log10(masses)
    min_mass = 13
    filt = np.where(log_mass >= min_mass)
    log_mass = log_mass[filt]
    mass = masses[filt]
    bins = np.logspace(min_mass, 16, 100)

    N = []
    for x in range(np.size(bins)):
        lo = bins[x]
        N.append(np.size(np.where((mass >= lo))[0]))
    N = np.array(N)
    return bins,N

def get_hmf(masses):
    log_mass = np.log10(masses)
    min_mass = 13
    filt = np.where(log_mass >= min_mass)
    log_mass = log_mass[filt]
    mass = masses[filt]
    bins = np.logspace(min_mass, 16, 100)
    dlogm = np.log10(bins[1]) - np.log10(bins[0])
    N = []
    for x in range(np.size(bins)-1):
        lo,up = bins[x], bins[x+1]
        N.append(np.size(np.where((mass >= lo) & (mass < up))[0]))
    N = np.array(N)
    dn = -1*(N[1:]-N[:-1])
    dndlnm = dn/(dlogm*1e9)
    return bins[1:-1], dndlnm

def get_cmf(masses):
    log_mass = np.log10(masses)
    min_mass = 13
    filt = np.where(log_mass >= min_mass)
    log_mass = log_mass[filt]
    mass = masses[filt]
    bins = np.logspace(min_mass, 16, 100)
    dlogm = 1
    N = []
    for x in range(np.size(bins)-1):
        lo,up = bins[x], bins[x+1]
        N.append(np.size(np.where(mass >= lo)[0]))
    hmf = np.array(N)/dlogm
    return bins[:-1], hmf


def get_color(om):
    om_max = 0.5
    om_min = 0.1
    return CMAP((om-om_min)/(om_max-om_min))

def get_mp(count):
    dir_ = "sb"+str(count)
    param_file = open(dir_+"/2LPT.param")
    for line in param_file:
        if("Omega " in line): OMEGAM = float(line.split()[-1])
        if("OmegaLambda" in line): OMEGAL = float(line.split()[-1])
        if("HubbleParam" in line): H = float(line.split()[-1])
        if("Sigma8" in line): S8 = float(line.split()[-1])
    RHO_CRIT = 2.77536627e11*H*H #Msun/MPC^3
    L = 3000.0
    N = 1536
    vol_box = np.power(L/H,3) #Mpc^3
    total_mass = OMEGAM * RHO_CRIT * vol_box
    mass_per_particle = np.float32(total_mass / np.power(N,3))*H
    return mass_per_particle

def get_om(dir_num):
    om = 0
    file = open("sb"+str(dir_num)+"/2LPT.param", "r")
    for line in file:
        line = line.strip()
        if("Omega " in line): om = float(line.split()[1])
    file.close()
    return om

halo_dir = "rockstar_halos"
fig_type = str(sys.argv[1])

fig,axs = plt.subplots(2, gridspec_kw={"height_ratios": [3,1]},figsize=(10,10), sharex=True)
axs[0].set_yscale("log")
axs[0].set_xscale("log")
axs[1].set_xscale("log")

if(fig_type == "cmf"):
    axs[0].set_ylabel(r"$N$ ($> M_{\rm halo}$)")
    axs[1].set_ylabel(r"$\Delta N/N_{\rm true}$")
elif(fig_type == "hmf"):
    axs[0].set_ylabel(r"$dn/d$log$_{10}M$ [Mpc$^{-3}$]")
    axs[1].set_ylabel(r"$\Delta n/n_{\rm true}$")

axs[1].set_xlabel(r"$M_{\rm halo}$ $[M_\odot]$")
axs[1].set_ylim(-1.0,1.0)






#for dir_num in [0]:
for dir_num in range(8):
    #mp = get_mp(dir_num)

    dir_ = "/scratch/08288/tg875874/ltu_gobig/sb"+str(dir_num)+"/"
    print("working on ", dir_)

    om = get_om(dir_num)

    dsN = yt.load(dir_+ halo_dir+"_gadget/halos_0.0.bin")
    adN = dsN.all_data()
    massN = np.array(adN["all","particle_mass"].to("Msun/h"))
    dsE = yt.load(dir_+ halo_dir+"/halos_0.0.bin")
    adE = dsE.all_data()
    massE = np.array(adE["all","particle_mass"].to("Msun/h"))

    print(np.size(np.where(massN > 1e13)))

    del dsN
    del adN
    del dsE
    del adE
    
    '''

    ### TEST
    for target in [1e13,1e14,1e15]:
        massN = massN[np.where(massN > target)]
        massE = massE[np.where(massE > target)]
        NN = np.size(massN)
        NE = np.size(massE)
        print(target/1e13)
        print(np.abs(NN-NE)/NN)

    print("5 most massive from nbod:", np.sort(massN)[-5:]/1e15)
    print("5 most massive from emu:", np.sort(massE)[-5:]/1e15)
    mass_cut = mp*120
    print("this is mass cut /1e14", mass_cut/1e14)

    print(np.max(massN))
    print(np.size(np.where(massN > mass_cut)[0]))
    massN = massN[np.where(massN > mass_cut)]
    print("this is the total number of haloes above mass cut", np.size(massN))
    '''
    if(fig_type == "raw"):
        binsN, numN = get_raw_hmf(massN)
        binsE, numE = get_raw_hmf(massE)
        df = pd.DataFrame({'binsE': binsE, 'binsN': binsN, "numN": numN, "numE": numE})
        df.to_csv("data/hmf_"+str(dir_num))
    else:


        if(fig_type == "cmf"):
            binsN, hmfN = get_cmf(massN)
            binsE, hmfE = get_cmf(massE)
        elif(fig_type == "hmf"):
            binsN, hmfN = get_hmf(massN)
            binsE, hmfE = get_hmf(massE)
        col = get_color(om)

        

        
        axs[0].plot(binsN, hmfN, color=col)
        axs[0].scatter(binsN, hmfE, color=col, marker="s", s=10)
        filt = np.where(hmfN > 0)
        axs[1].plot(binsN[filt], (hmfE[filt]-hmfN[filt])/hmfN[filt], color=col)


if(fig_type != "raw"):
    plt.subplots_adjust(hspace=0)
    c=axs[1].scatter([binsN[0], binsN[1]], [hmfN[0], hmfN[1]], c=[0.1,0.5], cmap=CMAP, s=0)
    plt.colorbar(c,ax=axs.ravel().tolist(), label=r"$\Omega_m$")
    plt.savefig("figures/"+str(fig_type)+".pdf", bbox_inches="tight")
