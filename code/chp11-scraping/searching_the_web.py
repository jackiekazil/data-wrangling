import urllib
import urllib2

google = urllib2.urlopen('http://google.com')
google = google.read()
print google[:200]

url = 'http://google.com?q='
url_with_query = url + urllib.quote_plus('python web scraping')

web_search = urllib2.urlopen(url_with_query)
web_search = web_search.read()
print web_search[:200]
