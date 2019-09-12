#!/usr/bin/bash -l

#SBATCH -A snic2018-3-568
#SBATCH -p core
#SBATCH -n 4
#SBATCH -t 00:30:00
#SBATCH -J Extracting_Taxa_name_from_ACN
#SBATCH --mail-type=ALL
#SBATCH --mail-user karl.nyren.6523@student.uu.se

ACC_NR_FILE=$1
OUT_NAME=$2
ACC_COUNT_FILE=$3
HIT_PARAM=$4
ACC_NR_2_TID_PATH='/sw/data/uppnex/ncbi_taxonomy/latest/accession2taxid/nucl_gb.accession2taxid'
ID_TO_NAME_PATH='/sw/data/uppnex/ncbi_taxonomy/latest/names.dmp'
OUT_FILE_PATH='/home/karlnyr/research_training_19/blast_queries/genome_hits'
PY_SCRIPT_PATH='/home/karlnyr/research_training_19/Scripts/06_filder_tid_count.py'

fgrep -w -f $1 $ACC_NR_2_TID_PATH | awk -F "\t" '{print $3}' > $OUT_FILE_PATH/$OUT_NAME'_tid.txt'
python3 $PY_SCRIPT_PATH $OUT_FILE_PATH/$OUT_NAME'_tid.txt' $3 $4 > $OUT_FILE_PATH/$OUT_NAME'_filtered_tid.txt'
fgrep -w -f $OUT_FILE_PATH/$OUT_NAME'_filtered_tid.txt' $ID_TO_NAME_PATH | awk -F "|" '$4~/scientific name/ {print $2}' > $OUT_FILE_PATH/$OUT_NAME

