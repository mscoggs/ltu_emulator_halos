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


filebase = "convert_pos_to_ascii"
for count in range(8):
    dir_ = "sb"+str(count)
    param_file = open(dir_+"/2LPT.param")
    for line in param_file:
        if("Omega " in line): OMEGAM = float(line.split()[-1])
        if("OmegaLambda" in line): OMEGAL = float(line.split()[-1])
        if("HubbleParam" in line): H = float(line.split()[-1])
        if("Sigma8" in line): S8 = float(line.split()[-1])

    print("making ", dir_," conversion with Om, Ol, H, S8:", OMEGAM, OMEGAL, H, S8)

    os.system("cp "+filebase+".py "+dir_+"/"+filebase+".py")
    file = open(filebase+"_base.sh", "r")
    replacement = ""
    for line in file:
        line = line.strip()
        line = line.replace("NUM", str(count))
        line = line.replace("OMPARAM", str(OMEGAM))
        line = line.replace("OLPARAM", str(OMEGAL))
        line = line.replace("HPARAM", str(H))
        replacement = replacement + line + "\n"
    file.close()
    fout = open("sb"+str(count)+"/"+filebase+".sh", "w")
    fout.write(replacement)
    fout.close()
    submit_str += "cd sb"+str(count) + "\n"
    submit_str += "sbatch "+filebase+".sh" + "\n"
    submit_str += "cd .." + "\n"



sbatch_submit = open("submit_convert3.sh", "w")
sbatch_submit.write(submit_str)
sbatch_submit.close()
os.system("chmod +x submit_convert3.sh")



