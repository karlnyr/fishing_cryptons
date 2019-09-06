#!/usr/bin/bash -l

#SBATCH -A snic2018-3-568
#SBATCH -p core
#SBATCH -n 4
#SBATCH -t 01:30:00
#SBATCH -J Extracting Taxa name from ACN
#SBATCH --mail-type=ALL
#SBATCH --mail-user karl.nyren.6523@student.uu.se

ACC_NR_FILE=$1
OUT_NAME=$2
ACC_NR_2_TID_PATH='/sw/data/uppnex/ncbi_taxonomy/latest/accession2taxid/'*
ID_TO_NAME_PATH='/sw/data/uppnex/ncbi_taxonomy/latest/names.dmp'
TMP_file_PATH='/home/karlnyr'
OUT_FILE_PATH='/home/karlnyr/research_trainging_19/blast_queries/genome_hits'


fgrep -w -f $1 $ACC_NR_2_TID_PATH | awk 'F="\t" {print $3}' > $TMP_file_PATH/$OUT_NAME'_tmp.txt'
fgrep -w -f $TMP_file_PATH/$OUT_NAME'_tmp.txt' $ID_TO_NAME_PATH | awk 'F="\t" {print $3}' > $OUT_FILE_PATH/$OUT_NAME
rm $TMP_file_PATH/$OUT_NAME'_tmp.txt'
