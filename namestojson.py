#!/usr/bin/env python
# nametojson.py > data/name.json

import itertools
import json
import sys

def names(inp, out):
    r = {}
    for taxid,group in itertools.groupby(rows(inp), lambda r: r[0]):
        d = {}
        for _,name,_,class_ in group:
            if class_ == 'genbank common name':
                d['genbank'] = name
            if class_ == 'common name':
                d['common'] = name
            if class_ == 'scientific name':
                d['scientific'] = name
        r[taxid] = d
    json.dump(r, out, indent=2)

def rows(inp):
    for line in inp:
        if line.endswith('\t|\n'):
            line = line[:-3]
        l = line.split('\t|\t')
        yield l

def main():
    with open('dump/names.dmp') as f:
        names(f, sys.stdout)

if __name__ == '__main__':
    main()
