import sys


def main():
    model_RefSeq = []
    genetic_RefSeq = []
    with open(sys.argv[1]) as file:
        for line in file:
            split_line = line.split('\t')
            if ['XM', 'XR', 'XP'] in split_line[1]:
                model_RefSeq.append(line)
            else:
                genetic_RefSeq.append(line)
    return model_RefSeq genetic_RefSeq


main()
