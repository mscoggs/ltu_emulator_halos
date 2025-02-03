import numpy as np
import readgadget
import sys



L = 3000.0
N = 1536
#L = 1000.0
#N = 512
dx = L/N
args = sys.argv
num = int(args[-1])
dir_ ="/scratch/08288/tg875874/ltu_gobig/sb"+str(num)
f = dir_+"/ICs/ics"
g = dir_+"/ICs/grid"

#old grid, not sure if it works
#g = "/scratch/08288/tg875874/ltu_gobig/ICs/grid"
ptype = [1]


print("reading pos")

pos = readgadget.read_block(f, "POS ", ptype)/1e3
print("reading grid")
pos_grid = np.rint(((readgadget.read_block(g, "POS ", ptype)/1e3).T/1.953125)).astype(np.int64)
print("calc indices")

indices = pos_grid[1]*1536**2 + pos_grid[0]*1536 + pos_grid[2]
del pos_grid
arg_sort = np.argsort(indices)
del indices
print("apply indices")
pos = pos[arg_sort]
del arg_sort


print("making g")
g = np.linspace(0,L-dx, N, dtype=np.float32)
g = np.float32(np.vstack(list(map(np.ravel, np.meshgrid(g,g,g)))))

print("calc disp")
d = pos.T - g
del pos
del g
print("apply periodic bounds")
d[np.where(d>L/2)] -= L
d[np.where(d<-L/2)] += L
print("calc mean")
print(np.mean(d))
print(np.mean(np.abs(d)))
print(np.max(d))
print(np.min(d))
print(np.median(d))
print(np.std(d))

print("reshaping")
d = [d[1], d[0], d[2]]
d = np.reshape(d, (3, N, N, N))
print("saving")
np.save(dir_+"/displacement_2lpt.npy", d)
