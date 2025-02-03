import os
import glob
import numpy as np
import shutil
import sys
import pandas as pd
submit_str = "#!/bin/bash\n\n"

count_list = []
om_list = []
for count in range(8):
    dir_ = "sb"+str(count)
    param_file = open(dir_+"/2LPT.param")
    for line in param_file:
        if("Omega " in line): OMEGAM = float(line.split()[-1])
        if("OmegaLambda" in line): OMEGAL = float(line.split()[-1])
        if("HubbleParam" in line): H = float(line.split()[-1])
        if("Sigma8" in line): S8 = float(line.split()[-1])
    count_list.append(count)
    om_list.append(OMEGAM)
df = pd.DataFrame({'n': count_list, 'Om': om_list})
df.to_csv("data/om_list")
