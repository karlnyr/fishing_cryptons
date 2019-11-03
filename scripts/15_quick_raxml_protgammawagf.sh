#!/usr/bin/bash -l

#SBATCH -A snic2018-3-568
#SBATCH -p core
#SBATCH -n 12
#SBATCH -t 16:00:00
#SBATCH -J protgammaf_phylogeny
#SBATCH --mail-type=ALL
#SBATCH --mail-user karl.nyren.6523@student.uu.se

module load bioinfo-tools
module load raxml/8.2.10-gcc-mpi

ALIGNMENT_FILE_PATH=$1
FILE_EXT=$2

MODEL='PROTGAMMAWAGF'

# MPI loaded for boostrapping, T for number of threads(1 thread per core recommended), -b for random bootstrap seed(reproducible if same data),
# -N Number of bootstraps to be performed, -p to reproduce ML.
raxmlHPC \
    -f a \
    -p 3214 \
    -x 123123 \
    -s $ALIGNMENT_FILE_PATH \
    -n $FILE_EXT \
    -m $MODEL \
    -T 12 \
    -N autoMRE
