#!/usr/bin/bash -l

#SBATCH -A snic2018-3-568
#SBATCH -p core
#SBATCH -n 4
#SBATCH -t 00:30:00
#SBATCH -J alignment_clustering

module load bioinfo-tools
module load biopython/1.73-py3
module load blast/2.9.0+

SCRIPT_PATH='/home/karlnyr/research_training_19/scripts/09_alignment_grouping.py'
FILE_PATH='/home/karlnyr/research_training_19/alignments/*/02/*'
PERC_CUTOF=$2
MIN_LENGTH=$3

for file in $FILE_PATH;
    do
        python3 $SCRIPT_PATH $file $PERC_CUTOF $MIN_LENGTH \
        > $file'_clustering'
done
