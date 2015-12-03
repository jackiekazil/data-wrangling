import xlrd
from xlrd.sheet import ctype_text
import csv
from decimal import Decimal
import agate
import json
import numpy


DATA_FOLDER = '../../data/chp9/'


workbook = xlrd.open_workbook(DATA_FOLDER + 'unicef_oct_2014.xls')
sheet = workbook.sheets()[0]

title_rows = zip(sheet.row_values(4), sheet.row_values(5))
country_rows = [sheet.row_values(r) for r in range(6, 114)]
continent_rows = [sheet.row_values(r) for r in range(115, 125)]

text_type = agate.Text()
number_type = agate.Number()
date_type = agate.Date()

titles = [t[0] + ' ' + t[1] for t in title_rows]
titles = [t.strip() for t in titles]
types = []

example_row = sheet.row(6)

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

try:
    table = agate.Table(country_rows, zip(titles, types))
    #Throws error for conversion
except Exception as e:
    print e
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
    table = agate.Table(cleaned_rows, zip(titles, types))
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

new_arr = get_new_array(cleaned_rows, remove_bad_chars)


def get_table(new_arr, types, titles):
    try:
        table = agate.Table(new_arr, zip(titles, types))
        return table
    except Exception as e:
        print e

table = get_table(new_arr, types, titles)

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

has_por.columns['Place of residence (%) Urban'].aggregate(agate.Mean())
has_por.columns['Place of residence (%) Urban'].aggregate(agate.Max())

has_por.columns['Rural'].aggregate(agate.Mean())
has_por.columns['Rural'].aggregate(agate.Max())

has_por.find(lambda x: x['Rural'] > 50)

ranked = table.compute([(agate.Rank('Total (%)',
                        reverse=True), 'Total Child Labor Rank')])

# If we wanted a column showing children not working percentage ...


def reverse_percent(row):
    return 100 - row['Total (%)']

table = table.compute([(agate.Formula(number_type, reverse_percent),
                       'Children not working (%)')])

# some investigation into other possible connections

hiv_workbook = xlrd.open_workbook(DATA_FOLDER + 'hiv_aids_2014.xlsx')
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


def clean_null_data(row):
    return [r.replace(u'\u2013', '') if
            isinstance(r, (str, unicode)) else str(r) for r in row]

country_data = [clean_null_data(row) for row in country_data]

hiv_table = get_table(country_data, hiv_types, hiv_titles)

joined = hiv_table.join(ranked,
                        'Countries and territories',
                        'Countries and areas')

print joined.columns.keys()

has_estimate = joined.where(lambda row: row['High estimate'] is not None)

for row in has_estimate.rows[:]:
    print '%s: child labor %s%%;  num parents lost: %d' % (
        row['Countries and territories'], row['Total (%)'],
        row['Children who have lost one or both parents due to AIDS,' +
            ' 2013 Estimate'])

for row in has_estimate.rows[:]:
    print '%s %s: child labor %s%%;  num parents lost: %d' % (
        row['Countries and territories'], row['Countries and territories'],
        row['Total (%)'], row[
            'Children who have lost one or both parents due to AIDS,' +
            ' 2013 Estimate'])

has_both = has_estimate.where(lambda row:
                              row['Total (%)'] is not None)

len(has_both.rows)

for row in has_both.rows[:]:
    print row['Countries and territories'], row['Total Child Labor Rank']

hiv_table = hiv_table.where(lambda row:
                            row['Children who have lost one or both' +
                                ' parents due to AIDS, 2013 Estimate']
                            is not None)

has_both_with_join = ranked.join(hiv_table, 'Countries and areas',
                                 'Countries and territories', inner=True)

for row in has_both_with_join.order_by('Children who have lost one ' +
                                       'or both parents' +
                                       ' due to AIDS, 2013 Estimate',
                                       reverse=True).rows[:]:
    print row['Countries and areas'], \
        row['Total Child Labor Rank'], row['Children who have lost ' +
                                           'one or both parents' +
                                           ' due to AIDS, 2013 Estimate']


# exploring teen pregnancy data

teen_pregnancy = csv.reader(open(DATA_FOLDER + 'fertility_rate.csv', 'rb'))


def get_csv_types(example_row):
    types = []
    for r in example_row:
        try:
            float(r)
            types.append(number_type)
        except:
            types.append(text_type)
    return types

# Note: you cannot read backwards in a CSV reader so apologize for the messy
# next calls. If we actually wanted to use this data in the future, we would
# want to write a function for this and likely first create a list of rows and
# then produce the types and titles

next(teen_pregnancy, None)
next(teen_pregnancy, None)

teen_preg_titles = next(teen_pregnancy, None)
teen_preg_types = get_csv_types(next(teen_pregnancy, None))

teen_pregnancy = csv.reader(open(DATA_FOLDER + 'fertility_rate.csv', 'rb'))
next(teen_pregnancy, None)
next(teen_pregnancy, None)
next(teen_pregnancy, None)

