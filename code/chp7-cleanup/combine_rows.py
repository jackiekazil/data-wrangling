from csv import DictReader

mn_data_rdr = DictReader(open('../../data/unicef/mn.csv', 'rb'))
mn_data = [d for d in mn_data_rdr]


def combine_data_dict(data_rows):
    data_dict = {}
    for row in data_rows:
        key = '%s-%s' % (row.get('HH1'), row.get('HH2'))
        if key in data_dict.keys():
            data_dict[key].append(row)
        else:
            data_dict[key] = [row]
    return data_dict

mn_dict = combine_data_dict(mn_data)

print len(mn_dict)
