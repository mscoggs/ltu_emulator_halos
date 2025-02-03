from kymatio.torch import HarmonicScattering3D
import numpy as np
import torch
from kymatio.scattering3d.backend.torch_backend import TorchBackend3D
import sys
import Pk_library as PKL
import MAS_library as MASL
import pandas as pd
import redshift_space_library as RSL



dir_ = "/scratch/08288/tg875874/ltu_gobig/"
N=1536
dtype = np.float32
Np = N**3
grid  = 256
BoxSize = 3000.0
MAS     = "CIC"
verbose = True
axis = 0
threads = 10
ptypes = [1]

J,L = 4,4
integral_powers = [0.8]
sigma = 0.8
n_mesh = grid
print("init scatter")

scattering = HarmonicScattering3D(J=J, shape=(n_mesh, n_mesh, n_mesh), L=L,
        sigma_0 = sigma, integral_powers=integral_powers, max_order=2)
print("sending to cpu")
scattering.to("cpu")

for count in range(8):

    full_dir = dir_+"sb"+str(count)+"/"
    print("working on emu")

    f = full_dir +"pos_out.npy"
    pos = np.load(f).astype(dtype)
    pos = (pos).reshape(3,Np).T
    
    delta = np.zeros((grid,grid,grid), dtype=dtype)
    MASL.MA(pos, delta, BoxSize, MAS, verbose=verbose)

    density = delta
    full_density_batch = torch.from_numpy(np.asarray(np.real(density)))
    full_density_batch = full_density_batch.to("cpu").float()
    full_density_batch = full_density_batch.contiguous()
    full_order_0 = TorchBackend3D.compute_integrals(full_density_batch, integral_powers)
    full_scattering = scattering(full_density_batch)
    s_mat_avg = np.real(full_scattering.cpu().numpy()[:,:,0])
    s_mat_avg = s_mat_avg.flatten()
    s0 = full_order_0.cpu().numpy()[0,0]
    wst_coefficients = np.hstack((s0, s_mat_avg))/n_mesh**3

    n = np.array(list(range(np.size(wst_coefficients))))
    df = pd.DataFrame({'n': n, 'wst_coefficients': wst_coefficients})
    df.to_csv("data/wst_emu_"+str(count))



    print("working on nbody", count)
    f = full_dir+"snapdir_004/snap_004"
    do_RSD = False
    delta = MASL.density_field_gadget(f, ptypes, grid, MAS, do_RSD, axis, verbose)
    density = delta
    full_density_batch = torch.from_numpy(np.asarray(np.real(density)))
    full_density_batch = full_density_batch.to("cpu").float()
    full_density_batch = full_density_batch.contiguous()
    full_order_0 = TorchBackend3D.compute_integrals(full_density_batch, integral_powers)
    full_scattering = scattering(full_density_batch)
    s_mat_avg = np.real(full_scattering.cpu().numpy()[:,:,0])
    s_mat_avg = s_mat_avg.flatten()
    s0 = full_order_0.cpu().numpy()[0,0]
    wst_coefficients = np.hstack((s0, s_mat_avg))/n_mesh**3

    n = np.array(list(range(np.size(wst_coefficients))))
    df = pd.DataFrame({'n': n, 'wst_coefficients': wst_coefficients})
    df.to_csv("data/wst_nbod_"+str(count))

