#!/bin/bash 
#SBATCH -J map2mapemuNUM         # Job name
#SBATCH -o emu.oNUM       # Name of stdout output file
#SBATCH -e emu.eNUM       # Name of stderr error file
#SBATCH -p icx            # Queue (partition) name
#SBATCH -N 1               # Total # of nodes
#SBATCH -n 10              # Total # of mpi tasks
#SBATCH -t 5:40:00        # Run time (hh:mm:ss)
#SBATCH --mail-user=mts2188@columbia.edu
#SBATCH --mail-type=NONE    # Send email at begin and end of job
#SBATCH -A TG-AST140041

# Other commands must follow all #SBATCH directives...


module load python
pwd
date
rm emu


IN_FILES='/scratch/08288/tg875874/ltu_gobig/sbNUM/displacement_2lpt.npy'

STYLE_FILES='/scratch/08288/tg875874/ltu_gobig/sbNUM/cosmo_params.dat'

OUTPUT_DIRS='/scratch/08288/tg875874/ltu_gobig/sbNUM'

export TF_CPP_MIN_LOG_LEVEL=3

echo $IN_FILES

m2m.py run \
    --in-pattern "$IN_FILES" \
    --style-pattern "$STYLE_FILES" \
    --out-pattern "$OUTPUT_DIRS" \
    --crop 128 --batches 1 --loader-workers 5 >> emu
    #--no_vel >> output.txt    

# Can output either only dis, only vel, or both dis and vel
#    --no_dis --no_vel # Can output either only dis, only vel, or both dis and vel