teen_preg_table = get_table(teen_pregnancy, teen_preg_types, teen_preg_titles)

try:
    preg_and_cl = teen_preg_table.join(ranked, 'Country Name',
                                       'Countries and areas', inner=True)
except:
    pass
# throws an error because of the blank final column

teen_preg_titles[-1] = 'Extra'

teen_pregnancy = csv.reader(open(DATA_FOLDER + 'fertility_rate.csv', 'rb'))
next(teen_pregnancy, None)
next(teen_pregnancy, None)
next(teen_pregnancy, None)

teen_preg_table = get_table(teen_pregnancy, teen_preg_types, teen_preg_titles)

preg_and_cl = teen_preg_table.join(ranked, 'Country Name',
                                   'Countries and areas', inner=True)

for row in preg_and_cl.order_by('2014', reverse=True).limit(20).rows:
    print '%s: %s %s' % (row['Country Name'], row['2014'],
                         row['Total Child Labor Rank'])


len(preg_and_cl.rows)


# Investigating agricultural links


agriculture = csv.reader(open(DATA_FOLDER + 'agriculture_rate.csv', 'rb'))
next(agriculture, None)
next(agriculture, None)

agr_titles = next(agriculture, None)
agr_titles[-1] = "extra"
agr_types = get_csv_types(next(agriculture, None))

agriculture = csv.reader(open(DATA_FOLDER + 'agriculture_rate.csv', 'rb'))
next(agriculture, None)
next(agriculture, None)
next(agriculture, None)

agr_table = get_table(agriculture, agr_types, agr_titles)

agr_and_cl = ranked.join(agr_table, 'Countries and areas',
                         'Country Name', inner=True)

for row in agr_and_cl.where(lambda r:
                            r['2013'] is not None).order_by(
                                '2013', reverse=True).limit(20).rows:
    print '%s: %s %s' % (row['Countries and areas'], row['2013'],
                         row['Total Child Labor Rank'])


def get_latest_avg(row):
    latest_yrs = ['2013', '2012', '2011', '2010']
    how_many = [x for x in latest_yrs if row[x] is not None]
    tot = sum(Decimal(row[x]) for x in how_many)
    if len(how_many) > 0:
        return tot / len(how_many)
    return None


agr_and_cl = agr_and_cl.compute([(agate.Formula(number_type, get_latest_avg),
                                'latest_avg',)])

agr_and_cl = agr_and_cl.where(lambda x: x['latest_avg'] is not None)

print 'latest avgs'

for row in agr_and_cl.order_by('latest_avg', reverse=True).rows:
    print '%s: %s %s' % (row['Countries and areas'], row['latest_avg'],
                         row['Total Child Labor Rank'])


def get_table_from_wb_data(file_name):
    rdr = csv.reader(open(file_name, 'rb'))
    lines = [l for l in rdr]
    titles = lines[2]
    titles[-1] = 'extra'
    types = get_csv_types(lines[3])
    return get_table(lines[3:], types, titles)


country_json = json.loads(open(
    DATA_FOLDER + 'earth-cleaned.json', 'rb').read())


rural = get_table_from_wb_data(DATA_FOLDER + 'rural.csv')
africa = [c['name'] for c in country_json if c['parent'] == 'africa']
africa_ranked = ranked.where(lambda x: x['Countries and areas'].lower()
                             in africa)

rur_and_cl = africa_ranked.join(rural, 'Countries and areas',
                                'Country Name', inner=True)

print len(rur_and_cl.rows)

rur_and_cl = rur_and_cl.compute([(agate.Formula(number_type, get_latest_avg),
                                  'latest_avg')])

rur_and_cl = rur_and_cl.where(lambda x: x['latest_avg'] is not None)

print 'latest rural'

for row in rur_and_cl.order_by('latest_avg', reverse=True).rows:
    print '%s: %s %s' % (row['Countries and areas'], row['latest_avg'],
                         row['Total Child Labor Rank'])


# Investigating links with homicide data


homicides = csv.reader(open(DATA_FOLDER + 'homicide-deaths.csv', 'rb'))
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


hom_and_cl = africa_ranked.join(homicide_table,
                                'Countries and areas', 'COUNTRY (DISPLAY)',
                                inner=True)

print hom_and_cl.columns['Numeric'].aggregate(agate.Median())


for r in hom_and_cl.order_by('Numeric', reverse=True).rows:
    print r['Countries and areas'], r['Numeric'], r['Total (%)']


# Investigating CPI (Corruption perception index)

pci_workbook = xlrd.open_workbook(DATA_FOLDER +
                                  'perceived_corruption_index.xls')
pci_sheet = pci_workbook.sheets()[0]

for r in range(pci_sheet.nrows):
    print r, pci_sheet.row_values(r)

pci_title_rows = zip(pci_sheet.row_values(1), pci_sheet.row_values(2))
pci_titles = [t[0] + ' ' + t[1] for t in pci_title_rows]
pci_titles = [t.strip() for t in pci_titles]

