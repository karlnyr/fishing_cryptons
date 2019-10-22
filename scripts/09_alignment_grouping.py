import sys
import os
import subprocess as sp
from Bio import SeqIO
from Bio.Blast.Applications import NcbiblastnCommandline
from collections import defaultdict

'''Will group alignment entries by their percentage identity. Returns a report of
what sequences are to be grouped together by the user percentage cut of.
python3 <script.py> <input_file.fasta> <percentage_id_cutof> <minimum_alignment_length>'''


class blast_hit():
    '''Class to handle the blast outputs regarding the parameters in question'''

    def __init__(self, query, subject, perc_id, length):
        '''Initializing blast_hit object'''
        self.query = query
        self.subject = subject
        self.perc_id = float(perc_id)
        self.length = int(length)

    def tuple_set(self):
        '''Returns a touple made from query and subject in blast_hit object'''
        return {self.query, self.subject}

    def __str__(self):
        return f"{self.query}-{self.subject}: {self.length}"


def parse_n_blastn(fasta_file):
    '''Used to parse the alignment fasta file, removing any "-" occured in the
    alignment and creates an database to be used in the blastn'''
    seq_handle = SeqIO.parse(fasta_file, 'fasta')
    with open(f'{fasta_file}_1_tmp', 'w') as temp_f1:
        for record in seq_handle:
            if 'Ambiguous_orientation' in record.name:
                record.name = record.name.replace('Ambiguous_orientation', 'A_O')
            temp_f1.write(f'>{record.name}\n{str(record.seq).replace("-","")}\n')
            sp.run(f'cp {fasta_file}_1_tmp {fasta_file}_2_tmp', shell=True)

    sp.run(f'makeblastdb -in {fasta_file}_1_tmp -dbtype nucl -parse_seqids -blastdb_version 5', shell=True)
    print("\n------Temporary database set up------\n")
    # Running blastn
    blastn_cline = NcbiblastnCommandline(query=f"{fasta_file}_2_tmp", db=f"{fasta_file}_1_tmp", outfmt=6)
    aln = blastn_cline()[0].split('\n')
    del aln[-1]
    sp.run(f'rm {fasta_file}_*_tmp*', shell=True)
    print("------BLASTn done. Removing tmp files and database------\n")

    return aln


def same_sequences(bh_1, bh_2):
    '''Takes two blast_hit objects and checks if they are ambiguous,
    meaning that they are done on the same protein'''
    if bh_1.query == bh_2.query and bh_1.subject == bh_2.subject:
        return True
    elif bh_1.query == bh_2.subject and bh_1.subject == bh_2.query:
        return True
    else:
        False


def seq_check(blast_hit, shortest_aln_allowed, perc_id_cutof):
    '''return true or fasle if statements are correct'''
    if blast_hit.length >= shortest_aln_allowed and blast_hit.query != blast_hit.subject and blast_hit.perc_id >= perc_id_cutof:
        return True
    else:
        return False


def id_match(name_set, blast_hit):
    '''Checks if any id in query or subject matches between two blast_hit objects'''
    if name_set & blast_hit:
        return True
    else:
        return False


def filter_blast(aln, shortest_aln_allowed, perc_id_cutof):
    '''Filter blast output, will return a non-redundant list where length is '''
    working_list = []
    list_init = 0
    for alignment in aln:
        split_aln = alignment.split('\t')
        blast_item = blast_hit(split_aln[0], split_aln[1], split_aln[2], split_aln[3])
        if seq_check(blast_item, shortest_aln_allowed, perc_id_cutof):
            if not list_init:
                working_list.append(blast_item)
                list_init = 1
            elif list_init:
                exist = 0
                indx = 0
                for i in range(len(working_list)):
                    if blast_item.tuple_set() == working_list[i].tuple_set():
                        exist = 1
                        indx = i
                if exist and blast_item.length > working_list[i].length:
                    working_list.pop(indx)
                    working_list.insert(indx, blast_item)
                else:
                    working_list.append(blast_item)

    out_list = []
    for item in working_list:
        out_list.append(item.tuple_set())
    return out_list


def messy_clustering(bh_list):
    '''Loop over a list of blast hit object, group them together as long as there are combinations to do'''
    changing = False
    out_list = []
    list_init = 0
    counter = 1
    while not changing:
        changing = True
        before = len(out_list)
        if not list_init:
            for bh_item in bh_list:
                if not list_init:
                    out_list.append(bh_item)
                    list_init = 1
                elif list_init:
                    for i in range(len(out_list)):
                        if out_list[i] & bh_item:
                            union = out_list[i] | bh_item
                            out_list.pop(i)
                            out_list.insert(i, union)
                        else:
                            out_list.append(bh_item)
        elif list_init:
            working_list = []
            for item in out_list:
                if not len(working_list):
                    working_list.append(item)
                else:
                    a_match = 0
                    for i in range(len(working_list)):
                        if working_list[i] & item:
                            union = working_list[i] | item
                            working_list.pop(i)
                            working_list.insert(i, union)
                            a_match = 1
                    if not a_match:
                        working_list.append(item)
            out_list = working_list
        after = len(out_list)

        if after == before:
            for i in range(after):
                if working_list[i] != out_list[i]:
                    changing = False
        elif after != before:
            changing = False
    return out_list


def main(alignment_file, perc_id_cutof, shortest_aln_allowed):
    aln = parse_n_blastn(alignment_file)
    filtered_aln = filter_blast(aln, shortest_aln_allowed, perc_id_cutof)
    output = messy_clustering(filtered_aln)
    cluster_count = 1
    print(f'The following clusters was identified with {perc_id_cutof}% identity and minimum alignment length of {shortest_aln_allowed}')
    for item in output:
        tmp = list(item)
        if len(tmp) >= 3:
            print(f"cluster {cluster_count}:")
            for i in tmp:
                print(i)
            cluster_count += 1


main(sys.argv[1], float(sys.argv[2]), int(sys.argv[3]))
