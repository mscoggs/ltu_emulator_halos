import numpy as np
import math
import sys
import matplotlib.pyplot as plt
# from matplotlib import cm
# from matplotlib.lines import Line2D
# import glob
import yt
# #from yt.units import kpc
# #import ytree/
# from astropy import units as u
# import matplotlib.cm as cm

CMAP = plt.cm.coolwarm


dir_ = "rockstar_comparisons/test_default_"  
dsnbod = yt.load(dir_+"nbody/halos_0.0.bin")
dsemu = yt.load(dir_+"emu/halos_0.0.bin")
pos_nbod = dsnbod.all_data()["all","particle_position"].to("Mpc/h")
mass_nbod  = dsnbod.all_data()["all","particle_mass"].to("Msun/h")
rad_nbod  = dsnbod.all_data()["all","virial_radius"].to("Mpc/h")
pos_emu = dsemu.all_data()["all","particle_position"].to("Mpc/h")
mass_emu  = dsemu.all_data()["all","particle_mass"].to("Msun/h")
rad_emu  = dsemu.all_data()["all","virial_radius"].to("Mpc/h")

# filter_mass1 = np.where(mass_nbod >= 1e13)
# filter_mass2 = np.where(mass_emu >= 1e13)
# pos_nbod = pos_nbod[filter_mass1]
# mass_nbod = mass_nbod[filter_mass1]
# rad_nbod = rad_nbod[filter_mass1]
# pos_emu = pos_emu[filter_mass2]
# mass_emu = mass_emu[filter_mass2]
# rad_emu = rad_emu[filter_mass2]



OMEGA_B = 0.0486 
OMEGA_M = 0.307
OMEGA_L = 1-OMEGA_M
SIGMA_8 = 0.8159
delta_c = 1.686
h=0.677
rho_crit = 1.5*1e11 #Msol/mpc^3
T_HUBBLE = 4.55e17 #s
MPC_TO_CM = 3.086e+24

K = 1.380649e-16 #ergs/K
SEC_PER_MYR = 3.15576e+13
m_p = 1.6e-27
msol = 2e30
mpc = 3.086e+24
n = rho_crit*msol/mpc**3*OMEGA_B/m_p #cm^-3



def r_vir(m_h,z):
    #returns mpc
    h=0.7
    
    OMEGA_K = 1-OMEGA_M-OMEGA_L
    OMEGA_M_Z=OMEGA_M*np.float_power(1+z,3)/ (OMEGA_M*np.float_power(1+z,3) + OMEGA_L + OMEGA_K*np.float_power(1+z,2))
    d = OMEGA_M_Z-1
    delta_c = 18*np.pi*np.pi + 82*d -39*d*d

    return 1e-3*0.784/h* np.float_power(m_h*h/1e8, 1.0/3)*np.float_power(OMEGA_M/OMEGA_M_Z * (delta_c/(18*np.pi*np.pi)), -1.0/3) * (10/(1+z))




ids_nbod, ids_emu = np.linspace(-1,-1,len(mass_nbod)), np.linspace(-1,-1,len(mass_emu))
bs= 50
bw = bs/2.0
bf=3
l = bw+bf
xc = bw
xsteps, ysteps, zsteps = int(1000/bs),int(1000/bs),int(1000/bs)
N=0
N_emu = 0
emu_args = []
nbod_args = []
sizes=[]

