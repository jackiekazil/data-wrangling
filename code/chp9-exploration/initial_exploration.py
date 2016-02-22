""" This is an OLD version of some data exploration for the book. You will
notice it uses an old form of agate called journalism. You will also notice it's
simply a dump of an IPython session. We've included it as just an example of
how we attempted to link the data to different datasets. Again, it's not code
you should use, but if you'd like to take a look to see different ways of
investigating connections or if you'd like to try investigating those connections
yourself, it might be of interest. -- @kjam
"""


import xlrd
import journalism
from xlrd.sheet import ctype_text
import csv
from decimal import Decimal
import json


workbook = xlrd.open_workbook('unicef_oct_2014.xls')

workbook.nsheets
workbook.sheet_names()
workbook.sheets()

sheet = workbook.sheets()[0]

sheet.nrows
sheet.row_values(0)


for r in range(sheet.nrows):
    print r, sheet.row(r)

title_rows = zip(sheet.row_values(4), sheet.row_values(5))


country_rows = [sheet.row_values(r) for r in range(6, 114)]


continent_rows = [sheet.row_values(r) for r in range(115, 125)]



text_type = journalism.TextType()
number_type = journalism.NumberType()
date_type = journalism.DateType()


titles = [t[0] + ' ' + t[1] for t in title_rows]
titles = [t.strip() for t in titles]
types = []


example_row = sheet.row(6)
example_row[0].ctype
example_row[0].value




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



columns = zip(titles, types)
columns

try:
    table = journalism.Table(country_rows, types, titles)
    #Throws error for conversion
except:
    pass

cleaned_rows = []


def float_to_str(val):
    if isinstance(val, float):
        return str(val)
    elif isinstance(val, (str, unicode)):
        print 'unicode is', val.encode('utf-8')
        return val.encode('ascii', errors='replace').strip()
    return val


for row in country_rows:
    cleaned_row = [float_to_str(rv) for rv in row]
    cleaned_rows.append(cleaned_row)


try:
    table = journalism.Table(cleaned_rows, types, titles)
    #Error re '-' to number conversion
except:
    pass


def remove_bad_chars(val):
    if val == '-':
        return None
    return val


def get_new_array(old_array, function_to_clean):
    new_arr = []
    for row in old_array:
        cleaned_row = [function_to_clean(rv) for rv in row]
        new_arr.append(cleaned_row)
    return new_arr

#TODO: place input and output here
new_arr = get_new_array(cleaned_rows, remove_bad_chars)


def get_table(new_arr, types, titles):
    try:
        table = journalism.Table(new_arr, types, titles)
        return table
    except Exception as e:
        print e

#TODO: place input and output here
table = get_table(new_arr, types, titles)

table.get_column_names()

most_egregious = table.order_by('Total (%)', reverse=True).limit(10)


for r in most_egregious.rows:
    print r


most_females = table.order_by('Female', reverse=True).limit(10)
for r in most_females.rows:
    print '{}: {}%'.format(r['Countries and areas'], r['Female'])


female_data = table.where(lambda r: r['Female'] is not None)
most_females = female_data.order_by('Female', reverse=True).limit(10)
for r in most_females.rows:
    print '{}: {}%'.format(r['Countries and areas'], r['Female'])


try:
    table.columns['Place of residence (%) Urban'].mean()
except:
    pass

has_por = table.where(lambda r: r['Place of residence (%) Urban'] is not None)

has_por.columns['Place of residence (%) Urban'].mean()
has_por.columns['Place of residence (%) Urban'].max()

has_por.columns['Rural'].mean()
has_por.columns['Rural'].max()


has_por.find(lambda x: x['Rural'] > 50)


ranked = table.rank('Total (%)', 'Total Child Labor Rank')

for row in ranked.order_by('Total (%)', reverse=True).limit(20).rows:
    print row['Total (%)'], row['Total Child Labor Rank']

#WOW! we did not expect that. so we need to make a new col i
# that's % of kids not working and sort by that...


def reverse_percent(percent_val):
    return 100 - percent_val

ranked = table.compute('Children not working (%)',
                       number_type, lambda x: reverse_percent(x['Total (%)']))


ranked = ranked.rank('Children not working (%)', 'Total Child Labor Rank')
for row in ranked.order_by('Total (%)', reverse=True).limit(20).rows:
    print row['Total (%)'], row['Total Child Labor Rank']


# TODO: Here i need to figure out whether to use percentiles and HOW
#ranked = ranked.compute('Child labor percentiles', number_type,
#                        lambda x: x.percentile())

hiv_workbook = xlrd.open_workbook('hiv_aids_2014.xlsx')

