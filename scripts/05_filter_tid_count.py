import sys
'''returns a list of taxa id that meets a blast hit parameter passed to the script.
script.py <acn_file> <hit_param>'''


def filter_tid(acn_tid_file, hit_param):
    '''Return the tid of protein sequences with more than X amount of blast
    hits to one and the same taxa'''
    temp_list = []
    return_list = []
    temp_tid = {}

    with open(acn_tid_file, 'r') as at_file:
        for line in at_file:
            temp_list.append(line.split('\t'))
    for item in temp_list:
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
                return_list.append(f"{t_id.strip()}\t{protein}\n")

    try:
        return_list[-1] = return_list[-1].strip('\n')
        return "".join(return_list)
    except IndexError:
        return None


print(filter_tid(sys.argv[1], sys.argv[2]))