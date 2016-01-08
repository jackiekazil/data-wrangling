import pygal

# NOTE: you'll need the 'ranked' table from Chp 9 with the ISO codes added
# (see: add_iso_data.py)

worldmap_chart = pygal.Worldmap()
worldmap_chart.title = 'Child Labor Worldwide'

cl_dict = {}
for r in ranked.rows:
    cl_dict[r.get('country_code_complete').lower()] = r.get('Total (%)')

worldmap_chart.add('Total Child Labor (%)', cl_dict)
worldmap_chart.render()