for xstep in range(xsteps):
    yc = bw
    for ystep in range(ysteps):
        zc = bw
        for zstep in range(zsteps):
            c = np.array([xc,yc,zc])
            
            x1,y1,z1 = (pos_nbod.value - c).T
            x2,y2,z2 = (pos_emu.value - c).T
            nb_filt = np.where((-bw<=x1) & (x1<=bw) & (-bw<=y1) & (y1<=bw) & (-bw<=z1) & (z1<=bw))[0]
            em_filt = np.where((-l<=x2) & (x2<=l) & (-l<=y2) & (y2<=l) & (-l<=z2) & (z2<=l))[0]

            pos_nbod1 = pos_nbod[nb_filt]
            rad_nbod1 = rad_nbod[nb_filt]
            ids_nbod1 = ids_nbod[nb_filt]
            pos_emu1 = pos_emu[em_filt]
            rad_emu1 = rad_emu[em_filt]
            ids_emu1 = ids_emu[em_filt]

            for i in range(len(pos_nbod1)):
                pos_target = pos_nbod1[i]
                rad_target = rad_nbod1[i]



                dist = np.sqrt(np.sum(np.power((pos_emu1 - pos_target),2),axis=1))
                size = len(np.where(dist<rad_target)[0])
                if(size>= 2): sizes.append(size)
                pair_ind = np.argmin(dist)

                if(dist[pair_ind] > rad_target): continue
    
                if(ids_emu1[pair_ind] != -1): continue
                ids_emu1[pair_ind] = i+N

                ids_nbod1[i] = i+N
                emu_args.append(ids_emu1[pair_ind])
                nbod_args.append(ids_nbod1[i])

            ids_emu[em_filt] = ids_emu1
            ids_nbod[nb_filt] = ids_nbod1
            
            #print(xc,yc,zc)
            zc += bs
            N+= len(pos_nbod1)
            N_emu += len(pos_emu1)
        yc+=bs
    xc+= bs
    print(xc)
    




