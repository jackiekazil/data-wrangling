import csv

csvfile = open('data-text.csv', "rb")
reader = csv.reader(csvfile)

for row in reader:
    print row
