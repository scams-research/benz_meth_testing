#!/bin/bash
# Job options
#SBATCH --job-name=lammps
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32
#SBATCH --time=24:00:00
#SBATCH --constraint=cpu_model:epyc-9655

# load module - not sure it's needed?
module load pmix

# 1. Initialize Spack
source /projects/public/b56as/spack/share/spack/setup-env.sh

# 2. Load the package OR activate an environment
spack env activate lammps-env
AOCC_LIB=$(spack location -i aocc@5.0.0)/lib
export LD_LIBRARY_PATH=${AOCC_LIB}:${LD_LIBRARY_PATH}
export OMP_NUM_THREADS=1

# Launch job
srun --mpi=pmix --cpu-bind=cores --distribution=block:block --unbuffered lmp -in equil.lammps