#!/usr/bin/env python
# handle ncbi dump files.

import json
import sys

def rows(inp):
    """Convert dump file *inp* (which can be any iterator that
    yields lines) into a generator of rows, where each row is a
    list.
    """
    for line in inp:
        if line.endswith('\t|\n'):
            line = line[:-3]
        l = line.split('\t|\t')
        yield l

def build_tree(d):
    """*d* is a dict mapping node id (a taxid) to the row (as a
    list) in the dump file."""

    # For each node, a list of its children.
    ch = dict((k,[]) for k in d)
    for k,v in d.items():
        parent = v[1]
        ch[parent].append(k)
        if k.endswith('00zz'):
            sys.stdout.write('\r%s' % k)
    # for some reason, the parent of 1 is 1.  remove it.
    ch['1'].remove('1')
    return mktree(ch, '1')

def mktree(ch, at):
    """Recursively construct tree as a dict.  *ch* is the dict
    that gives child nodes, *at* is the root of the desired
    tree.
    """

    res = dict(name=at)
    children = [mktree(ch, child) for child in ch[at]]
    if children:
        res['children'] = children
    return res


def main():
    f = open('dump/nodes.dmp')
    d = dict((row[0], row) for row in rows(f))
    tree = build_tree(d)
    json.dump(tree, sys.stdout)

if __name__ == '__main__':
    main()
