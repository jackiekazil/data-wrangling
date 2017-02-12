from csv import reader


def get_headers(data_rows, header_rows):
    all_short_headers = [h[0] for h in header_rows]
    skip_index = []
    final_header_rows = []

    for header in data_rows[0]:
        if header not in all_short_headers:
            index = data_rows[0].index(header)
            skip_index.append(index)
        else:
            for head in header_rows:
                if head[0] == header:
                    final_header_rows.append(head)
                    break
    return final_header_rows, skip_index


def get_clean_rows():
    data_rdr = reader(open('../../data/unicef/mn.csv', 'rb'))
    header_rdr = reader(open('../../data/unicef/mn_headers_updated.csv', 'rb'))

    data_rows = [d for d in data_rdr]
    header_rows = [h for h in header_rdr if h[0] in data_rows[0]]

    final_header_rows, skip_index = get_headers(data_rows, header_rows)
    new_data = []

    for row in data_rows[1:]:
        new_row = []
        for i, d in enumerate(row):
            if i not in skip_index:
                new_row.append(d)
        new_data.append(new_row)
    return header_rows, new_data


def get_zipped_data():
    header_rows, data_rows = get_clean_rows()
    zipped_data = []

    for drow in data_rows:
        zipped_data.append(zip(header_rows, drow))
    return zipped_data
