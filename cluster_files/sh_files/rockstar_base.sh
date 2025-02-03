#!/bin/bash 
#SBATCH -J ltu_rockstarNUM           # Job name
#SBATCH -o rockstar.oNUM       # Name of stdout output file
#SBATCH -e rockstar.eNUM       # Name of stderr error file
#SBATCH -p icx          # Queue (partition) name
#SBATCH -N 4               # Total # of nodes
#SBATCH -n 32               # Total # of mpi tasks
#SBATCH -t 4:00:00        # Run time (hh:mm:ss)
#SBATCH --mail-user=mts2188@columbia.edu
#SBATCH --mail-type=NONE    # Send email at begin and end of job
#SBATCH -A TG-AST140041

# Other commands must follow all #SBATCH directives...
module load gcc
module load hdf5
module list
pwd
date

DIR=/scratch/08288/tg875874/ltu_gobig/sbNUM/rockstar_halos
rm rockstar
rm "$DIR"/auto-rockstar.cfg
./rockstar-galaxies -c rockstar.cfg  >& rockstar &
until [ -e "$DIR"/auto-rockstar.cfg ]
do
	sleep 5
done
echo "starting"
ibrun ./rockstar-galaxies -c "$DIR"/auto-rockstar.cfg  >> rockstar
echo "killing backgground jobs"
jobs -p | xargs kill
date
