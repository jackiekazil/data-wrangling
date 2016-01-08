import json

# NOTE: you will need the 'ranked' table we first created in Chapter 9.

country_codes = json.loads(open('../../data/chp10/iso-2-cleaned.json', 'rb').read())
country_dict = {}

for c in country_codes:
    country_dict[c.get('name')] = c.get('alpha-2')

def get_country_code(row):
    return country_dict.get(row['Countries and areas'])

ranked = ranked.compute([(agate.Formula(text_type, get_country_code),
                          'country_code')])

for r in ranked.where(lambda x: x.get('country_code') is None).rows:
    print r['Countries and areas']
