from multiprocessing import Process, Manager
import requests

ALL_URLS = ['google.com', 'bing.com', 'yahoo.com',
            'twitter.com', 'facebook.com', 'github.com',
            'python.org', 'myreallyneatsiteyoushouldread.com']


def is_up_or_not(url, is_up, lock):
    resp = requests.get('http://www.isup.me/%s' % url)
    if 'is up.' in resp.content:
        is_up.append(url)
    else:
        with lock:
            print 'HOLY CRAP %s is down!!!!!' % url


def get_procs(is_up, lock):
    procs = []
    for url in ALL_URLS:
        procs.append(Process(target=is_up_or_not,
                             args=(url, is_up, lock)))
    return procs


def main():
    manager = Manager()
    is_up = manager.list()
    lock = manager.Lock()
    for p in get_procs(is_up, lock):
        p.start()
        p.join()
    print is_up

if __name__ == '__main__':
    main()
