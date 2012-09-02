#!/usr/bin/env python
# Extracting stuff from wikispecies

import json
import re
import urllib

class Error(Exception):
    pass

# See http://www.mediawiki.org/wiki/API:FAQ#get_the_content_of_a_page_.28wikitext.29.3F
# Example URL
wikibase = 'http://species.wikimedia.org/w/index.php'

def CommonName(title):
    """Get the (english) common name; we expect *title* to be a
    genus."""

    q = urllib.urlencode(dict(action='raw', title=title))
    url = "%s?%s" % (wikibase, q)
    section = ''.join(vernacular(urllib.urlopen(url))).replace('\n','')
    m = re.search(r'{{(.*)}}', section)
    if not m:
        raise Error("Not found")
    s = m.group(1)
    l = s.split('|')
    return [re.sub(r'^en=', '', x) for x in l if x.startswith('en')]

def vernacular(f):
    """Given a sequence of lines, yield only those in the
    vernacular section.
    """

    while True:
        l = f.next()
        if 'Vernacular' in l:
            yield l
            break
    while True:
        l = f.next()
        yield l
        if '}}' in l:
            break

def main(argv=None):
    import sys
    if argv is None:
        argv = sys.argv
    arg = argv[1:]
    for x in arg:
        try:
            print json.dumps(CommonName(x))
        except Error as m:
            print json.dumps(dict(error="%s: %s" % (x,m)))

if __name__ == '__main__':
    main()
