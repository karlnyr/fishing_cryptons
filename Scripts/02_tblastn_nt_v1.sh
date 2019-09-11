#!/usr/bin/bash -l

#SBATCH -A snic2018-3-568
#SBATCH -p core
#SBATCH -n 4
#SBATCH -t 16:00:00
#SBATCH -J tblastn nt fmt 6 or 5
#SBATCH --mail-type=ALL
#SBATCH --mail-user karl.nyren.6523@student.uu.se

module load bioinfo-tools
module load blast/2.7.1+

IN_FILE_PATH=$1
OUT_FILE_PATH='/home/karlnyr/research_training_19/blast_queries'
ADD_DATE=`date +%d%m%y`
OUT_NAME=$2'_'$ADD_DATE
XML_EXT='.xml'
FMT_6_EXT='_fmt6'

# Database used: nt - almost non-redundant database
# $FMT Needs to be passed from sbatach format

if [[ $3 = '6' ]];
    then
    for file in $IN_FILE_PATH;
        do
            tblastn -db nt \
            -query $file \
            -outfmt $3 \
            -num_threads 4 \
            -out $OUT_FILE_PATH/$OUT_NAME$FMT_6_EXT
    done
elif [[ $3 = '5' ]];
    then
    for file in $IN_FILE_PATH;
        do
            tblastn -db nt \
            -query $file \
            -outfmt $3 \
            -num_threads 4 \
            -out $OUT_FILE_PATH/$OUT_NAME$XML_EXT
    done
fi