hiv_workbook.sheet_names()

children = hiv_workbook.sheet_by_name('T6_CABA')

hiv_titles = zip(children.row_values(3), children.row_values(4),
                 children.row_values(5))
hiv_titles = [' '.join(list(t)) for t in hiv_titles]
hiv_titles = [t.strip() for t in hiv_titles]

for row in range(0, children.nrows):
    print row, children.row(row)

country_data = [children.row_values(r) for r in range(6, 203)]


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

# Nambia appears to have all the data
hiv_types = get_types(children.row(125))

# Error: duplicate titles
try:
    hiv_table = get_table(country_data, hiv_types, hiv_titles)
except:
    print hiv_titles

for i in range(len(hiv_titles)):
    if 'FN' in hiv_titles[i]:
        hiv_titles[i] = '%s Notes' % hiv_titles[i - 1]

# Error: bad data in blank rows
try:
    hiv_table = get_table(country_data, hiv_types, hiv_titles)
except:
    print country_data[4]


# first i did not have u'' in front of unicode, point out mistake!
def clean_null_data(row):
    return [r.replace(u'\u2013', '') if
            isinstance(r, (str, unicode)) else str(r) for r in row]

country_data = [clean_null_data(row) for row in country_data]

hiv_table = get_table(country_data, hiv_types, hiv_titles)

joined = hiv_table.left_outer_join(
    'Countries and territories', ranked, 'Countries and areas')

joined.get_column_names()

has_estimate = joined.where(lambda row: row['High estimate'] is not None)

for row in has_estimate.rows[:]:
    print '%s: child labor %s%%;  num parents lost: %d' % (
        row['Countries and areas'], row['Total (%)'],
        row['Children who have lost one or both parents due to AIDS,' +
            ' 2013 Estimate'])

for row in has_estimate.rows[:]:
    print '%s %s: child labor %s%%;  num parents lost: %d' % (
        row['Countries and areas'], row['Countries and territories'],
        row['Total (%)'], row[
            'Children who have lost one or both parents due to AIDS,' +
            ' 2013 Estimate'])

has_both = has_estimate.where(lambda row:
                              row['Total (%)'] is not None)

len(has_both.rows)

for row in has_both.rows[:]:
    print row['Countries and areas'], row['Total Child Labor Rank']

hiv_table = hiv_table.where(lambda row:
                            row['Children who have lost one or both' +
                                ' parents due to AIDS, 2013 Estimate']
                            is not None)

has_both_with_join = ranked.inner_join('Countries and areas',
                                       hiv_table, 'Countries and territories')

for row in has_both_with_join.order_by('Children who have lost one ' +
                                       'or both parents' +
                                       ' due to AIDS, 2013 Estimate',
                                       reverse=True).rows[:]:
    print row['Countries and areas'], \
        row['Total Child Labor Rank'], row['Children who have lost ' +
                                           'one or both parents' +
                                           ' due to AIDS, 2013 Estimate']



teen_pregnancy = csv.reader(open('fertility_rate.csv', 'rb'))


def get_csv_types(example_row):
    types = []
    for r in example_row:
        try:
            float(r)
            types.append(number_type)
        except:
            types.append(text_type)
    return types

next(teen_pregnancy, None)
next(teen_pregnancy, None)

teen_preg_titles = next(teen_pregnancy, None)
teen_preg_types = get_csv_types(next(teen_pregnancy, None))

# A note about the inability of reading "backwards" in csvs

teen_pregnancy = csv.reader(open('fertility_rate.csv', 'rb'))
next(teen_pregnancy, None)
next(teen_pregnancy, None)
next(teen_pregnancy, None)

teen_preg_table = get_table(teen_pregnancy, teen_preg_types, teen_preg_titles)

try:
    preg_and_cl = teen_preg_table.inner_join('Country Name', ranked,
                                             'Countries and areas')
except:
    pass
# throws an error because of the blank final column

teen_preg_titles[-1] = 'Extra'
teen_preg_table = get_table(teen_pregnancy, teen_preg_types, teen_preg_titles)

preg_and_cl = teen_preg_table.inner_join('Country Name', ranked,
                                         'Countries and areas')

for row in preg_and_cl.order_by('2014', reverse=True).limit(20).rows:
    print '%s: %s %s' % (row['Country Name'], row['2014'],
                         row['Total Child Labor Rank'])


len(preg_and_cl.rows)


agriculture = csv.reader(open('agriculture_rate.csv', 'rb'))
next(agriculture, None)
next(agriculture, None)

