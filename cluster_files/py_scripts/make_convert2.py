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


filebase = "convert_emu_to_npy"
for count in range(8):
    dir_ = "sb"+str(count)
    os.system("cp "+filebase+".py "+dir_+"/"+filebase+".py")
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
    submit_str += "cd sb"+str(count) + "\n"
    submit_str += "sbatch "+filebase+".sh" + "\n"
    submit_str += "cd .." + "\n"



sbatch_submit = open("submit_convert2.sh", "w")
sbatch_submit.write(submit_str)
sbatch_submit.close()
os.system("chmod +x submit_convert2.sh")
