from csv import DictReader

data_rdr = DictReader(open('../../data/unicef/mn.csv', 'rb'))
header_rdr = DictReader(open('../../data/unicef/mn_headers.csv', 'rb'))

data_rows = [d for d in data_rdr]
header_rows = [h for h in header_rdr]
new_rows = []

for data_dict in data_rows:
    new_row = {}
    for dkey, dval in data_dict.items():
        for header_dict in header_rows:
            if dkey in header_dict.values():
                new_row[header_dict.get('Label')] = dval
    new_rows.append(new_row)

print new_rows[0]
