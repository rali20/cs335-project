import ply.lex as lex

# Removed 
# INTERFACE, FALLTHROUGH, DEFER, 
# CHAN, RANGE, GO, SELECT, MAP

keywords = {
  'BREAK', 'CASE', 'CONST', 'CONTINUE', 'DEFAULT',
	'ELSE', 'FOR', 'FUNC', 'GOTO', 'IF', 'IMPORT', 
	'PACKAGE', 'RETURN', 'STRUCT', 'SWITCH', 
	'TYPE', 'VAR' }
	# Added
	#'INT', 'FLOAT', 'UINT', 'COMPLEX', 'BOOL',
	#'STRING', 'RUNE'

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
  'IDENTIFIER',  # main
  'INT_LIT',    # 12345
  'OCTAL',  # 017
  'HEX',    # 0x12abcd
  'FLOAT_LIT',  # 123.45
  'IMAG',   # 123.45i
  'STRING_LIT', # "abc",'abc'
  'RUNE_LIT',  	# unicode_chars
  'COMMENT'	#//
}

tokens = list(operators) + list(types) + list(reserved.values())


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
int_re = "(0|([1-9][0-9]*))"
octal_re = "(0[0-7]*)"
hex_re = "(0x|0X)[0-9a-fA-F]+"

# float based regex
float_re = "[0-9]*\.[0-9]+([eE][-+]?[0-9]+)?"

imag_re = "(" + int_re + "|" + float_re + ")i"

string_re = r'(\"[^\"]*\")|(\'[^\']*\')'
rune_re = r'(\'(.|(\\[abfnrtv]))\')|(\"(.|(\\[abfnrtv]))\")'
identifier_re = "[_a-zA-Z]+[a-zA-Z0-9_]*"
comment_re = r'(/\*([^*]|\n|(\*+([^*/]|\n])))*\*+/)|(//.*)'

@lex.TOKEN(string_re)
def t_STRING_LIT(t):
  t.value = t.value[0:]
  return t

@lex.TOKEN(identifier_re)
def t_IDENTIFIER(t):
  t.type = reserved.get(t.value, 'IDENTIFIER')
  return t

@lex.TOKEN(rune_re)
def t_RUNE_LIT(t):
  t.value = ord(t.value[1:-1])
  return t

@lex.TOKEN("[\\n]+")
def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)

@lex.TOKEN(imag_re)
def t_IMAG(t):
  t.value = complex(t.value.replace('i','j'))
  return t

@lex.TOKEN(float_re)
def t_FLOAT_LIT(t):
  t.value = float(t.value)
  return t

@lex.TOKEN(hex_re)
def t_HEX(t):
  t.value = int(t.value,16)
  return t

@lex.TOKEN(octal_re)
def t_OCTAL(t):
  t.value = int(t.value,8)
  return t

@lex.TOKEN(int_re)
def t_INT_LIT(t):
  t.value = int(t.value,10)
  return t


ERROR_LIST = list([])
def t_error(t):
  print("Error in lexer character")
  ERROR_LIST.append(t.value[0])
  print(t)
  t.lexer.skip(1)
