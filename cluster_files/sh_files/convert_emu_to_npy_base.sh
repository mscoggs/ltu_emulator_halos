#!/bin/bash 
#SBATCH -J convert_emu_to_npyNUM         # Job name
#SBATCH -o convert_emu_to_npy.oNUM #Name of stdout output file
#SBATCH -e convert_emu_to_npy.eNUM       # Name of stdout error file
#SBATCH -p icx            # Queue (partition) name
#SBATCH -N 1               # Total # of nodes
#SBATCH -n 1              # Total # of mpi tasks
#SBATCH -t 1:00:00        # Run time (hh:mm:ss)
#SBATCH --mail-user=mts2188@columbia.edu
#SBATCH --mail-type=NONE    # Send email at begin and end of job
#SBATCH -A TG-AST140041

# Other commands must follow all #SBATCH directives...


module load python
pwd
date
rm convert_emu_to_npy



python -u convert_emu_to_npy.py NUM >> convert_emu_to_npy


