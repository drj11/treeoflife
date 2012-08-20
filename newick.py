#!/usr/bin/env python

# Newick format:
# http://en.wikipedia.org/wiki/Newick_format

class Node:
    def __init__(self, **k):
        self.__dict__.update(k)
    def __repr__(self):
        if 'name' in self.__dict__:
            return "Node(name=%r)" % self.name
        return "Node(id=%r)" % id(self)
    def asdict(self):
        d = {}
        l = getattr(self, 'length', None)
        if l is not None:
            d['length'] = l
        if hasattr(self, 'name'):
            d['name'] = self.name
        if hasattr(self, 'children'):
            d['children'] = [n.asdict() for n in self.children]
        return d

def search(node, name):
    if node.name == name:
        return node
    if not hasattr(node, 'children'):
        return False
    for n in node.children:
        r = search(n, name)
        if r:
            return r
    return False

def count(node):
    if not hasattr(node, 'children'):
        return 1
    return 1 + sum(count(n) for n in node.children)

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
    res = Node(children=l, name=name)
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
    node.length = length
    return node

def readSubtree(f):
    c = f.peek()
    if c == '(':
        return readInternal(f)
    name = readOptionalName(f)
    node = Node(name=name)
    return node

def readTree(f):
    # Grammar in wikipedia says: Subtree ; | Branch ;
    # but surely that's ambiguous?
    node = readSubtree(f)
    c = f.getc()
    assert ';' == c
    return node

def entree(f):
    lex = Machine(f)
    return readTree(lex)

def ncbi():
    import glob
    # http://docs.python.org/release/2.7.3/library/gzip.html
    import gzip
    fn = glob.glob('ncbi*')[0]
    fd = gzip.GzipFile(fn)
    global r
    r = entree(fd)
    global f
    f = search(r, 'INT9681')

def asjson():
    import json

    json.dump(r.asdict(), open('root.json', 'w'))
    json.dump(f.asdict(), open('felidae.json', 'w'))

def main():
    pass

if __name__ == '__main__':
    main()
