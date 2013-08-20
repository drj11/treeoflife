#!/usr/bin/env python

import json
import os

"""Recreate part of the tree of life as a file hierarchy."""

def mk(node, name):
    """Recursively make directories."""
    children = node.get('children')
    filename = name[node['name']]['scientific']
    if not children:
        open(filename, 'w').close()
        return
    os.mkdir(filename)
    os.chdir(filename)
    for n in children:
        mk(n, name)
    os.chdir('..')

def search(needle, haystack):
    if haystack['name'] == needle:
        return haystack
    children = haystack.get('children')
    if not children:
        return
    for child in children:
        gotit = search(needle, child)
        if gotit:
            return gotit

def main(argv=None):
    import sys
    if argv is None:
        argv = sys.argv

    arg = argv[1:]
    if len(arg) > 0:
        root = arg[0]
    else:
        root = "9681" # Felidae

    with open('data/ncbi.json') as ncbi:
      with open('data/name.json') as name:
        ncbi = json.load(ncbi)
        name = json.load(name)
        start = search(root, ncbi)
        mk(start, name)
      

if __name__ == '__main__':
    main()
