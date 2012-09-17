#!/usr/bin/env python

from newick import search

"""Display as tree, ptree style."""

def tree(t, name, indent=0):
    id = t['name']
    print "%s%8s %s" % ("  " * indent, id, name[id]['scientific'])
    if 'children' not in t:
        return
    for c in t['children']:
        tree(c, name, indent+1)

def main(argv=None):
    import getopt
    import json
    import sys

    target = None

    if argv is None:
        argv = sys.argv
    opts,arg = getopt.getopt(argv[1:], '', 'root=')
    for k,v in opts:
        if k == '--root':
            target = v
    t = json.load(open('data/ncbi.json'))
    if target:
        t = search(t, target)
    n = json.load(open('data/name.json'))
    tree(t, n)

if __name__ == '__main__':
    main()
