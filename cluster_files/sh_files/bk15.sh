#!/bin/bash
#SBATCH -J ltu_bk15           # Job name
#SBATCH -o LOG/bk.o15       # Name of stdout output file
#SBATCH -e LOG/bk.e15       # Name of stderr error file
#SBATCH -p icx          # Queue (partition) name
#SBATCH -N 1               # Total # of nodes
#SBATCH -n 1               # Total # of mpi tasks
#SBATCH -t 5:00:00        # Run time (hh:mm:ss)
#SBATCH --mail-user=mts2188@columbia.edu
#SBATCH --mail-type=NONE    # Send email at begin and end of job
#SBATCH -A TG-AST140041

# Other commands must follow all #SBATCH directives...
module load gcc
module load python
module list
pwd
date


rm LOG/bk15
python -u bk_equi.py emu 7 >> LOG/bk15
date
