import sys


def separating_models_and_genome():
    '''Used to separate the protein models and genetic sequences found in a blast.
    Requires blast 6 format to work'''

    out_file_gene = open(sys.argv[2], w)
    out_file_model = open(sys.argv[3], w)
    # model_RefSeq = []
    # genetic_RefSeq = []
    model_index = ['XM', 'XR', 'XP']  # Indexing used on protein model sequences used for blast database

    with open(sys.argv[1]) as file:
        for line in file:
            split_line = line.split('\t')
            for index in model_index:
                if index in split_line[1]:
                    out_file_model.write(line)
                    # model_RefSeq.append(line)
                else:
                    out_file_gene.write(line)
                    # genetic_RefSeq.append(line)


separating_models_and_genome()
