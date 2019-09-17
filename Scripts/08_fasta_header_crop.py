import sys
'''If fasta header is separated by blankspaces this script will take out
the acn and abbreviate into new file.'''

with open(sys.argv[1], 'r') as input_f, \
        open(sys.argv[2], 'w') as out_f:
    new_line = input_f.readline()
    while new_line:
        if '>' in new_line:
            cropped_head = f"{new_line.strip().split(' ')[0]}\n"
            out_f.write(cropped_head)
            new_line = input_f.readline()
            while '>' not in new_line and new_line:
                out_f.write(f"{new_line.strip()}\n")
                new_line = input_f.readline()
        else:
            new_line = input_f.readline()

    print("\nCropped!\n")
