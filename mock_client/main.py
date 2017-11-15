import random
import time
import urllib2
import string
import os


def next_id():
    return str(random.randrange(1, 13))


if __name__ == '__main__':
    base = string.Template("http://$HOST_PORT/owners/").substitute(os.environ)
    while True:
        try:
            url = base + next_id()
            urllib2.urlopen(url)
            time.sleep(random.randrange(1, 10))
        except urllib2.HTTPError:
            continue
        except Exception as e:
            print 'Invalid URL ', url, e
            break
