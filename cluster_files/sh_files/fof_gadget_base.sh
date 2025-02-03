#!/bin/bash 
#SBATCH -J ltu_fof_gadgetNUM           # Job name
#SBATCH -o fof_gadget.oNUM       # Name of stdout output file
#SBATCH -e fof_gadget.eNUM       # Name of stderr error file
#SBATCH -p icx          # Queue (partition) name
#SBATCH -N 16               # Total # of nodes
#SBATCH -n 16              # Total # of mpi tasks
#SBATCH -t 2:00:00        # Run time (hh:mm:ss)
#SBATCH --mail-user=mts2188@columbia.edu
#SBATCH --mail-type=NONE    # Send email at begin and end of job
#SBATCH -A TG-AST140041

# Other commands must follow all #SBATCH directives...
module load python
module list
pwd
date


rm fof_gadget
ibrun python -u fof_gadget.py NUM >> fof_gadget
date
