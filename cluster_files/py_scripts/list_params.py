import os
import glob
import numpy as np
import shutil
import sys
submit_str = "#!/bin/bash\n\n"



scratch = '/scratch/08288/tg875874/ltu_gobig/'
for count in range(8):

    dir_ = "sb"+str(count)
    param_file = open(dir_+"/2LPT.param")
    for line in param_file:
        if("Omega " in line): OMEGAM = float(line.split()[-1])
        if("OmegaLambda" in line): OMEGAL = float(line.split()[-1])
        if("HubbleParam" in line): H = float(line.split()[-1])
        if("Sigma8" in line): S8 = float(line.split()[-1])
    p = scratch+dir_+"/CAMB.params"
    camb_file = open(p)
    for line in camb_file:
        if("ombh2 " in line): OMEGAB = float(line.split()[-1])/H**2
        #if("omch2 " in line): OMEGAM2 = float(line.split()[-1])/H**2
        if(" ns =" in line): NS = float(line.split()[-1])


    print(count, " & ", "{:.4f}".format(OMEGAM), " & ", "{:.4f}".format(OMEGAB), " & ", "{:.4f}".format(OMEGAL), " & ", "{:.4f}".format(H), " & ", "{:.4f}".format(S8), " & ", "{:.4f}".format(NS), "\\\\")
    print("\\hline")
