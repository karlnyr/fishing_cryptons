#!/usr/bin/bash -l

#SBATCH -A snic2018-3-568
#SBATCH -p core
#SBATCH -n 4
#SBATCH -t 00:05:00
#SBATCH -J Extracting_Taxa_name_from_ACN
#SBATCH --mail-type=ALL
#SBATCH --mail-user karl.nyren.6523@student.uu.se

ACC_NR_FILE=$1
OUT_NAME=$2
HIT_PARAM=$3
ACC_NR_2_TID_PATH='/sw/data/uppnex/ncbi_taxonomy/latest/accession2taxid/nucl_gb.accession2taxid'
ID_TO_NAME_PATH='/home/karlnyr/ncbi_taxa_names/sorted_taxa_id-name'
OUT_FILE_PATH='/home/karlnyr/research_training_19/blast_queries/genome_hits'
PY_SCRIPT_PATH='/home/karlnyr/research_training_19/Scripts/06_filter_tid_count.py'
A_T_EXT='_acn_tid'
FILT_EXT='_f_tid'
FILT_A_T='filt_acn_tid'
FILT_BLAST='filtered_blast_hits'

fgrep -w -f $1 $ACC_NR_2_TID_PATH | \
    awk -F "\t" '{print $2"\t"$3}' > $OUT_FILE_PATH/$OUT_NAME$A_T_EXT

python3 $PY_SCRIPT_PATH $OUT_FILE_PATH/$OUT_NAME$A_T_EXT $3 \
    > $OUT_FILE_PATH/$OUT_NAME$FILT_EXT

join -t $'\t' \
    -1 1 -2 2 \
    -o 1.1,2.1 \
    <(sort -k1 $OUT_FILE_PATH/$OUT_NAME$FILT_EXT) \
    <(sort -k2 $OUT_FILE_PATH/$OUT_NAME$A_T_EXT) \
    > $OUT_FILE_PATH/$OUT_NAME$FILT_A_T

rm $OUT_FILE_PATH/$OUT_NAME$FILT_EXT

join -t $'\t' \
    -1 1 -2 1 \
    -o 1.1,1.2,2.1 \
    $OUT_FILE_PATH/$OUT_NAME$FILT_A_T \
    $ID_TO_NAME_PATH | \
    sort -n -k1 \
    > $OUT_FILE_PATH/$OUT_NAME$FILT_BLAST
