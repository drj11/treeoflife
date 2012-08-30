#!/usr/bin/env python

"""
Prunes ncbi.json file by removing nodes that have
the GenBank hidden flag set.

A node is pruned if it is a hidden node and all its
descendents are hidden (this is much less drastic, and seems
to give better trees, than the original strategy of pruning all
hidden nodes).
"""

import json
import sys

def open_hidden():
    """Open data/nodes.dmp and return a set of all hidden
    nodes."""

    r = set()
    for row in rows(open('dump/nodes.dmp')):
        if int(row[10]):
            r.add(row[0])
    return r
        
def rows(inp):
    for line in inp:
        if line.endswith('\t|\n'):
            line = line[:-3]
        l = line.split('\t|\t')
        yield l

def remove_hidden(n, hidden):
    """Remove any nodes from n that have names in the set
    *hidden*.  Result may share structure with *n*, but *n* will
    not be modified.
    """
    name = n['name']
    if name.startswith('INT'):
        name = name[3:]
    n = dict(n)
    if 'children' not in n:
        n['children'] = []
    children = []
    for c in n['children']:
        r = remove_hidden(c, hidden)
        if r:
            children.append(r)
    n['children'] = children
    if name in hidden and not children:
        return None
    if not children:
        del n['children']
    return n

def remove_single(n):
    """Remove all nodes that have only a single child (by
    reattaching the child to the parent).
    """
    if 'children' not in n:
        return n
    if len(n['children']) == 1:
        return remove_single(n['children'][0])
    n = dict(n)
    n['children'] = map(remove_single, n['children'])
    return n

def main():
    n = json.load(open('data/ncbi.json'))
    hidden = open_hidden()
    pruned = remove_hidden(n, hidden)
    json.dump(pruned, sys.stdout)

if __name__ == '__main__':
   main()
