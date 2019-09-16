import sys
'''returns a list of taxa id that meets a blast hit parameter passed to the script.
script.py <taxa_ids> <acn_counts> <hit_param>'''


def filter_tid(acn_tid_file, hit_param):
    '''Return the tid of those with X amount of blast hits'''
    temp_list = []
    return_list = []
    temp_tid = {}

    with open(acn_tid_file, 'r') as at_file:
        for line in at_file:
            temp_list.append(line.split('\t'))

    for item in temp_list:
        if item[1] in temp_tid:
            temp_tid[item[1]]['count'] += 1
            temp_tid[item[1]]['acn'].append(item[0])
        else:
            temp_tid[item[1]] = {'count': 1, 'acn': [item[0]]}

    for t_id in temp_tid:
        if int(temp_tid[t_id]['count']) > int(hit_param):
            return_list.append(t_id)

    return_list[-1] = return_list[-1].strip('\n')
    return "".join(return_list)


print(filter_tid(sys.argv[1], sys.argv[2]))
