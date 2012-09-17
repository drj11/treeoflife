#!/usr/bin/env python
# coding:utf-8
# monotyp.py > data/msw-common.json

"""Map Genus to species for monotypic genera."""

# The CSV file appears to be using Windows-1252 encoding, though
# this is undocumented.  It is common to see a mixture of
# \u2019 and \x27 for apostrophe.  As in "Salim Ali’s Fruit Bat"
# and "Bulmer's Fruit Bat".
# And just to keep you on your toes, there exists at least one species
# with non-ascii in the specific name: Leimacomys büttneri (this species
# does not seem to appear in the NCBI database).

import csv
import itertools
import json
import sys

def main():
    res = {}
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
            res[g] = dict(species=s, vernacular=cn)
    json.dump(res, sys.stdout)

if __name__ == '__main__':
    main()