N_targets=500
for target_mass in [1e14,5e14]:
    print("working on", target_mass)
    pos_nbod = dsnbod.all_data()["all","particle_position"].to("Mpc/h")
    mass_nbod  = dsnbod.all_data()["all","particle_mass"].to("Msun/h")

    pos_emu = dsemu.all_data()["all","particle_position"].to("Mpc/h")
    mass_emu  = dsemu.all_data()["all","particle_mass"].to("Msun/h")


    #indices_nbod = np.argsort(np.abs(mass_nbod-dsnbod.quan(target_mass, 'Msun/h')))[0:int(N_targets*2)]
    #ids_nbod_stack = ids_nbod[indices_nbod]
    #ids_nbod_stack = ids_nbod_stack[np.where(ids_nbod_stack != -1.0)[0]][0:N_targets].astype(int)
    indices_emu = np.argsort(np.abs(mass_emu-dsnbod.quan(target_mass, 'Msun/h')))[0:int(N_targets*2)]
    ids_emu_stack = ids_emu[indices_emu]
    ids_emu_stack = ids_emu_stack[np.where(ids_emu_stack != -1.0)[0]][0:N_targets].astype(int)
    indices_nbod = [np.where(ids_nbod == id_)[0][0] for id_ in ids_emu_stack]
    indices_emu = [np.where(ids_emu == id_)[0][0] for id_ in ids_emu_stack]

    target_mass_list_nbod =  mass_nbod[indices_nbod]
    target_positions_nbod= pos_nbod[indices_nbod]
    poss_nbod = target_positions_nbod.value


    target_mass_list_emu =  mass_emu[indices_emu]
    target_positions_emu= pos_emu[indices_emu]
    poss_emu = target_positions_emu.value


    pos_particle_nbody = np.load("LtU-selected/pos_nbody.npy")
    vel_particle_nbody = np.load("LtU-selected/vel_nbody.npy")
    vel_particle_nbody = np.reshape(vel_particle_nbody,(3,512**3)).T
    pos_particle_nbody = np.reshape(pos_particle_nbody,(3,512**3)).T

    vmag_nbody = np.sqrt(np.sum(np.power(vel_particle_nbody,2),axis=1))
    px_nbody,py_nbody,pz_nbody = pos_particle_nbody.T


    pos_particle_emu = np.load("LtU-selected/pos_emu.npy")
    vel_particle_emu = np.load("LtU-selected/vel_emu.npy")
    vel_particle_emu = np.reshape(vel_particle_emu,(3,512**3)).T
    pos_particle_emu = np.reshape(pos_particle_emu,(3,512**3)).T

    vmag_emu = np.sqrt(np.sum(np.power(vel_particle_emu,2),axis=1))
    px_emu,py_emu,pz_emu = pos_particle_emu.T





    vmag_emu = np.sqrt(np.sum(np.power(vel_particle_emu,2),axis=1))
    px_emu,py_emu,pz_emu = pos_particle_emu.T

    vmag_nbody = np.sqrt(np.sum(np.power(vel_particle_nbody,2),axis=1))
    px_nbody,py_nbody,pz_nbody = pos_particle_nbody.T




    xl = r_vir(target_mass,0)*1.5
    yl = xl
    zl = xl

    dif_emus = []
    dif_nbodys = []
    vmag_emus, vmag_nbodys = [],[]
    v3d_emus, v3d_nbodys = [],[]

    pos_emu = pos_particle_emu
    vel_emu = vel_particle_emu
    pos_nbody = pos_particle_nbody
    vel_nbody = vel_particle_nbody
    i=0
    for pos in poss_nbod:
        dif_nbody = np.subtract(pos_nbody, pos).T
        dif_nbody_mag = np.abs(dif_nbody)
        yes_nbody = np.where((dif_nbody_mag[0] <= xl/2.0)
                                & (dif_nbody_mag[1] <= yl/2.0)
                                & (dif_nbody_mag[2] <= zl/2.0)
                               )
        dif_nbodys.extend(dif_nbody.T[yes_nbody])
        v3d_nbodys.extend(vel_nbody[yes_nbody])

        vmag_nbodys.extend(vmag_nbody[yes_nbody])

        if(i%10 == 0): print(i/N_targets, "%")
        i+=1
        
    i=0
    for pos in poss_emu:

        dif_emu = np.subtract(pos_emu, pos).T
        dif_emu_mag = np.abs(dif_emu)
        yes_emu = np.where((dif_emu_mag[0] <= xl/2.0)
                                & (dif_emu_mag[1] <= yl/2.0)
                                & (dif_emu_mag[2] <= zl/2.0)
                               )
        dif_emus.extend(dif_emu.T[yes_emu])
        v3d_emus.extend(vel_emu[yes_emu])
        vmag_emus.extend(vmag_emu[yes_emu])

        if(i%10 == 0): print(i/N_targets, "%")
        i+=1
        
        
    dif_emus = np.array(dif_emus)
    dif_nbodys = np.array(dif_nbodys)
    vmag_emus = np.array(vmag_emus)
    vmag_nbodys = np.array(vmag_nbodys)
    v3d_emus = np.array(v3d_emus)
    v3d_nbodys = np.array(v3d_nbodys)


    # dx, dy = 0.05,0.05
    # x0, y0 = -xl/2.0+dx/2.0, -yl/2.0+dx/2.0
    # xsteps = int(xl/dx)
    # ysteps = int(yl/dy)
    xsteps = 51
    ysteps = xsteps
    zsteps = xsteps
    dx, dy = xl*1.0/xsteps,yl*1.0/ysteps 
    x0, y0 = -xl/2.0+dx/2.0, -yl/2.0+dx/2.0
    dz = zl*1.0/zsteps
    z0 = -zl/2.0+dz/2.0

    z_list = []
    x_list, y_list, N_list_emu,N_list_nbody = [],[],[],[]
    V_list_emu, V_list_nbody = [],[]
    V3d_list_emu, V3d_list_nbody = [],[]
    V3d_dif_list = []

    for z_step in range(zsteps):
        x0 = -xl/2.0+dx/2.0
        for x_step in  range(xsteps):
            y0 =  -yl/2.0+dy/2.0
            for y_step in range(ysteps):

                dif = np.array([x0,y0,z0])
                V3d_dif = np.array([0,0,0])
                lens = np.abs(dif_emus - dif).T
                yes_emu = np.where((lens[0] <= dx/2.0)& (lens[1] <= dy/2.0) & (lens[2] <= dz/2.0))
                N_emu= len(yes_emu[0])

                if(N_emu == 0): 
                    V_emu = 0
                    V3d_emu = 0
                else: 
                    V_emu = np.sum(vmag_emus[yes_emu[0]])/N_emu
                    V3d_emu = np.sqrt(np.sum(np.power(np.sum(v3d_emus[yes_emu[0]],axis=0),2)))/N_emu
                    V3d_dif = np.sum(v3d_emus[yes_emu[0]],axis=0)/N_emu

                lens = np.abs(dif_nbodys - dif).T
                yes_nbody = np.where((lens[0] <= dx/2.0)& (lens[1] <= dy/2.0) & (lens[2] <= dz/2.0))
                N_nbody= len(yes_nbody[0])

                if(N_nbody == 0): 
                    V_nbody = 0
                    V3d_nbody = 0
                else: 
                    V_nbody= np.sum(vmag_nbodys[yes_nbody[0]])/N_nbody
                    V3d_nbody = np.sqrt(np.sum(np.power(np.sum(v3d_nbodys[yes_nbody[0]],axis=0),2)))/N_nbody
                    V3d_dif = V3d_dif - (np.sum(v3d_nbodys[yes_nbody[0]],axis=0)/N_nbody)

                x_list.append(x0)
                y_list.append(y0)
                z_list.append(z0)
                N_list_emu.append(N_emu)
                N_list_nbody.append(N_nbody)
                V_list_emu.append(V_emu)
                V_list_nbody.append(V_nbody)
                V3d_list_emu.append(V3d_emu)
                V3d_list_nbody.append(V3d_nbody)
                V3d_dif_list.append(np.sqrt(np.sum(np.power(V3d_dif,2))))
        #         print(x0,y0,N_emu, N_nbody)
                y0 += dy
            x0 += dx
        z0 += dz
        
        
    x_list = np.array(x_list)
    y_list = np.array(y_list)
    z_list = np.array(z_list)
    N_list_nbody = np.array(N_list_nbody)
    N_list_emu = np.array(N_list_emu)
    r_max = xl/2.0*np.sqrt(2.1)
    d_square = np.sqrt(np.power(x_list, 2) + np.power(y_list,2) + np.power(z_list,2))

    mass_per_particle = 6.565293600596489e11 #msun/h

    r_list = np.logspace(-1.5,np.log10(r_max),200)
    rho_list_emu = []
    rho_list_nbody = []

    for r in r_list:
        r_args = np.where(d_square <= r)[0]
        mass_enc_emu = np.sum(N_list_emu[r_args])*mass_per_particle/N_targets
        mass_enc_nbody = np.sum(N_list_nbody[r_args])*mass_per_particle/N_targets
        vol = 4/3 * np.pi * np.power(r,3.0)
        rho_list_emu.append(mass_enc_emu/vol)
        rho_list_nbody.append(mass_enc_nbody/vol)
        
        
        
    fig, axs = plt.subplots(1,2,figsize=(10,4))
    print_mass = scientific_notation="{:.3e}".format(target_mass)
    print_massn = scientific_notation="{:.3e}".format(np.mean(target_mass_list_nbod).value)
    print_masse = scientific_notation="{:.3e}".format(np.mean(target_mass_list_emu).value)

    plt.suptitle("N="+str(N_targets)+" target mass = "+str(print_mass)+" rvir="+str(int(r_vir(target_mass,0)*1000)/1000.0) +
                "\n mean nbody mass = "+str(print_massn) +
                " mean emu mass = "+str(print_masse))
    # axs[0].plot(r_list, rho_list_emu, label ="emu")
    # axs[0].plot(r_list, rho_list_nbody, label ="nbody")
    # axs[0].legend()
    # axs[0].set_xlabel("r [Mpc]")
    # axs[0].set_ylabel("density [Msun/Mpc^3]")
    # axs[0].set_yscale("log")
    mean_density = mass_per_particle*np.power(512.0/1000,3)
    p200 = 200*mean_density

    axs[0].plot(np.log10(r_list), np.log10(rho_list_emu), label ="emu")
    axs[0].plot(np.log10(r_list), np.log10(rho_list_nbody), label ="nbody")
    axs[0].plot(np.log10(r_list), np.log10(np.linspace(p200, p200,len(r_list))),label="rho_mean")
    axs[0].legend()
    axs[0].set_xlabel("log(r/Mpc)")
    axs[0].set_ylabel("log(density/[Msun/Mpc^3])")


    rat = np.array(rho_list_emu)/np.array(rho_list_nbody)
    axs[1].plot(r_list, rat)
    axs[1].set_xlabel("r [Mpc]")
    axs[1].set_ylabel("rho_emu/rho_nbody")

    r200_nbody = r_list[np.argmin(np.abs(rho_list_nbody-p200))]
    r200_emu = r_list[np.argmin(np.abs(rho_list_emu-p200))]

    axs[1].plot(np.linspace(r200_nbody,r200_nbody,10),
                np.linspace(np.min(rat), np.max(rat),10),
                label="r200_nbody="+str(int(r200_nbody*1000)/1000.0))
    axs[1].plot(np.linspace(r200_emu,r200_emu,10),
                np.linspace(np.min(rat), np.max(rat),10),
                label="r200_emu="+str(int(r200_emu*1000)/1000.0))

    axs[1].legend()


    plt.savefig("figures/density_v_r_tm_"+str(print_mass)+".pdf")




