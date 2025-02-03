#!/bin/bash 
#SBATCH -J ltu_fofNUM           # Job name
#SBATCH -o fof.oNUM       # Name of stdout output file
#SBATCH -e fof.eNUM       # Name of stderr error file
#SBATCH -p icx          # Queue (partition) name
#SBATCH -N 16               # Total # of nodes
#SBATCH -n 16               # Total # of mpi tasks
#SBATCH -t 4:00:00        # Run time (hh:mm:ss)
#SBATCH --mail-user=mts2188@columbia.edu
#SBATCH --mail-type=NONE    # Send email at begin and end of job
#SBATCH -A TG-AST140041

# Other commands must follow all #SBATCH directives...
module load python
module list
pwd
date


rm fof
ibrun python -u fof.py NUM MASSPARAM >> fof
date
