pdf_txt = 'en-final-table9.txt'
openfile = open(pdf_txt, 'r')
country_line = total_line = False
previous_line = ''
countries = []
totals = []

double_lined_countries = [
    'Bolivia (Plurinational \n',
    'Democratic People\xe2\x80\x99s \n',
    'Democratic Republic \n',
    'Lao People\xe2\x80\x99s Democratic \n',
    'Micronesia (Federated \n',
    'Saint Vincent and \n',
    'The former Yugoslav \n',
    'United Republic \n',
    'Venezuela (Bolivarian \n',
]

def turn_on_off(line, status, start, prev_line, end='\n'):
    """
    This function checks to see if a line starts/ends with a certain
    value. If the line starts/ends with that value, the status is
    set to on/off (True/False).
    """
    if line.startswith(start):
        status = True
    elif status:
        if line == end and prev_line != 'and areas':
            status = False
    return status


def clean(line):
    """
    Cleans line breaks, spaces, and special characters from our line.
    """
    line = line.strip('\n').strip()
    line = line.replace('\xe2\x80\x93', '-')
    line = line.replace('\xe2\x80\x99', '\'')
    return line


for line in openfile:
    if country_line:
        if previous_line in double_lined_countries:
            line = ' '.join([clean(previous_line), clean(line)])
        countries.append(clean(line))

    elif total_line:
        if len(line.replace('\n', '').strip()) > 0:
            totals.append(clean(line))



    country_line = turn_on_off(line, country_line, 'and areas', previous_line)
    total_line = turn_on_off(line, total_line, 'total', previous_line)

    previous_line = line


import pprint
data = dict(zip(countries, totals))
pprint.pprint(data)
