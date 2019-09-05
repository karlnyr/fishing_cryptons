import sys
from functools import reduce
'''Used to separate model protein and gene hits from blast 6 formats.
<script> <input_file> <out_gene> <out_model> <gene_accession_nrs>'''


def is_model_protein(accession_nr):
    '''Model protein checker, uses GENBANK accession numbers to verify'''

    model_index = ['XM', 'XR', 'XP']  # Indexing used on protein model sequences used for blast database

    if any(index in accession_nr for index in model_index):
        return True
    else:
        return False

########################## WORK IN PROGRESSSS ########################################
def make_tuple(x):
    '''make tuples for mapping'''
    return (1, x)


def do_sum(touple1, touple2):
    '''sum two integers if second tuple matches'''
    if touple1[1] == touple2[1]:
        return(touple1[0] + touple1[0], v)


def compress_accession_nrs(accession_nr_list):

    temp_list = []
    mapped_list = map(make_tuple, accession_nr_list)
    reduced_list = reduce(do_sum, mapped_list)

########################## WORK IN PROGRESSSS ########################################

def main():
    try:
        out_file_gene = open(sys.argv[2], 'w')
        out_file_model = open(sys.argv[3], 'w')
        # gene_accession_numbers = open(sys.argv[4], 'w')
    except:
        print("Not enought arguments supplied")
    gene_accession_numbers = []
    with open(sys.argv[1]) as file:
        for line in file:
            split_line = line.split('\t')
            if is_model_protein(split_line[1]):
                out_file_model.write(line)
            else:
                out_file_gene.write(line)
                # gene_accession_numbers.write(f"{split_line[1]}\n")
                gene_accession_numbers.append(f"{split_line[1]}\n")


main()
