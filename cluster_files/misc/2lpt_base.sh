#!/bin/bash 
#SBATCH -J 2lptNUM          # Job name
#SBATCH -o 2lpt.oNUM       # Name of stdout output file
#SBATCH -e 2lpt.eNUM       # Name of stderr error file
#SBATCH -p icx          # Queue (partition) name
#SBATCH -N 16               # Total # of nod
#SBATCH -n 512              # Total # of mpi tasks
#SBATCH -t 1:00:00        # Run time (hh:mm:ss)
#SBATCH --mail-user=mts2188@columbia.edu
#SBATCH --mail-type=NONE    # Send email at begin and end of job
#SBATCH -A TG-AST140041

# Other commands must follow all #SBATCH directives...


module load gcc
module load fftw2
module load gsl
pwd
date

rm logIC
mpirun -np 512 ./2LPTic 2LPT.param_ic  >> logIC
mpirun -np 512 ./2LPTic_grid 2LPT.param_ic_grid  >> logIC


