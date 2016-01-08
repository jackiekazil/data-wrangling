"""
Part 4 / 5
NOTE: This is a continuation of the IPython session working with
child labor and corruption indexes to determine correlation. Again, it
should not be used as a script, but instead an example of functions and
methods when exploring data.
"""
import json
import agate

country_json = json.loads(open('../../data/chp9/earth.json', 'rb').read())
country_dict = {}

for dct in country_json:
    country_dict[dct['name']] = dct['parent']


def get_country(country_row):
    return country_dict.get(country_row['Country / Territory'].lower())

cpi_and_cl = cpi_and_cl.compute([('continent',
                                  agate.Formula(text_type, get_country)), ])
cpi_and_cl.column_names

for r in cpi_and_cl.rows:
    print r['Country / Territory'], r['continent']

no_continent = cpi_and_cl.where(lambda x: x['continent'] is None)
for r in no_continent.rows:
    print r['Country / Territory']

cpi_and_cl = cpi_table.join(ranked, 'Country / Territory',
                            'Countries and areas', inner=True)
country_json = json.loads(open(
    '../../data/chp9/earth-cleaned.json', 'rb').read())

for dct in country_json:
    country_dict[dct['name']] = dct['parent']

cpi_and_cl = cpi_and_cl.compute([('continent',
                                  agate.Formula(text_type, get_country)), ])

for r in cpi_and_cl.rows:
    print r['Country / Territory'], r['continent']

grp_by_cont = cpi_and_cl.group_by('continent')
grp_by_cont

for cont, table in grp_by_cont.items():
    print cont, len(table.rows)

agg = grp_by_cont.aggregate([('cl_mean', agate.Mean('Total (%)')),
                             ('cl_max', agate.Max('Total (%)')),
                             ('cpi_median', agate.Median('CPI 2013 Score')),
                             ('cpi_min', agate.Min('CPI 2013 Score'))])

agg
agg.print_table()

agg.print_bars('continent', 'cl_max')
