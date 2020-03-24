import sys
'''returns a list of taxa id that meets a blast hit parameter passed to the script.
05_filter_tid_count.py <acn_file> <hit_param>'''


def filter_tid(acn_tid_file, hit_param):
    '''Return the tid of protein sequences with more than X amount of blast
    hits to one and the same taxa'''
    at_list = []
    filtered_list = []
    temp_tid = {}
    return_list = []

    with open(acn_tid_file, 'r') as at_file:
        # Parse file
        for line in at_file:
            at_list.append(line.split('\t'))
        for item in at_list:

            if item[0] in temp_tid:
                try:
                    temp_tid[item[0]][item[2]]['count'] += 1
                except KeyError:
                    temp_tid[item[0]][item[2]] = {}
                    temp_tid[item[0]][item[2]]['count'] = 1
            else:
                temp_tid[item[0]] = {}
                temp_tid[item[0]][item[2]] = {}
                temp_tid[item[0]][item[2]]['count'] = 1

        for protein in temp_tid:
            for t_id in temp_tid[protein]:
                if temp_tid[protein][t_id]['count'] >= int(hit_param):
                    print(f"{temp_tid[protein][t_id]['count']} => {hit_param}")
                    filtered_list.append([protein, t_id.strip()])

        for f_prot in range(len(filtered_list)):
            for a_tid in range(len(at_list)):
                if filtered_list[f_prot][1] == at_list[a_tid][2].strip() and filtered_list[f_prot][0] == at_list[a_tid][0]:
                    at_list[a_tid][2] = at_list[a_tid][2].strip()
                    print("\t".join(at_list[a_tid]))


filter_tid(sys.argv[1], sys.argv[2])
