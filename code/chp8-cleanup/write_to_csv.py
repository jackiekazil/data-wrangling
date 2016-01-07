from csv import writer
from get_zipped_data import get_zipped_data

def write_file(zipped_data, file_name):
    with open(file_name, 'wb') as new_csv_file:
        wrtr = writer(new_csv_file)
        titles = [row[0][1] for row in zipped_data[0]]
        wrtr.writerow(titles)
        for row in zipped_data:
            answers = [resp[1] for resp in row]
            wrtr.writerow(answers)

write_file(get_zipped_data(), 'cleaned_unicef_data.csv')
