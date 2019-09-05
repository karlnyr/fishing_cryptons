import sys


class fasta_sequence:
    '''fasta initializer, used to capture fasta header and sequence'''

    def __init__(self, fasta_header):
        '''initializing fasta format'''
        self.fasta_header = fasta_header
        self.sequence = ''

    def __str__(self):
        '''printing fasta header on call'''
        return f"{self.fasta_header}{self.sequence}"


def main():
    with open(sys.argv[1]) as f:
        line = f.readline()
        while line:
            if sys.argv[2] in line:
                new_seq = fasta_sequence(line)
                line = f.readline()
                while '>' not in line:
                    new_seq.sequence = new_seq.sequence + line
                    line = f.readline()
                temp_seq = list(new_seq.sequence)
                temp_seq[-1] = ''
                new_seq.sequence = "".join(temp_seq)
                print(new_seq)
            else:
                line = f.readline()


main()
