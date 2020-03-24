import sys

'''Used to separate model protein and gene hits from blast 6 formats,
returns only those genomes that has X number of hits in the blast search.
04_handling_blast_out.py <input_file> <out_dir> <out_index>'''


def is_model_protein(accession_nr):
    '''Model protein checker, uses GENBANK accession numbers to verify'''

    # Indexing used on protein model sequences used for blast database
    model_index = ['XM', 'XR', 'XP']

    if any(index in accession_nr for index in model_index):
        return True
    else:
        return False


def main():

    gene_accession_numbers = []

    with open(sys.argv[1], 'r') as in_file, \
            open(f"{sys.argv[2]}{sys.argv[3]}_gene", 'w') as out_file_gene, \
            open(f"{sys.argv[2]}{sys.argv[3]}_model", 'w') as out_file_model, \
            open(f"{sys.argv[2]}{sys.argv[3]}_acn", 'w') as file_acn:
        for line in in_file:
            split_line = line.split('\t')
            if is_model_protein(split_line[1]):
                out_file_model.write(line)
            else:
                out_file_gene.write(line)
                gene_accession_numbers.append(f"{split_line[0]}\t{split_line[1]}\n")
        file_acn.write("".join(gene_accession_numbers))


main()
