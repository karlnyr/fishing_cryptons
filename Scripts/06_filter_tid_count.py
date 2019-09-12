import sys
'''returns a list of taxa id that meets a blast hit parameter passed to the script.
script.py <taxa_ids> <acn_counts> <hit_param>'''


def compress_files(taxa_id_file, acn_count_file):
    '''combines the two files into one list'''
    with open(taxa_id_file, 'r') as t_ids, \
            open(acn_count_file, 'r') as acn_count:
        compiled_list = []
        for line in acn_count:
            compiled_list.append(line.split('\t'))
        row_count = 0
        for line in t_ids:
            compiled_list[row_count].append(line)
            row_count += 1
        return compiled_list


def filter_tid(acn_tid_list, hit_param):
    '''Return the tid of those with X amount of blast hits'''
    temp_tid = {}
    for item in acn_tid_list:
        if item[1] in temp_tid:
            temp_tid[item[2]] += item[1]
        else:
            temp_tid[item[2]] = item[1]
    return_list = []
    for t_id in temp_tid:
        if temp_tid[t_id] > hit_param:
            return_list.append(t_id)
    return "".join(return_list)


def main(taxa_id_file, acn_counts, hit_param):
    print(
        filter_tid(
            compress_files(taxa_id_file, acn_counts),
            hit_param))


main(sys.argv[1], sys.argv[2], sys.argv[3])
