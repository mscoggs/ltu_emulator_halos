#!/bin/bash
#SBATCH -J ltu_bk1           # Job name
#SBATCH -o LOG/bk.o1       # Name of stdout output file
#SBATCH -e LOG/bk.e1       # Name of stderr error file
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


rm LOG/bk1
python -u bk_equi.py nbod 1 >> LOG/bk1
date