agr_titles = next(agriculture, None)
agr_titles[-1] = "extra"
agr_types = get_csv_types(next(agriculture, None))

agriculture = csv.reader(open('agriculture_rate.csv', 'rb'))
next(agriculture, None)
next(agriculture, None)
next(agriculture, None)

agr_table = get_table(agriculture, agr_types, agr_titles)

agr_and_cl = ranked.inner_join('Countries and areas', agr_table,
                               'Country Name')

print len(agr_and_cl.rows)
for row in agr_and_cl.where(lambda r:
                            r['2013'] is not None).order_by(
                                '2013', reverse=True).limit(20).rows:
    print '%s: %s %s' % (row['Country Name'], row['2013'],
                         row['Total Child Labor Rank'])


def get_latest_avg(row):
    latest_yrs = ['2013', '2012', '2011', '2010']
    how_many = [x for x in latest_yrs if row[x] is not None]
    tot = sum(Decimal(row[x]) for x in how_many)
    if len(how_many) > 0:
        return tot / len(how_many)
    return None


agr_and_cl = agr_and_cl.compute('latest_avg', number_type,
                                lambda x: get_latest_avg(x))

agr_and_cl = agr_and_cl.where(lambda x: x['latest_avg'] is not None)

print 'latest avgs'

for row in agr_and_cl.order_by('latest_avg', reverse=True).rows:
    print '%s: %s %s' % (row['Country Name'], row['latest_avg'],
                         row['Total Child Labor Rank'])


def get_table_from_wb_data(file_name):
    rdr = csv.reader(open(file_name, 'rb'))
    lines = [l for l in rdr]
    titles = lines[2]
    titles[-1] = 'extra'
    types = get_csv_types(lines[3])
    return get_table(lines[3:], types, titles)


country_json = json.loads(open(
    'earth-cleaned.json', 'rb').read())


rural = get_table_from_wb_data('rural.csv')
africa = [c['name'] for c in country_json if c['parent'] == 'africa']
africa_ranked = ranked.where(lambda x: x['Countries and areas'].lower()
                             in africa)

rur_and_cl = africa_ranked.inner_join('Countries and areas',
                                      rural, 'Country Name')

print len(rur_and_cl.rows)

rur_and_cl = rur_and_cl.compute('latest_avg', number_type,
                                lambda x: get_latest_avg(x))

rur_and_cl = rur_and_cl.where(lambda x: x['latest_avg'] is not None)

print 'latest rural'

for row in rur_and_cl.order_by('latest_avg', reverse=True).rows:
    print '%s: %s %s' % (row['Country Name'], row['latest_avg'],
                         row['Total Child Labor Rank'])


homicides = csv.reader(open('homicide-deaths.csv', 'rb'))
homicide_titles = next(homicides, None)
homicide_data = [r for r in homicides]
homicide_types = get_csv_types(homicide_data[0])

try:
    homicide_table = get_table(homicide_data, homicide_types, homicide_titles)
except:
    pass

#ascii error

for data_row in homicide_data:
    c = 0
    for item in data_row:
        if isinstance(item, (str, unicode)):
            data_row[c] = item.decode('utf-8', 'replace')
        c += 1

homicide_table = get_table(homicide_data, homicide_types, homicide_titles)

homicide_table = homicide_table.where(lambda x: 'rates' in x['GHO (DISPLAY)'])


hom_and_cl = africa_ranked.inner_join('Countries and areas', homicide_table,
                                      'COUNTRY (DISPLAY)')

print hom_and_cl.columns['Numeric'].median()


for r in hom_and_cl.order_by('Numeric', reverse=True).rows:
    print r['Countries and areas'], r['Numeric'], r['Total (%)']


cpi_workbook = xlrd.open_workbook('perceived_corruption_index.xls')
cpi_sheet = cpi_workbook.sheets()[0]

for r in range(cpi_sheet.nrows):
    print r, cpi_sheet.row_values(r)

cpi_title_rows = zip(cpi_sheet.row_values(1), cpi_sheet.row_values(2))
cpi_titles = [t[0] + ' ' + t[1] for t in cpi_title_rows]
cpi_titles = [t.strip() for t in cpi_titles]

cpi_rows = [cpi_sheet.row_values(r) for r in range(3, cpi_sheet.nrows)]

cpi_types = get_types(cpi_sheet.row(3))

try:
    cpi_table = get_table(cpi_rows, cpi_types, cpi_titles)
except:
    # error : duplicate titles
    pass

cpi_titles[0] = cpi_titles[0] + ' Duplicate'

try:
    cpi_table = get_table(cpi_rows, cpi_types, cpi_titles)
except:
    pass
    # error - float prallem

