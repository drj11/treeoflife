#!/usr/bin/env python

# Map Genus to species for monotypic genera.

import codecs
import csv
import itertools
import sys

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

def main():
    r = csv.reader(open('data/msw3-all.csv'))
    header = r.next()
    dicts = (dict(zip(header, row)) for row in r)
    # retain only species
    dicts = (d for d in dicts if d['TaxonLevel'] == 'SPECIES')
    # retain only extant species
    dicts = (d for d in dicts if d['Extinct?'] == 'False')
    for genus,subs in itertools.groupby(dicts, lambda x: x['Genus']):
        l = list(subs)
        if len(l) == 1:
            x = l[0]
            cn = unicode(x['CommonName'], 'windows-1252')
            g = unicode(x['Genus'], 'windows-1252')
            s = unicode(x['Species'], 'windows-1252')
            print g, s, cn

if __name__ == '__main__':
    main()
