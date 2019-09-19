import sys
import csv
import pandas as pd
'''Extract taxa that is not existing in the repbase database'''

with open(sys.argv[1]) as rep_f, \
        open(sys.argv[2]) as blast_h:
    rb = pd.read_csv(rep_f, delimiter=',', names=['name', 'class', 'discovered_in'])
    bh = []
    # For some reason the format is wonky on the join, here fixing that here
    for line in blast_h:
        bh.append([f"{line.split()[0]}", f"{line.split()[1]}", f"{line.split()[2]} {line.split()[3]}"])
    hit_count = len(rb)
    for filt_hit in bh:
        loop_c = 0
        flag = 0
        while flag == 0 and loop_c <= hit_count:
            for row in rb:
                if filt_hit[2] == row['discovered in'] and filt_hit[0]:
                    print(f"{filt_hit[2]} = {species}")
                    flag = 1
                    loop_c += 1
                elif filt_hit[2] != species:
                    print(f"{filt_hit[2]} != {species}")
                    loop_c += 1

            # if filt_hit[2] not in rb['discovered_in']:
            #     pass
            # elif filt_hit[2] in rb['discovered_in']:
            #     print('already found')