cpi_rows = get_new_array(cpi_rows, float_to_str)

cpi_table = get_table(cpi_rows, cpi_types, cpi_titles)


cpi_and_cl = cpi_table.inner_join('Country / Territory',
                                  ranked, 'Countries and areas')

cpi_and_cl.get_column_names()

for r in cpi_and_cl.order_by('CPI 2013 Score').limit(10).rows:
    print '{}: {} - {}%'.format(r['Country / Territory'],
                                r['CPI 2013 Score'], r['Total (%)'])


print cpi_and_cl.pearson_correlation('CPI 2013 Score', 'Total (%)')

print 'HEREEREREREE' * 20

country_json = json.loads(open('earth-cleaned.json', 'rb').read())

country_dict = {}

for dct in country_json:
    country_dict[dct['name']] = dct['parent']


def get_country(country_txt):
    return country_dict.get(country_txt.lower())

cpi_and_cl = cpi_and_cl.compute('continent', text_type,
                                lambda x:
                                get_country(x['Countries and areas']))

no_continent = cpi_and_cl.where(lambda x: x['continent'] is None)

for r in no_continent.rows:
    print r['Countries and areas']



cpi_and_cl.group_by('continent')

agg = cpi_and_cl.aggregate('continent', (('Total (%)', 'mean'),
                                        ('Total (%)', 'max'),
                                        ('CPI 2013 Score', 'median'),
                                        ('CPI 2013 Score', 'min')))


agg_cols = agg.get_column_names()

print agg_cols

agg_cols_to_show = [c for c in agg_cols if c not in
                    ['continent', 'continent_count']]

for r in agg.rows:
    agg_details = '; '.join(['%s: %.2f' % (col_name, r[col_name])
                             for col_name in agg_cols_to_show])
    print '%s\t: %s' % (r['continent'], agg_details)


africa_cpi_cl = cpi_and_cl.where(lambda x: x['continent'] == 'africa')

for r in africa_cpi_cl.order_by('Total (%)', reverse=True).rows:
        print "{}: {}% - {}".format(r['Countries and areas'], r['Total (%)'],
                                    r['CPI 2013 Score'])


print africa_cpi_cl.pearson_correlation('Total (%)', 'CPI 2013 Score')



africa_cpi_cl = africa_cpi_cl.rank('Children not working (%)',
                                   'Africa Child Labor Rank')
africa_cpi_cl = africa_cpi_cl.rank('CPI 2013 Score', 'Africa cpi Rank')


cl_mean = africa_cpi_cl.columns['Total (%)'].mean()
cpi_mean = africa_cpi_cl.columns['CPI 2013 Score'].mean()


def highest_rates(row):
    if row['Total (%)'] > cl_mean and row['CPI 2013 Score'] < cpi_mean:
        return True
    return False

highest_cpi_cl = africa_cpi_cl.where(lambda x: highest_rates(x))

for r in highest_cpi_cl.rows:
    print "{}: {}% - {}".format(r['Countries and areas'], r['Total (%)'],
                                r['CPI 2013 Score'])

import pylab

pylab.plot(africa_cpi_cl.columns['CPI 2013 Score'],
           africa_cpi_cl.columns['Total (%)'])
pylab.xlabel('CPI Score - 2013')
pylab.ylabel('Child Labor Percentage')
pylab.title('CPI & Child Labor Correlation')

pylab.show()


pylab.plot(highest_cpi_cl.columns['CPI 2013 Score'],
           highest_cpi_cl.columns['Total (%)'])
pylab.xlabel('CPI Score - 2013')
pylab.ylabel('Child Labor Percentage')
pylab.title('CPI & Child Labor Correlation')

pylab.show()


import pygal

country_codes = json.loads(open('iso-2-cleaned.json', 'rb').read())
country_dict = {}

for c in country_codes:
    country_dict[c.get('name')] = c.get('alpha-2')

ranked = ranked.compute('country_code', text_type,
                        lambda x: country_dict.get(x['Countries and areas']))

for r in ranked.where(lambda x: x.get('country_code') is None).rows:
    print r['Countries and areas']

worldmap_chart = pygal.Worldmap()
worldmap_chart.title = 'Child Labor Worldwide'

cl_dict = {}
for r in ranked.rows:
    cl_dict[r.get('country_code').lower()] = float(r.get('Total (%)'))


worldmap_chart.add('Total Child Labor (%)', cl_dict)
worldmap_chart.render_to_file('child_labor_worldwide.svg')
worldmap_chart.render_to_png('child_labor_worldwide.png')

# TODO:
# percentile
# date columns
# percent change
