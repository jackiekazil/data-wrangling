import dataset
from get_zipped_data import get_zipped_data

db = dataset.connect('sqlite:///data_wrangling.db')

table = db['unicef_survey']

for row_num, data in enumerate(get_zipped_data()):
    for question, answer in data:
        data_dict = {
            'question': question[1],
            'question_code': question[0],
            'answer': answer,
            'response_number': row_num,
            'survey': 'mn',
        }
    table.insert(data_dict)
