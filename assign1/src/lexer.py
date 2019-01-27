import sys
import re
import ply.lex as lex

keywords =
{
  'BREAK', 'CASE', 'CHAN', 'CONST', 'CONTINUE', 'DEFAULT',
  'DEFER', 'ELSE', 'FALLTHROUGH', 'FOR', 'FUNC', 'GO', 'GOTO',
  'IF', 'IMPORT', 'INTERFACE', 'MAP', 'PACKAGE', 'RANGE',
  'RETURN', 'SELECT', 'STRUCT', 'SWITCH', 'TYPE', 'VAR'
}

operators =
{
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

	'LPAREN', # (
	'LBRACK', # [
	'LBRACE', # {
	'COMMA',  # ,
	'PERIOD', # .

	'RPAREN',    # )
	'RBRACK',    # ]
	'RBRACE',    # }
	'SEMICOLON', # ;
	'COLON'     # :
}

reserved = dict({})

for r in keywords :
  reserved[r.lower()] = r

types = {
'IDENT',  # main
'INT',    # 12345
'OCTAL',  # 017
'HEX',    # 0x12abcd
'FLOAT',  # 123.45
'IMAG',   # 123.45i
'STRING' # "abc",'abc'
'RUNE'  # unicode_chars
}

tokens = list(operators) + list(types) + list(reserved.values())

# token definitions

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
t_LPAREN = r'\('
t_LBRACK = r'\['
t_LBRACE = r'\{'
t_COMMA = r','
t_PERIOD = r'\.'
t_RPAREN = r'\)'
t_RBRACK = r'\]'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_COLON = r':'

# integer based regex
decimal_re = "(0|([1-9][0-9]*))"
octal_re = "(0[0-7]*)"
hex_re = "(0x|0X)[0-9a-fA-F]+" 

# float based regex
float_re = "[0-9]*\.[0-9]+([eE][-+]?[0-9]+)?"

imaginary_re = "(" + decimal_re + "|" + float_re + ")i"

string_re = r'(\"[^(\")]*\")|(\'[^(\')]*\')'
rune_re = r'(\'(.|(\\[abfnrtv]))\')|(\"(.|(\\[abfnrtv]))\")'
identifier_re = "[_a-zA-Z]+[a-zA-Z0-9_]*"


