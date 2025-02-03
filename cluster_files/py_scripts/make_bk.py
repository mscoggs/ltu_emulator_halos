import os
import sys
import glob
import numpy as np
import shutil
submit_str = "#!/bin/bash\n\n"



filebase = "bk_equi"
NUM = 0
for type_ in ["nbod", "emu"]:
    for count in range(8):

        file = open(filebase+"_base.sh", "r")
        replacement = ""
        for line in file:
            line = line.strip()
            line = line.replace("NUM", str(NUM))
            line = line.replace("TYPE", str(type_))
            line = line.replace("COUNT", str(count))
            replacement = replacement + line + "\n"
        file.close()
        fout = open("bk"+str(NUM)+".sh", "w")
        fout.write(replacement)
        fout.close()
        submit_str += "sbatch bk"+str(NUM)+".sh" + "\n"
        NUM += 1




submit_name = "submit_"+filebase+".sh"
sbatch_submit = open(submit_name, "w")
sbatch_submit.write(submit_str)
sbatch_submit.close()
os.system("chmod +x "+submit_name)

