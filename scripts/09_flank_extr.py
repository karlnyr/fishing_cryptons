import sys
import subprocess as sp


class blast_line:
    '''intented to store specifics on blast entries. Information on protein,
    ACN and ranges are stored'''

    def __init__(self, protein, acn, min_range, max_range):
        '''Initializing blast entry'''
        self.protein = protein
        self.acn = acn
        self.min_range = int(min_range)
        self.max_range = int(max_range)
        self.reveresed = check_reversed(min_range, max_range)


class fasta_seq:
    '''used to keep track of fasta length and name'''

    def __init__(self, name, sequence):
        '''initialize fasta_seq'''
        self.name = name
        self.sequence = seq
        self.length = len(str(self.seq))


def index_fasta(fasta_file):
    '''Indexing fasta file for iterative searching,
    returns a dictionary that can be used to specify start
    positions in the file'''

    fasta_index = {}
    with open(fasta_file, 'r') as ff:
        line_pos = 0
        line = ff.readline()
        start_flag = 0
        while line:
            if start_flag == 1:
                line_pos -= len(line)
            if '>' in line:
                start_flag = 1
                scaffold = line.strip().replace('>', '')
                # Assign position of sequence start
                line_pos += len(line)
                start_index = line_pos

                line = ff.readline()
                line_pos += len(line)
                seq_line_counter = 1

                while '>' not in line and line:
                    line = ff.readline()
                    line_pos += len(line)
                    seq_line_counter += 1

                fasta_index[scaffold] = start_index
            elif '>' not in line:
                start_flag = 1
                line = ff.readline()
                line_pos += len(line)
    return fasta_index


def check_reversed(min_range, max_range):
    '''checks if the hit is made in reverse or in forward orientation'''

    if (int(min_range) - int(max_range) > 0):
        return True
    else:
        return False


def set_ranges(fasta_seq, blast_entry, kb_flanks):
    '''set the size to be extracted from the sequences, given by the kb size'''

    flanks = int(kb_flanks) * 1000
    minimum = 0
    maximum = 0

    if (blast_entry.min_range - flanks - 1 >= 0):
        minimum = (blast_entry.min_range - flanks) - 1
    else:
        minimum = 0
    if (sequence.length <= blast_entry.max_range + flanks):
        maximum = blast_entry.max_range + flanks - 1
    else:
        maximum = sequence.length - 1
    return minimum, maximum


def extract_substring(fasta_seq, blast_entry, kb_flanks):
    '''Extract a subtring from a longer string, by given kb size'''
    minimum, maximum = set_ranges(fasta_seq, blast_entry, kb_flanks)
    if blast_entry.reveresed:
        substring = fasta_seq.seq[(minimum - 1):maximum]
        reverse_string = substring[::-1]
        return fasta_seq(f"{blast_entry.protein}_{fasta_seq.name}_{minimum}-{maximum}", reverse_string)
    else:
        substring = fasta_seq.seq[(minimum - 1):maximum]
        return fasta_seq(f"{blast_entry.protein}_{fasta_seq.name}_{minimum}-{maximum}", substring)


def main(fasta_file, blast_file, outdir, kb_flanks):

    # Gather all blast sequences
    blast_entries = []
    # Indexing fasta file
    fasta_indices = index_fasta(fasta_file)

    # Parse blast file
    with open(blast_file, 'r') as bf:
        for entry in bf:
            line = entry.split('\t')
            bl_entry = blast_line(line[0], line[1], line[8], line[9])
            blast_entries.append(bl_entry)

    # Group entries by ACN
    blast_entry_dict = {}

    for blast_entry in blast_entries:
        try:
            blast_entry_dict[blast_entry.acn].append(blast_entry)
        except KeyError:
            blast_entry_dict[blast_entry.acn] = []
            blast_entry_dict[blast_entry.acn].append(blast_entry)

    # Extract sequences by their scaffolds
    out_list = []
    for acn in blast_entry_dict:
        if acn in fasta_indices:
            print(acn)
        scaffold = ''
    #     with open(fasta_file) as ff:
    #         indices = ''
    #         try:
    #             indices = fasta_indices[acn]
    #         except KeyError:
    #             print(f"could not find scaffold {acn} in {fasta_file}")
    #             pass
    #         ff.seek(indices, 0)
    #         tmp_seq = ff.readline()
    #         seq = ''
    #         while '>' not in tmp_seq and tmp_seq:
    #             seq += tmp_seq.strip()
    #             tmp_seq.readline()
    #         scaffold = fasta_seq(acn, seq)

    #         for blast_entry in blast_entry_dict[acn]:
    #             extr_seq = extract_substring(scaffold, blast_entry, kb_flanks)
    #             out_list.append(extr_seq)

    # file_name = sp.run(['basename', blast_file], capture_output=True, text=True)
    # with open(f"{outdir}/{file_name}_flanks_{kb_flanks}", 'w') as out_f:
    #     for entry in out_list:
    #         out_f.write(f"{entry.name}\n{entry.seq}")


main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
