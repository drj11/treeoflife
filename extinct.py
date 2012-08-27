#!/usr/bin/env python

"""Create the file data/extinct.json

Extinct taxa are represented by citing the work "extinct" (see
table dump/citations.dmp).
"""

import json
import sys

def main():
    f = open('dump/citations.dmp')
    e = extinct(f)
    json.dump(e, sys.stdout)

def extinct(f):
    for line in f:
        row = line.split('\t|\t')
        if row[1] == 'extinct':
            return dict((taxid,1) for taxid in row[6].split())

if __name__ == '__main__':
    main()
