""" This short script can be used if you are taking breaks in between sections
of Chapter 9 and Chapter 10 and need a quick reference to just the essential parts
of our data exploration.
"""

import agate
import xlrd
from xlrd.sheet import ctype_text

text_type = agate.Text()
number_type = agate.Number()
boolean_type = agate.Boolean()
date_type = agate.Date()

def remove_bad_chars(val):
    """ Removing erroneous '-' values from missing data rows. """
    if val == '-':
        return None
    return val


def get_types(example_row):
    """ Classify with agate types using an XLS example row. """
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


def get_table(new_arr, types, titles):
    """ Return an agate table when given an array of data, list of types and
    list of titles."""
    try:
        table = agate.Table(new_arr, titles, types)
        return table
    except Exception as e:
        print e


def unicef_data():
    """ Return a ranked agate table of unicef data with proper cleaned rows."""
    workbook = xlrd.open_workbook('unicef_oct_2014.xlsx')
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

    return ranked


def cpi_data():
    """ Return an agate table of CPI data with proper rows."""


    cpi_workbook = xlrd.open_workbook(
        'corruption_perception_index.xlsx')
    cpi_sheet = cpi_workbook.sheets()[0]


    cpi_title_rows = zip(cpi_sheet.row_values(1), cpi_sheet.row_values(2))
    cpi_titles = [t[0] + ' ' + t[1] for t in cpi_title_rows]
    cpi_titles = [t.strip() for t in cpi_titles]
    cpi_rows = [cpi_sheet.row_values(r) for r in range(3, cpi_sheet.nrows)]


    cpi_types = get_types(cpi_sheet.row(3))
    cpi_titles[0] = cpi_titles[0] + ' Duplicate'
    cpi_table = get_table(cpi_rows, cpi_types, cpi_titles)

    return cpi_table


def combine_tables():
    """ Combining UNICEF and CPI data and returning the joined table. Can be used
    as a shortcut if you are taking breaks between code for Chp 9 and Chp 10."""
    ranked = unicef_data()
    cpi_table = cpi_data()
    cpi_and_cl = cpi_table.join(ranked, 'Country / Territory',
                                'Countries and areas', inner=True)
    return cpi_and_cl
