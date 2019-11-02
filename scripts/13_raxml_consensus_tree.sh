#!/usr/bin/bash -l

#SBATCH -A snic2018-3-568
#SBATCH -p core
#SBATCH -n 4
#SBATCH -t 01:00:00
#SBATCH -J
#SBATCH --mail-type=ALL
#SBATCH --mail-user karl.nyren.6523@student.uu.se

module load bioinfo-tools
module load raxml/8.2.10-gcc-mpi
BS_PHYLA=$1
MR_CONS='MR_CONS'

raxmlHPC \
    -I autoMRE \
    -m PROTGAMMAWAGF \
    -z $BS_PHYLA \
    -n $MR_CONS \
    -T 4 \
    -p 12321341
