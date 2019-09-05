#!/usr/bin/bash -l

#SBATCH -A snic2018-3-568
#SBATCH -p core
#SBATCH -n 4
#SBATCH -t 01:30:00
#SBATCH -J noniterative_tblastn_nt
#SBATCH --mail-type=ALL
#SBATCH --mail-user karl.nyren.6523@student.uu.se

module load bioinfo-tools
module load blast/2.7.1+

IN_FILE_PATH='/home/karlnyr/research_training_19/crypton_sequences/consensus_sequences/'$1
OUT_FILE_PATH='/home/karlnyr/research_training_19/blast_queries'
ADD_DATE=`date +%d%m%y`
OUT_NAME=$1$ADD_DATE
XML_EXT='.xml'
FMT_6_EXT='_fmt6'

# Database used: nt - almost non-redundant database
# $FMT Needs to be passed from sbatach format

if [[ $2 = '6' ]];
    then
    for file in $IN_FILE_PATH;
        do
            tblastn -db nt \
            -query $file \
            -outfmt $FMT \
            -num_threads 4 \
            -out $OUT_FILE_PATH/$OUT_NAME$FMT_6_EXT
    done
elif [[ $2 = '5' ]];
    then
    for file in $IN_FILE_PATH;
        do
            tblastn -db nt \
            -query $file \
            -outfmt $FMT \
            -num_threads 4 \
            -out $OUT_FILE_PATH/$OUT_NAME$XML_EXT
    done
else
    echo 'No valid outformat was provided, try sbatch <script> <filename> <format>'
fi

