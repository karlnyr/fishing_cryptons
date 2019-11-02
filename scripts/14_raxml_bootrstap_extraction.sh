#!/usr/bin/bash -l

#SBATCH -A snic2018-3-568
#SBATCH -p core
#SBATCH -n 12
#SBATCH -t 01:00:00
#SBATCH -J bootstrap_info_extraction
#SBATCH --mail-type=ALL
#SBATCH --mail-user karl.nyren.6523@student.uu.se

module load bioinfo-tools
module load raxml/8.2.10-gcc-mpi

BOOTSTRAPS=$1
ML_TREE=$2
mr_cons_BS='MR_CONS-bootstrap'

raxmlHPC \
    -f b \
    -z $BOOTSTRAPS \
    -t $ML_TREE \
    -m PROTGAMMAWAGF \
    -n $mr_cons_BS
    -T 12
