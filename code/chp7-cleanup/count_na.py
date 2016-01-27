from updated_zip_rows import zipped_data

na_count = {}
for row in zipped_data:
    for resp in row:
        question = resp[0][1]
        answer = resp[1]
        if answer == 'NA':
            if question in na_count.keys():
                na_count[question] += 1
            else:
                na_count[question] = 1

print na_count
