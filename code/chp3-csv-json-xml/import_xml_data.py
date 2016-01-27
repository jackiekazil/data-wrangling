from xml.etree import ElementTree as ET

tree = ET.parse('../../data/chp3/data-text.xml')
root = tree.getroot()
print root

data = root.find('Data')

all_data = []

for observation in data:
    record = {}
    for item in observation:

        lookup_key = item.attrib.keys()[0]

        if lookup_key == 'Numeric':
            rec_key = 'NUMERIC'
            rec_value = item.attrib['Numeric']
        else:
            rec_key = item.attrib[lookup_key]
            rec_value = item.attrib['Code']

        record[rec_key] = rec_value
    all_data.append(record)

print all_data
