import yt
import sys
import numpy as np
import pandas as pd

dir_num = int(sys.argv[1])
halo_type = str(sys.argv[2])
target_mass_power = float(sys.argv[3])
batch_num = int(sys.argv[4])



dir_ = "/scratch/08288/tg875874/ltu_gobig/sb"+str(dir_num)+"/"

if(halo_type == "rockstar"): halo_dir = "rockstar_halos"
elif(halo_type == "fof"): halo_dir = "halo_catalogs"
else: halo_dir = "WRONGTYPE"


print(dir_num, halo_type, halo_dir)
print("working on target_mass and batch_num", target_mass_power, batch_num)

dsN = yt.load(dir_+ halo_dir+"_gadget/halos_0.0.bin").all_data()

massN = dsN["all","particle_mass"]
massN = dsN["all","particle_mass"].to("Msun/h").value.astype(np.float32)
posN = dsN["all","particle_position"].to("Mpc/h").value.astype(np.float32)
radN = dsN["all","virial_radius"].to("Mpc/h").value.astype(np.float32)



dsE = yt.load(dir_+ halo_dir+"/halos_0.0.bin").all_data()
massE = dsE["all","particle_mass"].to("Msun/h").value.astype(np.float32)
posE = dsE["all","particle_position"].to("Mpc/h").value.astype(np.float32)
radE = dsE["all","virial_radius"].to("Mpc/h").value.astype(np.float32)

del dsN
del dsE

dtype = np.float32
Np = 1536**3
posPartE = (np.load(dir_+"pos_out.npy").astype(dtype)).reshape(3,Np).T
f = "snapdir_004/snap_004.0.hdf5"
dsPartN = yt.load(dir_+f)
posPartN = ((dsPartN.all_data()["all","Coordinates"].astype(dtype)).to("Mpc/h")).value
del dsPartN


N=100

target_mass = np.power(10.0,target_mass_power)
a,b = N*batch_num, N*(batch_num+1)
argsN = np.argsort(np.abs(massN-target_mass))[0:500]
argsE = np.argsort(np.abs(massE-target_mass))[0:500]


radN = radN[argsN]
radE = radE[argsE]

maxRad = np.max(radN)
maxRad2 = np.max(radE)
maxRad = np.max([maxRad, maxRad2])*1.0

argsN = argsN[a:b]
argsE = argsE[a:b]
massN = massN[argsN]
massE = massE[argsE]
posN = posN[argsN]
posE = posE[argsE]



#first, just trying to target nbody only haloes
#arrays are N by 3
#need to be transposed 
posPartN = posPartN.T
posPartE = posPartE.T

#planning to break the box up so the np.where is faster.
#distance check might be more time efficiet?
'''
posPartNSub = =np.array([])
subN = 2
L = 3000.0
step = L/subN
buffer = maxRad
bounds = []
for x in range(subN):
    xl, xr = x*step, (x+1)*step
    for y in range(subN):
        yl, yr = y*step, (y+1)*step
        for z in range(subN):
            zl, zr = z*step, (z+1)*step
         
'''








#extract the particles and add them to a list
for n in range(N):
    targetPosN = posN[n]
    tbl = targetPosN-maxRad
    tbr = targetPosN+maxRad
    #taking a smaller zsclie
    #tbl[2] = targetPosN[2]-maxRad*0.3
    #tbr[2] = targetPosN[2]+maxRad*0.3

    print("these are the targets and max rad")
    print(tbl, tbr, maxRad)

    targetPartsN = np.where((tbl[0]<=posPartN[0]) & (posPartN[0] <= tbr[0]) &
                            (tbl[1]<=posPartN[1]) & (posPartN[1] <= tbr[1]) &
                            (tbl[2]<=posPartN[2]) & (posPartN[2] <= tbr[2]))
    targetPartsE = np.where((tbl[0]<=posPartE[0]) & (posPartE[0] <= tbr[0]) &
                            (tbl[1]<=posPartE[1]) & (posPartE[1] <= tbr[1]) &
                            (tbl[2]<=posPartE[2]) & (posPartE[2] <= tbr[2]))

    targetPartsE = posPartE.T[targetPartsE] - targetPosN
    targetPartsN = posPartN.T[targetPartsN] - targetPosN

    if(n==0): allTargetsN, allTargetsE = targetPartsN, targetPartsE
    else: 
        allTargetsN = np.append(allTargetsN, targetPartsN, axis=0)
        allTargetsE = np.append(allTargetsE, targetPartsE, axis=0)

print(allTargetsN)

#arrays are N by 3
np.save("../data/stacked_nbod_"+str(dir_num)+"_mass_"+str(target_mass_power)+"_batch_"+str(batch_num), allTargetsN)
np.save("../data/stacked_emu_"+str(dir_num)+"_mass_"+str(target_mass_power)+"_batch_"+str(batch_num), allTargetsE)

#now 3byN

'''

xsteps = 30
ysteps = xsteps
dx = 2.0*maxRad/xsteps
dy = dx


xlist, ylist, nEmu, nNbod = [],[],[],[]

x0 = -maxRad
for xstep in range(xsteps):
    y0 = -maxRad
    for ystep in range(ysteps):

        targetN = np.where((x0 <= allTargetsN[0]) & (allTargetsN[0] < x0+dx) &
                           (y0 <= allTargetsN[1]) & (allTargetsN[1] < y0+dy))

        targetE = np.where((x0 <= allTargetsE[0]) & (allTargetsE[0] < x0+dx) &
                           (y0 <= allTargetsE[1]) & (allTargetsE[1] < y0+dy))

        
        nEmu.append(np.size(targetE))
        nNbod.append(np.size(targetN))

        xlist.append(x0+dx/2.0)
        ylist.append(y0+dy/2.0)
        y0 += dy
    x0 += dx

#importing pandas caused issues with yt ??? so doing this down here
df = pd.DataFrame({'x': xlist, 'y': ylist, 'nEmu': nEmu, 'nNbod': nNbod})
df.to_csv("../data/stacked_"+str(dir_num)+"_mass_"+str(target_mass_power)+"_batch_"+str(batch_num)+".txt")
'''
