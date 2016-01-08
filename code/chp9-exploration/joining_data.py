"""
Part 3 / 5

NOTE: This is continued iPython exploration joining the child labor data
with corruption perception data. It also begins to explore some of the powerful
`agate` library features for statistical correlations. Again, this is not
to be used as a script, only an example of the exploration covered in
Chapter 9. --@kjam
"""
import agate
import xlrd

from xlrd.sheet import ctype_text

text_type = agate.Text()
number_type = agate.Number()
boolean_type = agate.Boolean()
date_type = agate.Date()


def remove_bad_chars(val):
    if val == '-':
        return None
    return val


def get_types(example_row):
    types = []
    for v in example_row:
        value_type = ctype_text[v.ctype]
        if value_type == 'text':
            types.append(text_type)
        elif value_type == 'number':
            types.append(number_type)
        elif value_type == 'xldate':
            types.append(date_type)
        else:
            types.append(text_type)
    return types


workbook = xlrd.open_workbook('../../data/unicef/unicef_oct_2014.xls')
sheet = workbook.sheets()[0]

title_rows = zip(sheet.row_values(4), sheet.row_values(5))
titles = [t[0] + ' ' + t[1] for t in title_rows]
titles = [t.strip() for t in titles]

country_rows = [sheet.row_values(r) for r in range(6, 114)]
cleaned_rows = []

for row in country_rows:
    cleaned_row = [remove_bad_chars(rv) for rv in row]
    cleaned_rows.append(cleaned_row)

example_row = sheet.row(6)
types = get_types(example_row)

table = agate.Table(cleaned_rows, titles, types)
ranked = table.compute([('Total Child Labor Rank',
                         agate.Rank('Total (%)', reverse=True)), ])


cpi_workbook = xlrd.open_workbook(
    '../../data/chp9/corruption_perception_index.xls')
cpi_sheet = cpi_workbook.sheets()[0]

for r in range(cpi_sheet.nrows):
    print r, cpi_sheet.row_values(r)

cpi_title_rows = zip(cpi_sheet.row_values(1), cpi_sheet.row_values(2))
cpi_titles = [t[0] + ' ' + t[1] for t in cpi_title_rows]
cpi_titles = [t.strip() for t in cpi_titles]
cpi_rows = [cpi_sheet.row_values(r) for r in range(3, cpi_sheet.nrows)]


def get_table(new_arr, types, titles):
    try:
        table = agate.Table(new_arr, titles, types)
        return table
    except Exception as e:
        print e

cpi_types = get_types(cpi_sheet.row(3))
cpi_titles

cpi_table = get_table(cpi_rows, cpi_types, cpi_titles)
cpi_titles[0] = cpi_titles[0] + ' Duplicate'

cpi_table = get_table(cpi_rows, cpi_types, cpi_titles)

cpi_and_cl = cpi_table.join(ranked, 'Country / Territory',
                            'Countries and areas', inner=True)

cpi_and_cl.print_table()
cpi_and_cl.column_names
len(cpi_and_cl.rows)
len(cpi_table.rows)
len(ranked.rows)

for r in cpi_and_cl.order_by('CPI 2013 Score').limit(10).rows:
    print '{}: {} - {}%'.format(r['Country / Territory'],
                                r['CPI 2013 Score'], r['Total (%)'])

import numpy
numpy.corrcoef(cpi_and_cl.columns['Total (%)'].values(),
               cpi_and_cl.columns['CPI 2013 Score'].values())[0, 1]


numpy.corrcoef(
    [float(t) for t in cpi_and_cl.columns['Total (%)'].values()],
    [float(s) for s in cpi_and_cl.columns['CPI 2013 Score'].values()])[0, 1]


import agatestats
agatestats.patch()

std_dev_outliers = cpi_and_cl.stdev_outliers(
    'Total (%)', deviations=3, reject=False)
len(std_dev_outliers.rows)

std_dev_outliers = cpi_and_cl.stdev_outliers(
    'Total (%)', deviations=5, reject=False)
len(std_dev_outliers.rows)


mad = cpi_and_cl.mad_outliers('Total (%)')
for r in mad.rows:
    print r['Country / Territory'], r['Total (%)']
