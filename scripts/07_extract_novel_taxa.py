import sys
'''Extract taxa that is not existing in the repbase database
python3 <script> <repbase_path> <blast_path> <fmt_6_path> <out_path>'''


def novel_taxa(repbase_file, blast_file, fmt_6, out_file):
    with open(repbase_file, 'r') as rep_f, \
            open(blast_file, 'r') as blast_h, \
            open(fmt_6, 'r') as fmt6, \
            open(f"{out_file}_filt_fmt6", 'w') as out_f, \
            open(f"{out_file}_filt_fmt6_report", 'w') as out_r:

        # init lists
        discovered_r = []
        novel_r = []
        novel_list = []
        rb = []
        bh = []
        f6 = []
        extr_f6 = []
        # counters for novel or discovered, flag for undiscovered
        discovered = 0
        novel = 0
        flag = 0

        # Parse files
        for line in blast_h:
            bh.append(line.strip().split('\t'))
        for line in rep_f:
            rb.append(line.strip().split(','))
        for line in fmt6:
            f6.append(line.strip().split('\t'))

        # Go through to find if combo of prot and taxa exists already
        for blast_hit in range(len(bh)):
            for entry in range(len(rb)):
                if rb[entry][0] in bh[blast_hit][0] and bh[blast_hit][2].lower() == rb[entry][2].lower():
                    discovered_r.append(f"{bh[blast_hit][0]}\t{bh[blast_hit][1]}\t{bh[blast_hit][2]}\n")
                    discovered += 1
                    flag = 1
            if flag == 0:
                novel_r.append(f"{bh[blast_hit][0]}\t{bh[blast_hit][1]}\t{bh[blast_hit][2]}\n")
                novel_list.append([bh[blast_hit][0], bh[blast_hit][1], bh[blast_hit][2]])
                novel += 1

        out_r.write(f'Novel: {novel}\n{"".join(novel_r)}Already discovered: {discovered}\n{"".join(discovered_r)}')

        # Extract only novel blast hits.
        for entry in range(len(novel_list)):
            for hit in range(len(f6)):
                if novel_list[entry][0] == f6[hit][0] and novel_list[entry][1] == f6[hit][1]:
                    f6[hit].append(novel_list[entry][2])
                    extr_f6.append(f6[hit])

        for line in extr_f6:
            temp_line = "\t".join(line)
            out_f.write(f"{temp_line}\n")


novel_taxa(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
