import numpy as np
import yt
import sys
from yt.extensions.astro_analysis.halo_analysis import HaloCatalog
yt.enable_parallelism()

number = int(sys.argv[1])

dir_= "/scratch/08288/tg875874/ltu_gobig/sb"+str(number)+"/"
f = "snapdir_004/snap_004.0.hdf5"

print("loading gadget data")
ds = yt.load(dir_+f)
hc=HaloCatalog(data_ds = ds, finder_method="fof", output_dir=dir_+"halo_catalogs_gadget")#,finder_kwargs={"save_particles"='False'})
print("running hc")
hc.create(save_halos=True, save_output=True)
