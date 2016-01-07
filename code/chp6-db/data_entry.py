import dataset
db = dataset.connect('sqlite:///data_wrangling.db')

my_data_source = {
    'url':
    'http://www.tsmplug.com/football/premier-league-player-salaries-club-by-club/',
    'description': 'Premier League Club Salaries',
    'topic': 'football',
    'verified': False,
}

table = db['data_sources']
table.insert(my_data_source)

another_data_source = {
    'url':
    'http://www.premierleague.com/content/premierleague/en-gb/players/index.html',
    'description': 'Premier League Stats',
    'topic': 'football',
    'verified': True,
}

table.insert(another_data_source)
sources = db['data_sources'].all()

print sources
