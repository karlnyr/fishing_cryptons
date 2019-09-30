import sys
'''returns a list of taxa id that meets a blast hit parameter passed to the script.
script.py <acn_file> <hit_param>'''


def filter_tid(acn_tid_file, hit_param):
    '''Return the tid of protein sequences with more than X amount of blast
    hits to one and the same taxa'''
    at_list = []
    filtered_list = []
    temp_tid = {}

    with open(acn_tid_file, 'r') as at_file:
        for line in at_file:
            at_list.append(line.split('\t'))
        for item in at_list:
            if item[2] in temp_tid:
                try:
                    temp_tid[item[2]][item[0]]['count'] += 1
                except KeyError:
                    temp_tid[item[2]][item[0]] = {}
                    temp_tid[item[2]][item[0]]['count'] = 1
            else:
                temp_tid[item[2]] = {}
                temp_tid[item[2]][item[0]] = {}
                temp_tid[item[2]][item[0]]['count'] = 1
        for t_id in temp_tid:
            for protein in temp_tid[t_id]:
                if temp_tid[t_id][protein]['count'] >= int(hit_param):
                    filtered_list.append([t_id.strip(), protein])
        for f_tid in range(len(filtered_list)):
            for a_tid in range(len(at_list)):
                if filtered_list[f_tid][0].strip() == at_list[a_tid][2].strip():
                    at_list[a_tid][2] = at_list[a_tid][2].strip()
                    print("\t".join(at_list[a_tid]))


filter_tid(sys.argv[1], sys.argv[2])
