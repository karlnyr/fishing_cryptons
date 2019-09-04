import Bio
import sys
from Bio.Blast import NCBIXML

with open(sys.argv[1]) as file:
    blast_records = NCBIXML.parse(file)

    for record in blast_records:
        for alignment in blast_records.alignment:
            for hsp in alignment.hsps:
                print(hsp.query)
                print(hsp.match)
                print(hsp.match)
