import sys
import ply.lex as lex

keywords = {
    'BREAK', 'CASE', 'CONST', 'CONTINUE', 'DEFAULT',
    'DEFER', 'ELSE', 'FALLTHROUGH', 'FOR', 'FUNC',
    'GOTO', 'IF', 'IMPORT', 'INTERFACE', 'MAP',
    'PACKAGE', 'RANGE', 'RETURN', 'STRUCT',
    'SWITCH', 'TYPE', 'VAR' }

operators = {
    'ADD',  # +
    'SUB',  # -
    'MUL',  # *
    'QUO',  # /
    'REM',  # %

    'AND',     # &
    'OR',      # |
    'XOR',     # ^
    'SHL',     # <<
    'SHR',     # >>
    'AND_NOT',   # &^

    'ADD_AGN',  # +=
    'SUB_AGN',  # -=
    'MUL_AGN',  # *=
    'QUO_AGN',  # /=
    'REM_AGN',  # %=

    'AND_AGN',     # &=
    'OR_AGN',      # |=
    'XOR_AGN',     # ^=
    'SHL_AGN',     # <<=
    'SHR_AGN',     # >>=
    'AND_NOT_AGN',  # &^=

    'LAND',  # &&
    'LOR',   # ||
    'INC',   # ++
    'DEC',   # --

    'EQL',    # ==
    'LSS',    # <
    'GTR',    # >
    'AGN',  # =
    'NOT',    # !

    'NEQ',      # !=
    'LEQ',      # <=
    'GEQ',      # >=
    'DEFN',   # :=
    'ELPS', # ...

    'LPRN',  # (
    'LSQR',  # [
    'LCURL',  # {
    'LPRN_OR',  # (|
    'COMMA',  # ,
    'DOT',  # .

    'RPRN',    # )
    'RSQR',    # ]
    'RCURL',    # }
    'RPRN_OR',  # |)
    'SEMCLN',  # ;
    'COLON'     # :
}

reserved = {}
for r in keywords:
    reserved[r.lower()] = r

types = {'INTEGER_LIT', 'OCTAL_LIT', 'HEX_LIT', 'FLOAT_LIT',
         'STRING_LIT', 'IMAGINARY_LIT', 'RUNE_LIT', 'IDENT'}

tokens = list(operators) \
    + list(types) + list(reserved.values())

t_ignore_COMMENT = r'(/\*([^*]|\n|(\*+([^*/]|\n])))*\*+/)|(//.*)'
t_ignore = ' \t'
t_ADD = r'\+'
t_SUB = r'-'
t_MUL = r'\*'
t_QUO = r'/'
t_REM = r'%'
t_AND = r'&'
t_OR = r'\|'
t_XOR = r'\^'
t_SHL = r'<<'
t_SHR = r'>>'
t_AND_NOT = r'&\^'
t_ADD_AGN = r'\+='
t_SUB_AGN = r'-='
t_MUL_AGN = r'\*='
t_QUO_AGN = r'/='
t_REM_AGN = r'%='
t_AND_AGN = r'&='
t_OR_AGN = r'\|='
t_XOR_AGN = r'\^='
t_SHL_AGN = r'<<='
t_SHR_AGN = r'>>='
t_AND_NOT_AGN = r'&\^='
t_LAND = r'&&'
t_LOR = r'\|\|'
t_INC = r'\+\+'
t_DEC = r'--'
t_EQL = r'=='
t_LSS = r'<'
t_GTR = r'>'
t_AGN = r'='
t_NOT = r'!'
t_NEQ = r'!='
t_LEQ = r'<='
t_GEQ = r'>='
t_DEFN = r':='
t_ELPS = r'\.\.\.'
t_LPRN = r'\('
t_LSQR = r'\['
t_LCURL = r'\{'
t_LPRN_OR = r'\(\|'
t_COMMA = r','
t_DOT = r'\.'
t_RPRN = r'\)'
t_RSQR = r'\]'
t_RCURL = r'\}'
t_RPRN_OR = r'\|\)'
t_SEMCLN = r';'
t_COLON = r':'

decimal_lit = "(0|([1-9][0-9]*))"
octal_lit = "(0[0-7]*)"
hex_lit = "(0x|0X)[0-9a-fA-F]+"
float_lit = "[0-9]*\.[0-9]+([eE][-+]?[0-9]+)?"

string_lit = """("[^"]*")"""
rune_lit = "\'(.|(\\[abfnrtv]))\'"
identifier_lit = "[_a-zA-Z]+[a-zA-Z0-9_]*"

imaginary_lit = "(" + decimal_lit + "|" + float_lit + ")i"


@lex.TOKEN(identifier_lit)
def t_IDENT(t):
    t.type = reserved.get(t.value, 'IDENT')
    return t


@lex.TOKEN(rune_lit)
def t_RUNE(t):
    t.value = ord(t.value[1:-1])
    return t


@lex.TOKEN(string_lit)
def t_STRING_LIT(t):
    t.value = t.value[1:-1]
    return t


@lex.TOKEN(imaginary_lit)
def t_IMAGINARY_LIT(t):
    t.value = complex(t.value.replace('i', 'j'))
    return t


@lex.TOKEN(float_lit)
def t_FLOAT_LIT(t):
    t.value = float(t.value)
    return t


@lex.TOKEN(hex_lit)
def t_HEX_LIT(t):
    t.value = int(t.value, 16)
    # t.type = 'INTEGER_LIT'
    return t


@lex.TOKEN(octal_lit)
def t_OCTAL_LIT(t):
    t.value = int(t.value, 8)
    # t.type = 'INTEGER_LIT'
    return t


@lex.TOKEN(decimal_lit)
def t_INTEGER_LIT(t):
    t.value = int(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal Character")
    t.lexer.skip(1)


lexer = lex.lex()
