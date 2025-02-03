import numpy as np
import yt
from yt.extensions.astro_analysis.halo_analysis import HaloCatalog
import yt.units as u
import sys
yt.enable_parallelism()

number = int(sys.argv[1])
#f = "/scratch/08288/tg875874/ltu_gobig/npy_files/pos_out.npy"
dir_= "/scratch/08288/tg875874/ltu_gobig/sb"+str(number)+"/"
f = "pos_out.npy"

mass = float(sys.argv[2])
N=1536
dtype = np.float32
print("loading mass")
masses = np.linspace(mass,mass,N**3, dtype=dtype)
print("loading pos")
pos = np.float32(np.load(dir_+f))
print("reshaping")
pos = pos.reshape(3,N**3)
print("loading dict into ds")

bbox = np.array([[0.0,3000.0], [0.0,3000.0], [0.0,3000.0]])

data = dict(particle_position_x=pos[0],
        particle_position_y=pos[1],
        particle_position_z=pos[2],
        particle_mass = masses,)
        #bbox = bbox,
        #length_unit=(1.0, "Mpc"))
del pos
del masses
ds = yt.load_particles(data, length_unit=1.0*u.Mpc, mass_unit = 1.0*u.Msun, bbox=bbox)
del data
hc=HaloCatalog(data_ds = ds, finder_method="fof", output_dir = dir_+"halo_catalogs")
del ds
print("running hc")
hc.create(save_halos=True, save_output=True)
