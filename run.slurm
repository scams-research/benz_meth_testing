#!/bin/bash

#SBATCH --job-name=md
#SBATCH --time=1-00:00:00
#SBATCH --nodes=1
#SBATCH --output=out_files/%x-%j.out'

cd $SLURM_SUBMIT_DIR
source ~/miniforge3/bin/activate
conda activate md


echo "Running script: $1"
/home/b35bh/joe3010.b35bh/miniforge3/envs/md/bin/python "$1" "${@:2}"
