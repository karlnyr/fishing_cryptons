#!/usr/bin/bash -l

#SBATCH -A snic2018-3-568
#SBATCH -p core
#SBATCH -n 4
#SBATCH -t 00:30:00
#SBATCH -J Extracting_Taxa_name_from_ACN
#SBATCH --mail-type=ALL
#SBATCH --mail-user karl.nyren.6523@student.uu.se

ACN_FILE=$1
OUT_NAME=$2
HIT_PARAM=$3
ACC_NR_2_TID_PATH='/home/karlnyr/ncbi_taxa/accession2taxid'
ID_TO_NAME_PATH='/home/karlnyr/ncbi_taxa/sorted_taxa_id-name'
OUT_FILE_PATH='/home/karlnyr/research_training_19/blast_queries/genome_hits'
PY_SCRIPT_PATH='/home/karlnyr/research_training_19/scripts/05_filter_tid_count.py'
A_T_EXT='_acn_tid'
FILT_EXT='h'$HIT_PARAM'_f_tid'
FILT_A_T='h'$HIT_PARAM'_filt_acn_tid'
FILT_BLAST='h'$HIT_PARAM'_filtered_blast_hits'

echo "1 - Initiate ACN to TID search"
join -t $'\t' \
    -1 2 -2 2 \
    -o 1.1,1.2,2.3 \
    <(sort -t $'\t' -k2,2 $1) \
    <(sort -t $'\t' -k2,2 $ACC_NR_2_TID_PATH) \
    > $OUT_FILE_PATH/$OUT_NAME$A_T_EXT
echo "1 - Done"

echo "2 - Initiate blast hit filtering(python), fetching sequences with more than "$HIT_PARAM" hits to the same taxa"
python3 $PY_SCRIPT_PATH $OUT_FILE_PATH/$OUT_NAME$A_T_EXT $3 \
    > $OUT_FILE_PATH/$OUT_NAME$FILT_EXT
echo "2 - Done"

echo "3 - Initiate blast hit filtering(shell), fetching these proteins from all sequences matched"
join -t $'\t' \
    -1 2 -2 1 \
    -o 2.1,2.2,2.3 \
    <(sort -t $'\t' -k2 $OUT_FILE_PATH/$OUT_NAME$FILT_EXT) \
    <(sort -t $'\t' -k1 $OUT_FILE_PATH/$OUT_NAME$A_T_EXT) \
    > $OUT_FILE_PATH/$OUT_NAME$FILT_A_T
echo "3 - Done"

echo "4 - Initate final join on taxa id to taxa name"
join -t $'\t' \
    -1 3 -2 1 \
    -o 1.1,1.2,1.3,2.2 \
    <(sort -t $'\t' -k3 $OUT_FILE_PATH/$OUT_NAME$FILT_A_T) \
    <(sort -t $'\t' -k1,1 $ID_TO_NAME_PATH) \
    > $OUT_FILE_PATH/$OUT_NAME$FILT_BLAST
echo "4 - Done"
