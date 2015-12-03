import requests
import urllib2


resp = requests.get('http://sisinmaru.blog17.fc2.com/')

if resp.status_code == 404:
    print 'Oh no!!! We cannot find Maru!!'
elif resp.status_code == 500:
    print 'Oh no!!! It seems Maru might be overloaded.'
elif resp.status_code in [403, 401]:
    print 'Oh no!! You cannot have any Maru!'


try:
    resp = urllib2.urlopen('http://sisinmaru.blog17.fc2.com/')
except urllib2.URLError:
    print 'Oh no!!! We cannot find Maru!!'
except urllib2.HTTPError, err:
    if err.code == 500:
        print 'Oh no!!! It seems Maru might be overloaded.'
    elif err.code in [403, 401]:
        print 'Oh no!! You cannot have any Maru!'
    else:
        print 'No Maru for you! %s' % err.code
except Exception as e:
    print e
