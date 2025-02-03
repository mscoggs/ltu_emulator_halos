#!/bin/bash 
#SBATCH -J convert_pos_to_asciiNUM         # Job name
#SBATCH -o convert_pos_to_ascii.oNUM #Name of stdout output file
#SBATCH -e convert_pos_to_ascii.eNUM       # Name of stdout error file
#SBATCH -p icx            # Queue (partition) name
#SBATCH -N 1               # Total # of nodes
#SBATCH -n 1              # Total # of mpi tasks
#SBATCH -t 8:00:00        # Run time (hh:mm:ss)
#SBATCH --mail-user=mts2188@columbia.edu
#SBATCH --mail-type=NONE    # Send email at begin and end of job
#SBATCH -A TG-AST140041

# Other commands must follow all #SBATCH directives...


module load python
pwd
date
rm convert_pos_to_ascii



python -u convert_pos_to_ascii.py NUM OMPARAM OLPARAM HPARAM >> convert_pos_to_ascii


