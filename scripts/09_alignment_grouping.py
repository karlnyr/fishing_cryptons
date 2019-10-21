import sys
import os
import subprocess as sp
from Bio import SeqIO
from Bio.Blast.Applications import NcbiblastnCommandline
from collections import defaultdict

'''Will group alignment entries by their percentage identity. Returns a report of
what sequences are to be grouped together by the user percentage cut of.
python3 <script.py> <input_file.fasta> <percentage_id_cutof> <minimum_alignment_length'''

current_wd = os.getcwd()


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


def parse_n_blastn(fasta_file, cwd):
    '''Used to parse the alignment fasta file, removing any "-" occured in the
    alignment and creates an database to be used in the blastn'''
    seq_handle = SeqIO.parse(fasta_file, 'fasta')
    with open(f'{fasta_file}_1_tmp', 'w') as temp_f1:
        for record in seq_handle:
            if 'Ambiguous_orientation' in record.name:
                record.name = record.name.replace('Ambiguous_orientation', 'A_O')
            temp_f1.write(f'>{record.name}\n{str(record.seq).replace("-","")}\n')
            sp.run(f'cp {current_wd}/{fasta_file}_1_tmp {current_wd}/{fasta_file}_2_tmp', shell=True)

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
    if name_set & blast_hit.tuple_set():
        return True
    else:
        return False


def filter_blast(aln, shortest_aln_allowed, perc_id_cutof):
    '''Filter blast output, will return a non-redundant list where length is '''
    out_list = []
    list_init = 0
    for alignment in aln:
        split_aln = alignment.split('\t')
        blast_item = blast_hit(split_aln[0], split_aln[1], split_aln[2], split_aln[3])
        if seq_check(blast_item, shortest_aln_allowed, perc_id_cutof):
            if not list_init:
                out_list.append(blast_item)
                list_init = 1
            elif list_init:
                for app_item in out_list:
                    if not same_sequences(blast_item, app_item):
                        out_list.append(blast_item)
                    else:
                        if blast_item.length > app_item.length:
                            app_item = blast_item
    return out_list


def messy_clustering(bh_list):
    '''Loop over a list of blast hit object, group them together as long as there are combinations to do'''
    not_changing = False
    out_list = []
    print('starting messy cluster')
    while not not_changing:
        not_changing = True
        list_init = 0
        for bh_item in bh_list:
            if not list_init:
                out_list.append(bh_item.tuple_set())
                not_changing = False
                list_init = 1
            elif list_init:
                for item_set in out_list:
                    if id_match(item_set, bh_item):
                        item_set = item_set | bh_item.tuple_set()
                        not_changing = False

        inner_list_changing = False
        scrambled_list = []
        while not inner_list_changing:
            inner_list_changing = True
            for i in range(len(out_list)):
                working_set = {}
                for j in range(len(out_list)):
                    if out_list[i] != out_list[j]:
                        if out_list[i] & out_list[j]:
                            working_set = working_set | out_list[i] | out_list[j]
                if not len(scrambled_list):
                    scrambled_list.append(working_set)
                    inner_list_changing = False
                else:
                    for item in scrambled_list:
                        if item != working_set and item & working_set:
                            item = item | working_set
                            inner_list_changing = False
                        elif item != working_set:
                            scrambled_list.append(working_set)
                            inner_list_changing = False

        out_list = scrambled_list

    return out_list


def main(alignment_file, perc_id_cutof, shortest_aln_allowed):
    aln = parse_n_blastn(alignment_file, current_wd)
    filtered_aln = filter_blast(aln, shortest_aln_allowed, perc_id_cutof)
    output = messy_clustering(filter_blast)
    print(output)


main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
