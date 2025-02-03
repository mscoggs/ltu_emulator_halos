import os
import glob
import numpy as np
import shutil
submit_str = "#!/bin/bash\n\n"



def make_changes(line, word, val):
    #print(word, line)
    #print(word in line)
    if(word in line):
        line = line.split()
        line = line[0] + "   " + val

    return line


for count in range(8):
    dir_ = "sb"+str(count)
    file = open("run_emu_base.sh", "r")
    replacement = ""
    for line in file:
        line = line.strip()
        line = line.replace("NUM", str(count))
        replacement = replacement + line + "\n"
    file.close()
    fout = open("sb"+str(count)+"/run_emu.sh", "w")
    fout.write(replacement)
    fout.close()
    submit_str += "cd sb"+str(count) + "\n"
    submit_str += "sbatch run_emu.sh" + "\n"
    submit_str += "cd .." + "\n"

    om = 0
    ol = 0
    file = open(dir_+"/2LPT.param", "r")
    for line in file:
        line = line.strip()
        if("Omega " in line): om = float(line.split()[1])
        if("OmegaLam" in line): ol = float(line.split()[1])
    replacement = str(om) + " " + str(ol)
    fparam = open("/scratch/08288/tg875874/ltu_gobig/sb"+str(count)+"/cosmo_params.dat", "w")
    fparam.write(replacement)
    fparam.close()

sbatch_submit = open("submit_emu.sh", "w")
sbatch_submit.write(submit_str)
sbatch_submit.close()
os.system("chmod +x submit_emu.sh")
