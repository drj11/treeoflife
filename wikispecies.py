#!/usr/bin/env python
# Extracting stuff from wikispecies

import itertools
import json
import re
import urllib

class Error(Exception):
    pass

# See http://www.mediawiki.org/wiki/API:FAQ#get_the_content_of_a_page_.28wikitext.29.3F
# Example URL
wikibase = 'http://species.wikimedia.org/w/index.php'

def raw(title):
    """Return the raw wiki markup for a page.  Returns a list of
    strings."""

    q = urllib.urlencode(dict(action='raw', title=title))
    url = "%s?%s" % (wikibase, q)
    body = urllib.urlopen(url).readlines()

    return body

def getInfo(title):
    """From a title (species or genus), get a variety of
    information: the (english) common name; list of species.
    """

    res = {}

    body = raw(title)

    res['vernacular'] = vernacular(body)

    res.update(species(body))
    return res

def species(body):
    """Extract species.  A dict is returned with a list of
    extant species in the key 'extant', and a list of extinct
    species in the key 'extinct'.
    """

    res = dict(extant=[], extinct=[])

    ssection = [line for line in section('Taxonavigation', body)
      if line.startswith('Species')]
    # This has to be unicode to find the \u2020 (dagger)
    # character, but I have no idea if it is.
    for specie in itertools.chain(
      *(re.findall(r'[^\s]?{{.*?}}', line) for line in ssection)):
        if specie.startswith('{{'):
            l = res['extant']
        else:
            l = res['extinct']
        # By examination of one example (Macrotis), the text between
        # the {{ }} appears to be:
        # {{sp|M|acrotis|lagotis}}
        # Oh yukh.  Completely different for Dinomys:
        # Species: ''[[Dinomys branickii]]''
        t = re.search('{{sp.*?[|](.*)}}', specie).group(1)
        s = t.replace('|', '', 1).replace('|', ' ')
        l.append(s)
    return res

def vernacular(body):
    """Extract (english) vernacular, common name.  A list is
    returned (which is empty when there are no common names).
    """
    vsection = ''.join(section('Vernacular', body)).replace('\n','')
    m = re.search(r'{{(.*)}}', vsection)
    if not m:
        return []
    s = m.group(1)
    l = s.split('|')
    v = [re.sub(r'^en=', '', x) for x in l if x.startswith('en')]
    return v

def section(name, f):
    """Given a sequence of lines, yield only those in the
    section named *name*.
    """

    f = iter(f)

    while True:
        l = f.next()
        if l.startswith('=') and name in l:
            yield l
            break
    while True:
        l = f.next()
        if l.startswith('='):
            break
        yield l

def main(argv=None):
    import getopt
    import sys
    if argv is None:
        argv = sys.argv
    command = 'info'
    opts,arg = getopt.getopt(argv[1:], '', ['raw'])
    for o,v in opts:
        if o == '--raw':
            command = 'raw'
    for x in arg:
        try:
            if command == 'info':
                info = getInfo(x)
                print json.dumps(info['vernacular'])
                if len(info['extant']) == 1:
                    print '  monotypic'
            if command == 'raw':
                print ''.join(raw(x))
        except Error as m:
            print json.dumps(dict(error="%s: %s" % (x,m)))

if __name__ == '__main__':
    main()
