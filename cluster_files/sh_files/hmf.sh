#!/bin/bash 
#SBATCH -J ltu_hmf           # Job name
#SBATCH -o hmf.o1       # Name of stdout output file
#SBATCH -e hmf.e1       # Name of stderr error file
#SBATCH -p icx          # Queue (partition) name
#SBATCH -N 1               # Total # of nodes
#SBATCH -n 1               # Total # of mpi tasks
#SBATCH -t 2:00:00        # Run time (hh:mm:ss)
#SBATCH --mail-user=mts2188@columbia.edu
#SBATCH --mail-type=NONE    # Send email at begin and end of job
#SBATCH -A TG-AST140041

# Other commands must follow all #SBATCH directives...
module load gcc
module load python
module list
pwd
date


rm hmf
python -u hmf.py hmf >> hmf
python -u hmf.py cmf >> hmf
python -u hmf.py raw >> hmf
date
