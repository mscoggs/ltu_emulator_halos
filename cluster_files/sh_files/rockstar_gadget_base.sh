#!/bin/bash 
#SBATCH -J ltu_rockstar_gadgetNUM
#SBATCH -o rockstar_gadget.oNUM 
#SBATCH -e rockstar_gadget.eNUM
#SBATCH -p icx          
#SBATCH -N 4            
#SBATCH -n 32          
#SBATCH -t 4:00:00      
#SBATCH --mail-user=mts2188@columbia.edu
#SBATCH --mail-type=NONE    # Send email at begin and end of job
#SBATCH -A TG-AST140041

# Other commands must follow all #SBATCH directives...
module load gcc
module load hdf5
module list
pwd
date


DIR=/scratch/08288/tg875874/ltu_gobig/sbNUM/rockstar_halos_gadget
rm rockstar_gadget
rm "$DIR"/auto-rockstar.cfg
./rockstar-galaxies -c rockstar_gadget.cfg  >& rockstar_gadget &
until [ -e "$DIR"/auto-rockstar.cfg ]
do
	sleep 5
done
echo "starting"
ibrun ./rockstar-galaxies -c "$DIR"/auto-rockstar.cfg  >> rockstar_gadget
echo "killing backgground jobs"
jobs -p | xargs kill
date
