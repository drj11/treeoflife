#!/usr/bin/env python
# David Jones - drj@climatecode.org


# Uses PLY: http://www.dabeaz.com/ply/README.txt
# Parses Newick format: http://en.wikipedia.org/wiki/Newick_format

tokens = [
    'STRING'
    ]
# http://www.dabeaz.com/ply/ply.html#ply_nn26
literals = list('(),:;')
t_STRING = '[a-zA-Z_0-9]+'

t_ignore = ' \t\n'

def t_error(t):
    print "Illegal character %r" % t.value[0]
    t.lexer.skip(1)

import ply.lex as lex
lex.lex()

def p_tree(p):
    """tree : subtree ';'"""
    p[0] = p[1]

def p_subtree(p):
    '''subtree : leaf
               | internal'''
    if isinstance(p[1], dict):
        p[0] = p[1]
    else:
        p[0] = dict(children=[], name=p[1])

def p_leaf(p):
    'leaf : name'
    p[0] = p[1]

def p_internal(p):
    """internal : '(' branchset ')' name"""
    p[0] = dict(children=p[2], name=p[4])

def p_branchset(p):
    '''branchset : branch
                 | branchset ',' branch'''
    if len(p) > 2:
        assert p[2] == ','
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_branch(p):
    'branch : subtree length'
    p[0] = p[1]
    p[0]['length'] = p[2]


def p_name(p):
    '''name :
            | STRING'''
    
    if len(p) > 1 and p[1]:
        p[0] = p[1]
    else:
        p[0] = None

def p_length(p):
    '''length :
              | ':' STRING'''
    if len(p) > 1:
        assert p[1] == ':'
        p[0] = float(STRING)
    else:
        p[0] = None

def p_error(p):
    print "Syntax error at %r" % p.value

import ply.yacc as yacc
yacc.yacc()

print yacc.parse('(,,(,));')
import gzip
s = gzip.GzipFile('ncbi_complete_with_taxIDs.newick.gz').read()
# Takes about 1 minute
print yacc.parse(s)
