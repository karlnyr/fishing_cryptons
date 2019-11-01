#!/usr/bin/bash -l

#SBATCH -A snic2018-3-568
#SBATCH -p core
#SBATCH -n 4
#SBATCH -t 01:00:00
#SBATCH -J protgammaf_phylogeny
#SBATCH --mail-type=ALL
#SBATCH --mail-user karl.nyren.6523@student.uu.se

module load bioinfo-tools
module load raxml/8.2.10-gcc
BS_PHYLA=$1
FILE_EXT=$2

raxmlHPC -J MRE -m PROTGAMMAWAGF -z $BS_PHYLA -n $FILE_EXT
