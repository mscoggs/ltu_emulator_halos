import os
import glob
import numpy as np
import shutil
import sys
submit_str = "#!/bin/bash\n\n"



def make_changes(line, word, val):
    #print(word, line)
    #print(word in line)
    if(word in line):
        line = line.split()
        line = line[0] + "   " + val

    return line

L=3000.0
N= 1536.0
scratch = '/scratch/08288/tg875874/ltu_gobig/'
filebase = "rockstar_gadget"
for count in range(8):

    dir_ = "sb"+str(count)
    param_file = open(dir_+"/2LPT.param")
    for line in param_file:
        if("Omega " in line): OMEGAM = float(line.split()[-1])
        if("OmegaLambda" in line): OMEGAL = float(line.split()[-1])
        if("HubbleParam" in line): H = float(line.split()[-1])
        if("Sigma8" in line): S8 = float(line.split()[-1])
    RHO_CRIT = 2.77536627e11*H*H #Msun/MPC^3
    vol_box = np.power(L/H,3) #Mpc^3
    total_mass = OMEGAM * RHO_CRIT * vol_box
    mass_per_particle = np.float32(total_mass / np.power(N,3))
    print("making ", dir_," conversion with Om, Ol, H, S8:", OMEGAM, OMEGAL, H, S8)
    print("and mass per particle:", mass_per_particle)



    os.system("cp rockstar-galaxies "+dir_+"/rockstar-galaxies")
    os.system("rm -r "+scratch+dir_+"/rockstar_halos_gadget")
    os.system("mkdir "+scratch+dir_+"/rockstar_halos_gadget")


    file = open(filebase+"_base.sh", "r")
    replacement = ""
    for line in file:
        line = line.strip()
        line = line.replace("NUM", str(count))
        replacement = replacement + line + "\n"
    file.close()
    fout = open("sb"+str(count)+"/"+filebase+".sh", "w")
    fout.write(replacement)
    fout.close()

    file = open(filebase+".cfg", "r")
    replacement = ""
    for line in file:
        line = line.strip()
        line = line.replace("NUMBER", str(count))
        line = line.replace("MASSPARAM", str(mass_per_particle))
        line = line.replace("OMPARAM", str(OMEGAM))
        line = line.replace("OLPARAM", str(OMEGAL))
        line = line.replace("HPARAM", str(H))
        replacement = replacement + line + "\n"
    file.close()
    fout = open("sb"+str(count)+"/"+filebase+".cfg", "w")
    fout.write(replacement)
    fout.close()

    submit_str += "cd sb"+str(count) + "\n"
    submit_str += "sbatch "+filebase+".sh" + "\n"
    submit_str += "cd .." + "\n"



sbatch_submit = open("submit_"+filebase+".sh", "w")
sbatch_submit.write(submit_str)
sbatch_submit.close()
os.system("chmod +x submit_"+filebase+".sh")
