#!/bin/bash

cd sb0
sbatch convert_emu_to_npy.sh
cd ..
cd sb1
sbatch convert_emu_to_npy.sh
cd ..
cd sb2
sbatch convert_emu_to_npy.sh
cd ..
cd sb3
sbatch convert_emu_to_npy.sh
cd ..
cd sb4
sbatch convert_emu_to_npy.sh
cd ..
cd sb5
sbatch convert_emu_to_npy.sh
cd ..
cd sb6
sbatch convert_emu_to_npy.sh
cd ..
cd sb7
sbatch convert_emu_to_npy.sh
cd ..
