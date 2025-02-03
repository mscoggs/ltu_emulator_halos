#!/bin/bash 
#SBATCH -J 2lpt_convertNUM         # Job name
#SBATCH -o convert_gadget_to_npy.oNUM #Name of stdout output file
#SBATCH -e convert_gadget_to_npy.eNUM       # Name of stderr error file
#SBATCH -p icx          # Queue (partition) name
#SBATCH -N 1               # Total # of nod
#SBATCH -n 1              # Total # of mpi tasks
#SBATCH -t 1:40:00        # Run time (hh:mm:ss)
#SBATCH --mail-user=mts2188@columbia.edu
#SBATCH --mail-type=NONE    # Send email at begin and end of job
#SBATCH -A TG-AST140041

# Other commands must follow all #SBATCH directives...


module load python
pwd
date
rm convert_gadget_to_npy

#python -u convert_gadget_to_npy.py $SCRATCH/ltu_gobig/ICs/ >> convert_gadget_to_npy
python -u convert_gadget_to_npy.py NUM >> convert_gadget_to_npy

