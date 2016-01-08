"""
Part 5 / 5 (TBC in Chapter 10 with some charts)
NOTE: This is the final parts of Chapter 9's data exploration
using `agate`. This is just to be used as an example of how to
explore and investigate data. This section focuses on the dataset
from Africa and investigating correlation and potential case studies.
"""


africa_cpi_cl = cpi_and_cl.where(lambda x: x['continent'] == 'africa')

for r in africa_cpi_cl.order_by('Total (%)', reverse=True).rows:
    print "{}: {}% - {}".format(r['Country / Territory'], r['Total (%)'],
    r['CPI 2013 Score'])

import numpy

print numpy.corrcoef(
[float(t) for t in africa_cpi_cl.columns['Total (%)'].values()],
[float(c) for c in africa_cpi_cl.columns['CPI 2013 Score'].values()])[0, 1]

africa_cpi_cl = africa_cpi_cl.compute([('Africa Child Labor Rank', agate.Rank('Total (%)', reverse=True)), ])
africa_cpi_cl = africa_cpi_cl.compute([('Africa CPI Rank',
                                          agate.Rank('CPI 2013 Score')),
                                        ])
africa_cpi_cl.print_table()

cpi_mean = africa_cpi_cl.aggregate(agate.Mean('CPI 2013 Score'))
cl_mean = africa_cpi_cl.aggregate(agate.Mean('Total (%)'))

cl_mean
cpi_mean

def highest_rates(row):
    if row['Total (%)'] > cl_mean and row['CPI 2013 Score'] < cpi_mean:
        return True
    return False

highest_cpi_cl = africa_cpi_cl.where(lambda x: highest_rates(x))

for r in highest_cpi_cl.rows:
    print "{}: {}% - {}".format(r['Country / Territory'], r['Total (%)'],
    r['CPI 2013 Score'])

