#!/bin/bash
#SBATCH -J ltu_bk4           # Job name
#SBATCH -o LOG/bk.o4       # Name of stdout output file
#SBATCH -e LOG/bk.e4       # Name of stderr error file
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


rm LOG/bk4
python -u bk_equi.py nbod 4 >> LOG/bk4
date
