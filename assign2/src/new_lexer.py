import sys
import ply.lex as lex

keywords = {
    'BREAK', 'CASE', 'CONST', 'CONTINUE', 'DEFAULT',
	'ELSE', 'FOR', 'FUNC', 'GOTO', 'IF', 'IMPORT',
	'PACKAGE', 'RETURN', 'STRUCT', 'SWITCH',
	'TYPE', 'VAR',
    'INT_T', 'FLOAT_T', 'UINT_T', 'COMPLEX_T',
    'RUNE_T', 'BOOL_T', 'STRING_T', 'TYPECAST' }

operators = {
	'ADD', # +
	'SUB', # -
	'MUL', # *
	'QUO', # /
	'REM', # %

	'AND',     # &
	'OR',      # |
	'XOR',     # ^
	'SHL',     # <<
	'SHR',     # >>
	'AND_NOT', # &^

	'ADD_ASSIGN', # +=
	'SUB_ASSIGN', # -=
	'MUL_ASSIGN', # *=
	'QUO_ASSIGN', # /=
	'REM_ASSIGN', # %=

	'AND_ASSIGN',     # &=
	'OR_ASSIGN',      # |=
	'XOR_ASSIGN',     # ^=
	'SHL_ASSIGN',     # <<=
	'SHR_ASSIGN',     # >>=
	'AND_NOT_ASSIGN', # &^=

	'LAND',  # &&
	'LOR',   # ||
	'ARROW', # <-
	'INC',   # ++
	'DEC',   # --

	'EQL',    # ==
	'LSS',    # <
	'GTR',    # >
	'ASSIGN', # =
	'NOT',    # !

	'NEQ',      # !=
	'LEQ',      # <=
	'GEQ',      # >=
	'DEFINE',   # :=
	'ELLIPSIS', # ...

	'LPRN', # (
	'LSQR', # [
	'LCURL', # {
	'COMMA',  # ,
	'DOT', # .

	'RPRN',    # )
	'RSQR',    # ]
	'RCURL',    # }
	'SEMICOLON', # ;
	'COLON'     # :
}

reserved = {}
for r in keywords:
	reserved[r.lower()] = r

types = {'INTEGER', 'OCTAL', 'HEX', 'FLOAT', 'STRING', 'IMAGINARY', 'RUNE'}

identity = {'IDENTIFIER'}

tokens = list(operators) + list(types) + \
              list(identity) + list(reserved.values())

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
t_ADD_ASSIGN = r'\+='
t_SUB_ASSIGN = r'-='
t_MUL_ASSIGN = r'\*='
t_QUO_ASSIGN = r'/='
t_REM_ASSIGN = r'%='
t_AND_ASSIGN = r'&='
t_OR_ASSIGN = r'\|='
t_XOR_ASSIGN = r'\^='
t_SHL_ASSIGN = r'<<='
t_SHR_ASSIGN = r'>>='
t_AND_NOT_ASSIGN = r'&\^='
t_LAND = r'&&'
t_LOR = r'\|\|'
t_ARROW = r'<-'
t_INC = r'\+\+'
t_DEC = r'--'
t_EQL = r'=='
t_LSS = r'<'
t_GTR = r'>'
t_ASSIGN = r'='
t_NOT = r'!'
t_NEQ = r'!='
t_LEQ = r'<='
t_GEQ = r'>='
t_DEFINE = r':='
t_ELLIPSIS = r'\.\.\.'
t_LPRN = r'\('
t_LSQR = r'\['
t_LCURL = r'\{'
t_COMMA = r','
t_DOT = r'\.'
t_RPRN = r'\)'
t_RSQR = r'\]'
t_RCURL = r'\}'
t_SEMICOLON = r';'
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
def t_IDENTIFIER(t):
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

@lex.TOKEN(rune_lit)
def t_RUNE(t):
    t.value = ord(t.value[1:-1])
    return t

@lex.TOKEN(string_lit)
def t_STRING(t):
    t.value = t.value[1:-1]
    return t

@lex.TOKEN(imaginary_lit)
def t_IMAGINARY(t):
    t.value = complex(t.value.replace('i', 'j'))
    return t

@lex.TOKEN(float_lit)
def t_FLOAT(t):
    t.value = float(t.value)
    return t

@lex.TOKEN(hex_lit)
def t_HEX(t):
    t.value = int(t.value, 16)
    return t

@lex.TOKEN(octal_lit)
def t_OCTAL(t):
    t.value = int(t.value, 8)
    return t

@lex.TOKEN(decimal_lit)
def t_INTEGER(t):
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal Character")
    t.lexer.skip(1)

lexer = lex.lex()
