import sys
from functools import reduce
'''Used to separate model protein and gene hits from blast 6 formats,
returns only those genomes that has X number of hits in the blast search.
<script> <input_file> <out_dir> <out_index> <blast_hit_parameter>'''


def is_model_protein(accession_nr):
    '''Model protein checker, uses GENBANK accession numbers to verify'''

    model_index = ['XM', 'XR', 'XP']  # Indexing used on protein model sequences used for blast database

    if any(index in accession_nr for index in model_index):
        return True
    else:
        return False


def compress_accession_nrs(accession_nr_list):
    '''Compress genomes hit of accession numbers, return a list of genomes that had more than 4 hits'''
    temp_dict = {}
    counter = 0
    for acn in accession_nr_list:
        if acn in temp_dict:
            temp_dict[acn] += 1
        else:
            temp_dict[acn] = 1
    count_return_list = []
    return_list = []
    for acn in temp_dict:
        # if temp_dict[acn] > blast_hits:  # Needs X or more hits in blast query
        count_return_list.append(f"{acn}\t{temp_dict[acn]}\n")
        return_list.append(f"{acn}\n")
    return count_return_list, return_list


def main():

    gene_accession_numbers = []
    with open(sys.argv[1], 'r') as in_file, \
            open(f"{sys.argv[2]}{sys.argv[3]}_gene", 'w') as out_file_gene, \
            open(f"{sys.argv[2]}{sys.argv[3]}_model", 'w') as out_file_model, \
            open(f"{sys.argv[2]}{sys.argv[3]}_acn", 'w') as file_acn, \
            open(f"{sys.argv[2]}{sys.argv[3]}_count_list", 'w') as file_acn_count:
        for line in in_file:
            split_line = line.split('\t')
            if is_model_protein(split_line[1]):
                out_file_model.write(line)
            else:
                out_file_gene.write(line)
                gene_accession_numbers.append(f"{split_line[1]}")
        count_list, acn_list = compress_accession_nrs(gene_accession_numbers)
        file_acn.write("".join(acn_list))
        file_acn_count.write("".join(count_list))


main()
