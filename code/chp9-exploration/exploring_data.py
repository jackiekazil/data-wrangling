"""
Part 2 / 5

NOTE: this is a continuation of the IPython session beginning with importing_data.py.
It explores the table using some agate methods. Again, it is here as an example,
not as a usable script :) --@kjam
"""


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


(lambda x: 'Positive' if x >= 1 else 'Zero or Negative')(0)
(lambda x: 'Positive' if x >= 1 else 'Zero or Negative')(4)


table.columns['Place of residence (%) Urban'].aggregate(agate.Mean())
col = table.columns['Place of residence (%) Urban']
table.aggregate(agate.Mean('Place of residence (%) Urban'))


has_por = table.where(lambda r: r['Place of residence (%) Urban'] is not None)
has_por.aggregate(agate.Mean('Place of residence (%) Urban'))

first_match = has_por.find(lambda x: x['Rural'] > 50)
first_match['Countries and areas']

ranked = table.compute([('Total Child Labor Rank', agate.Rank('Total (%)', reverse=True)),])
for row in ranked.order_by('Total (%)', reverse=True).limit(20).rows:
    print row['Total (%)'], row['Total Child Labor Rank']

def reverse_percent(row):
    return 100 - row['Total (%)']
ranked = table.compute([('Children not working (%)',
                             agate.Formula(number_type, reverse_percent)),
                            ])

ranked = ranked.compute([('Total Child Labor Rank',
                              agate.Rank('Children not working (%)')),
                           ])


for row in ranked.order_by('Total (%)', reverse=True).limit(20).rows:
    print row['Total (%)'], row['Total Child Labor Rank']

