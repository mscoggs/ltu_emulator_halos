import os
import glob
import numpy as np
import shutil
import sys
submit_str = "#!/bin/bash\n\n"



L=3000.0
N= 1536.0
scratch = '/scratch/08288/tg875874/ltu_gobig/'
filebase = "fof_gadget"
for count in range(8):
    dir_ = "sb"+str(count)

    filename = filebase +".py"
    os.system("cp "+ filename + " " +dir_+"/"+filename)
    os.system("rm -r "+scratch+dir_+"/halo_catalogs_gadget")
    #os.system("mkdir "+scratch+dir_+"/halo_catalogs_gadget")


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



sbatch_submit = open("submit_"+filebase+".sh", "w")
sbatch_submit.write(submit_str)
sbatch_submit.close()
os.system("chmod +x submit_"+filebase+".sh")
