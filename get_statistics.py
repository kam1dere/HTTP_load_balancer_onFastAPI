def finally_statistic(file_name):
    file_logs = open(file_name, 'r')
    final_count = {'web_1': 0,
                   'web_2': 0,
                   'web_3': 0,
                   'web_4': 0,
                   'web_5': 0,
                   'web_6': 0, }
    for line in file_logs:
        if line[0:5] in final_count:
            final_count[(line[0:5])] += 1
    file_logs.close()
    return final_count


print(finally_statistic('webs_ok.txt'))
