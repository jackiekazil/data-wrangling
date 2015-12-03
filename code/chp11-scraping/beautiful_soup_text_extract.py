from bs4 import BeautifulSoup
import requests

page = requests.get('http://www.enoughproject.org/take_action')

bs = BeautifulSoup(page.content)
ta_divs = bs.find_all("div", class_="views-row")

all_data = []

for ta in ta_divs:
    data_dict = {}
    data_dict['title'] = ta.h2.get_text()
    data_dict['link'] = ta.a.get('href')
    data_dict['about'] = [p.get_text() for p in ta.find_all('p')]
    all_data.append(data_dict)

print all_data
