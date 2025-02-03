import os
import glob
import numpy as np
import shutil
submit_str = "#!/bin/bash\n\n"

lpt_files = np.sort(list(glob.iglob("sb*/2LPT.param")))

print(lpt_files)



def make_changes(line, word, val):
    #print(word, line)
    #print(word in line)
    if(word in line):
        line = line.split()
        line = line[0] + "   " + val

    return line


count = 0
for f in lpt_files:
    print(f)
    dir_ = "sb"+str(count)

    os.system("rm "+dir_+"/2LPTic")
    os.system("rm "+dir_+"/2LPTic_grid")
    os.system("cp 2LPTic "+dir_+"/2LPTic")
    os.system("cp 2LPTic_grid "+dir_+"/2LPTic_grid")
    file = open(f, "r")
    replacement = ""
    for line in file:
        line = line.strip()
        line = make_changes(line, "Nmesh", "3072")
        line = make_changes(line, "OutputDir", "/scratch/08288/tg875874/ltu_gobig/sb"+str(count)+"/ICs/")
        line = make_changes(line, "GlassFile", "/work2/08288/tg875874/stampede3/2lpt/GLASS/dummy_glass_dmonly_64.dat")
        line = make_changes(line, "Redshift", "0")
        #line = make_changes(line, "FileWithInput", "/work2/08288/tg875874/stampede3/2lpt/CAMB_matterpow_0.dat")
        line = make_changes(line, "NumFilesWritten", "64")
        replacement = replacement + line + "\n"
    file.close()
    fout = open(f+"_ic", "w")
    fout.write(replacement)
    fout.close()

    file = open(f, "r")
    replacement = ""

    for line in file:
        line = line.strip()
        line = make_changes(line, "Nmesh", "3072")
        line = make_changes(line, "OutputDir", "/scratch/08288/tg875874/ltu_gobig/sb"+str(count)+"/ICs/")
        line = make_changes(line, "GlassFile", "/work2/08288/tg875874/stampede3/2lpt/GLASS/dummy_glass_dmonly_64.dat")
        line = make_changes(line, "Redshift", "0")
        #line = make_changes(line, "FileWithInput", "/work2/08288/tg875874/stampede3/2lpt/CAMB_matterpow_0.dat")
        line = make_changes(line, "NumFilesWritten", "64")
        line = make_changes(line, "Redshift", "127")
        line = make_changes(line, "NumFilesWritten", "64")
        line = make_changes(line, "FileBase", "grid")
        replacement = replacement + line + "\n"

    file.close()
    fout = open(f+"_ic_grid", "w")
    fout.write(replacement)
    fout.close()

    file = open("2lpt_base.sh", "r")
    replacement = ""
    for line in file:
        line = line.strip()
        line = line.replace("NUM", str(count))
        replacement = replacement + line + "\n"
    file.close()
    fout = open("sb"+str(count)+"/2lpt.sh", "w")
    fout.write(replacement)
    fout.close()
    submit_str += "cd sb"+str(count) + "\n"
    submit_str += "sbatch 2lpt.sh" + "\n"
    submit_str += "cd .." + "\n"

    count+= 1


sbatch_submit = open("submit_2lpt.sh", "w")
sbatch_submit.write(submit_str)
sbatch_submit.close()
