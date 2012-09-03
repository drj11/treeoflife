#!/usr/bin/env python

# Newick format:
# http://en.wikipedia.org/wiki/Newick_format

import json
import sys

def search(node, name):
    if node['name'] == name:
        return node
    if 'children' not in node:
        return False
    for n in node['children']:
        r = search(n, name)
        if r:
            return r
    return False

def count(node):
    if 'children' not in node:
        return 1
    return 1 + sum(count(n) for n in node['children'])

class Machine:
    def __init__(self, f):
        self.f = f
        self.c = None
    def getc(self):
        if self.c:
            c = self.c
            self.c = None
        else:
            c = self.f.read(1)
        return c
    def peek(self):
        if not self.c:
            self.c = self.f.read(1)
        return self.c

def readInternal(f):
    # '(' has not been consumed.
    c = f.getc()
    assert '(' == c
    l = []
    while True:
        node = readBranch(f)
        l.append(node)
        c = f.peek()
        if ')' == c:
            break
        assert c == ','
        f.getc()
    # FOLLOW ')'
    c = f.getc()
    assert c == ')'
    name = readOptionalName(f)
    res = dict(children=l, name=name)
    return res

def readOptionalName(f):
    name = ''
    while True:
        c = f.peek()
        if c in ';:,()':
            return name
        name += c
        f.getc()
    return name

def readOptionalLength(f):
    c = f.peek()
    if c != ':':
        return None
    c = f.getc()
    assert ':' == c
    number = ''
    while True:
        c = f.peek()
        if c in '.0123456789':
            number += c
        else:
            break
    if len(number) == 0:
        raise Exception("Expected number")
    f = float(number)
    if f == int(f):
        return int(f)
    return f

def readBranch(f):
    node = readSubtree(f)
    length = readOptionalLength(f)
    if length is not None:
        node['length'] = length
    return node

def readSubtree(f):
    c = f.peek()
    if c == '(':
        return readInternal(f)
    name = readOptionalName(f)
    node = dict(name=name)
    return node

def readTree(f):
    # Grammar in wikipedia says: Subtree ; | Branch ;
    # but surely that's ambiguous?
    node = readSubtree(f)
    c = f.getc()
    assert ';' == c
    return node

def astree(f):
    lex = Machine(f)
    return readTree(lex)

def ncbi(name=None):
    """Read the NCBI newick format file and return the tree as a
    dict (with 'name' and 'children' keys).
    """
    import glob
    # http://docs.python.org/release/2.7.3/library/gzip.html
    import gzip

    if name is None:
        name = glob.glob('data/ncbi*.newick.gz')[0]
    fd = gzip.GzipFile(name)
    global NCBITree
    NCBITree = astree(fd)
    return NCBITree

def felidae(tree):
    global NCBIFelidae
    NCBIFelidae = search(tree, 'INT9681')
    return NCBIFelidae

def asjson():
    """Write out the files root.json and felidae.json."""

    root = ncbi()
    fel = felidae(root)

    json.dump(root, open('root.json', 'w'))
    # json.dump(fel, open('felidae.json', 'w'))

def main():
    """Create JSON file from default newick file."""
    json.dump(ncbi(), sys.stdout)

if __name__ == '__main__':
    main()
