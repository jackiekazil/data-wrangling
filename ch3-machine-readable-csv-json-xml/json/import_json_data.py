import json

json_data = open('data-text.json').read()

data = json.loads(json_data)

for item in data:
    print item
