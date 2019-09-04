#!/usr/bin/bash -l

#SBATCH -A snic2018-3-568
#SBATCH -p core
#SBATCH -n 4
#SBATCH -t 00:10:00
#SBATCH -J noniterative_tblastn_nt
#SBATCH --mail-type=ALL
#SBATCH --mail-user karl.nyren.6523@student.uu.se

module load bioinfo-tools
module load blast/2.7.1+

IN_FILE_PATH='/home/karlnyr/research_training_19/crypton_sequences/kirc.fasta'
OUT_FILE_PATH='/home/karlnyr/research_training_19/blast_queries'
OUT_NAME='kirc_tblastn_020919'

# Database used: nt - almost non-redundant database
for file in $IN_FILE_PATH;
    do
        command tblastn -db /sw/data/uppnex/blast_databases/nt -query $file -outfmt 6 -out $OUT_FILE_PATH/$OUT_NAME
done
