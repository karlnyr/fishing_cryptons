import sys
import csv
from Bio import SeqIO


def extract_fasta_headers_to_csv():
    '''put fasta headers into separate csv file. First arg is fasta to extract,
    Second arg is outfile with .csv extension'''
    with open(sys.argv[2], 'w') as csvf:
        filewriter = csv.writer(csvf, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        with open(sys.argv[1], "rU") as handle:
            for record in SeqIO.parse(handle, "fasta"):
                print(record.description.split('\t'))
                filewriter.writerow(record.description.split('\t'))


extract_fasta_headers_to_csv()
