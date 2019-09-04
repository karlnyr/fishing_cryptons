#!/usr/bin/bash -l

#SBATCH -A snic2018-3-568
#SBATCH -p core
#SBATCH -n 4
#SBATCH -t 01:00:00
#SBATCH -J noniterative_tblastn_nt
#SBATCH --mail-type=ALL
#SBATCH --mail-user karl.nyren.6523@student.uu.se

module load bioinfo-tools
module load blast/2.7.1+

IN_FILE_PATH='/home/karlnyr/research_training_19/crypton_sequences/consensus_sequences/kirc.fasta'
OUT_FILE_PATH='/home/karlnyr/research_training_19/blast_queries'
OUT_NAME='kirc_tblastn_020919.xml'

# Database used: nt - almost non-redundant database
for file in $IN_FILE_PATH;
    do
        tblastn -db nt \
        -query $file \
        -outfmt 5 \
        -num_threads 4 \
        -out $OUT_FILE_PATH/$OUT_NAME
done
