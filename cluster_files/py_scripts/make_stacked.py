import os
import sys
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


filebase = "stacked"
target_om_list = [0.14290558, 0.45916243, 0.31571019]
target_list = [3,5,6]

count = int(sys.argv[1])

dir_ = "sb"+str(count)
print("making stacks for ", dir_)
os.system("cp "+filebase+".py "+dir_+"/"+filebase+".py")
label = 0
for target_mass in [13.5,14.0, 14.5]:
    for batch_num in [0,1,2,3,4]:
        file = open(filebase+"_base.sh", "r")
        replacement = ""
        for line in file:
            line = line.strip()
            line = line.replace("TARGETMASS", str(target_mass))
            line = line.replace("BATCHNUM", str(batch_num))
            line = line.replace("NUM", str(count))
            line = line.replace("LABEL", str(label))
            replacement = replacement + line + "\n"
        file.close()
        fname = filebase+str(batch_num)+"_"+str(target_mass)
        fout = open("sb"+str(count)+"/"+fname+".sh", "w")
        fout.write(replacement)
        fout.close()
        submit_str += "cd sb"+str(count) + "\n"
        submit_str += "sbatch "+fname+".sh" + "\n"
        print(fname, batch_num, target_mass)
        submit_str += "cd .." + "\n"
        label +=1




submit_name = "submit_"+filebase+"_"+str(count)+".sh"
sbatch_submit = open(submit_name, "w")
sbatch_submit.write(submit_str)
sbatch_submit.close()
os.system("chmod +x "+submit_name)

