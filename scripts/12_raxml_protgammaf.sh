#!/usr/bin/bash -l

#SBATCH -A snic2018-3-568
#SBATCH -p core
#SBATCH -n 6
#SBATCH -t 16:00:00
#SBATCH -J protgammaf_phylogeny
#SBATCH --mail-type=ALL
#SBATCH --mail-user karl.nyren.6523@student.uu.se

module load bioinfo-tools
module load raxml/8.2.10-gcc-mpi

ALIGNMENT_FILE_PATH=$1
OUTFILE_PATH=$2
MODEL='PROTGAMMAWGAF'


# MPI loaded for repetitive
raxmlHPC -s $ALIGNMENT_FILE_PATH \
    -n $OUTFILE_PATH \
    -m $MODEL \
    -T 6 \
    -b 126345 \
    -B 0.03 \
    -N 10
