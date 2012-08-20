#!/usr/bin/env python
# David Jones - drj@climatecode.org


# Uses PLY: http://www.dabeaz.com/ply/README.txt
# Parses Newick format: http://en.wikipedia.org/wiki/Newick_format

tokens = (
    'PAR', 'REN', 'COMMA', 'COLON', 'SEMIC', 'STRING'
    )
t_PAR = r'\('
t_REN = r'\)'
t_COMMA = ','
t_COLON = ':'
t_SEMIC = ';'
t_STRING = '[a-zA-Z_0-9]+'

t_ignore = ' \t'

def t_error(t):
    print "Illegal character %r" % t.value[0]
    t.lexer.skip(1)

import ply.lex as lex
lex.lex()

def p_tree(p):
    'tree : subtree SEMIC'
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
    'internal : PAR branchset REN name'
    p[0] = dict(children=p[2], name=p[4])

def p_branchset(p):
    '''branchset : branch
                 | branchset COMMA branch'''
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
              | COLON STRING'''
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
