#!/usr/bin/env python
# rank.py > data/rank.json

"""Extract the taxonomic rank from dump/nodes.dmp"""

import json
import sys

def dumprows(f):
    """Return each row as a list."""
    for line in f:
        if line.endswith('\t|\n'):
            line = line[:-3]
        yield line.split('\t|\t')

def main():
    d = {}
    for row in dumprows(open('dump/nodes.dmp')):
        if row[2] != 'no rank':
            d[row[0]] = row[2]
    json.dump(d, sys.stdout)

if __name__ == '__main__':
    main()