pci_rows = [pci_sheet.row_values(r) for r in range(3, pci_sheet.nrows)]

pci_types = get_types(pci_sheet.row(3))

try:
    pci_table = get_table(pci_rows, pci_types, pci_titles)
except:
    # error : duplicate titles
    pass

pci_titles[0] = pci_titles[0] + ' Duplicate'

try:
    pci_table = get_table(pci_rows, pci_types, pci_titles)
except:
    pass
    # error - float prallem

pci_rows = get_new_array(pci_rows, float_to_str)

pci_table = get_table(pci_rows, pci_types, pci_titles)


pci_and_cl = pci_table.join(ranked, 'Country / Territory',
                            'Countries and areas', inner=True)

pci_and_cl.columns.keys()

for r in pci_and_cl.order_by('CPI 2013 Score').limit(10).rows:
    print '{}: {} - {}%'.format(r['Country / Territory'],
                                r['CPI 2013 Score'], r['Total (%)'])

country_json = json.loads(open(DATA_FOLDER +
                               'earth-cleaned.json', 'rb').read())

country_dict = {}

for dct in country_json:
    country_dict[dct['name']] = dct['parent']


def get_country(row):
    return country_dict.get(row['Country / Territory'].lower())

pci_and_cl = pci_and_cl.compute([(agate.Formula(text_type, get_country),
                                  'continent')])

no_continent = pci_and_cl.where(lambda x: x['continent'] is None)

for r in no_continent.rows:
    print r['Countries and areas']


grouped = pci_and_cl.group_by('continent')

agg = grouped.aggregate([
    ('Total (%)', agate.Mean(), 'total_mean'),
    ('Total (%)', agate.Max(), 'total_max'),
    ('CPI 2013 Score', agate.Median(), 'cpi_median'),
    ('CPI 2013 Score', agate.Min(), 'cpi_min')])


agg_cols = agg.columns.keys()

print agg_cols

agg_cols_to_show = [c for c in agg_cols if c not in
                    ['continent', 'continent_count']]

for r in agg.rows:
    agg_details = '; '.join(['%s: %.2f' % (col_name, r[col_name])
                             for col_name in agg_cols_to_show])
    print '%s\t: %s' % (r['continent'], agg_details)


africa_pci_cl = pci_and_cl.where(lambda x: x['continent'] == 'africa')

for r in africa_pci_cl.order_by('Total (%)', reverse=True).rows:
        print "{}: {}% - {}".format(r['Country / Territory'], r['Total (%)'],
                                    r['CPI 2013 Score'])


print numpy.corrcoef(
    [float(x) for x in africa_pci_cl.columns['Total (%)'].values()],
    [float(x) for x in africa_pci_cl.columns['CPI 2013 Score'].values()])[0, 1]


africa_pci_cl = africa_pci_cl.compute([(agate.Rank('Total (%)', reverse=True),
                                        'Africa Child Labor Rank')])
africa_pci_cl = africa_pci_cl.compute([(agate.Rank('CPI 2013 Score'),
                                        'Africa CPI Rank')])


cl_mean = africa_pci_cl.columns['Total (%)'].aggregate(agate.Mean())
cpi_mean = africa_pci_cl.columns['CPI 2013 Score'].aggregate(agate.Mean())


def highest_rates(row):
    if row['Total (%)'] > cl_mean and row['CPI 2013 Score'] < cpi_mean:
        return True
    return False

highest_pci_cl = africa_pci_cl.where(lambda x: highest_rates(x))

print numpy.corrcoef(
    [float(x) for x in highest_pci_cl.columns['Total (%)'].values()],
    [float(x) for x in highest_pci_cl.columns['CPI 2013 Score'].values()]
)[0, 1]

print highest_pci_cl.columns.keys()

for r in highest_pci_cl.rows:
    print "{}: {}% - {}".format(r['Country / Territory'], r['Total (%)'],
                                r['CPI 2013 Score'])

import matplotlib.pyplot as plt

plt.plot(africa_pci_cl.columns['CPI 2013 Score'],
         africa_pci_cl.columns['Total (%)'])
plt.xlabel('CPI Score - 2013')
plt.ylabel('Child Labor Percentage')
plt.title('CPI & Child Labor Correlation')

plt.show()


plt.plot(highest_pci_cl.columns['CPI 2013 Score'],
         highest_pci_cl.columns['Total (%)'])
plt.xlabel('CPI Score - 2013')
plt.ylabel('Child Labor Percentage')
plt.title('CPI & Child Labor Correlation')

plt.show()

import pygal

country_codes = json.loads(
    open(DATA_FOLDER + 'iso-2-cleaned.json', 'rb').read())
country_dict = {}

for c in country_codes:
    country_dict[c.get('name')] = c.get('alpha-2')

print ranked.columns.keys()


def get_country_code(row):
    return country_dict.get(row['Countries and areas'])

ranked = ranked.compute([(agate.Formula(text_type, get_country_code),
                        'country_code')])

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
