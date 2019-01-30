import ply.lex as lex
import sys

keywords = {
  'BREAK', 'CASE', 'CHAN', 'CONST', 'CONTINUE', 'DEFAULT',
  'DEFER', 'ELSE', 'FALLTHROUGH', 'FOR', 'FUNC', 'GO', 'GOTO',
  'IF', 'IMPORT', 'INTERFACE', 'MAP', 'PACKAGE', 'RANGE',
  'RETURN', 'SELECT', 'STRUCT', 'SWITCH', 'TYPE', 'VAR' }

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
  'IDENT',  # main
  'INT',    # 12345
  'OCTAL',  # 017
  'HEX',    # 0x12abcd
  'FLOAT',  # 123.45
  'IMAG',   # 123.45i
  'STRING', # "abc",'abc'
  'RUNE',  # unicode_chars
  'NEWLINE',
  'SPACE',
  'TAB',
  'COMMENT'
}

tokens = list(operators) + list(types) + list(reserved.values())

# token definitions



t_COMMENT = r'(/\*([^*]|\n|(\*+([^*/]|\n])))*\*+/)|(//.*)'
# t_ignore = ' \t'
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

string_re = r'(\"[^(\")]*\")|(\'[^(\')]*\')'
rune_re = r'(\'(.|(\\[abfnrtv]))\')|(\"(.|(\\[abfnrtv]))\")'
ident_re = "[_a-zA-Z]+[a-zA-Z0-9_]*"


@lex.TOKEN("[\\n]+")
def t_NEWLINE(t):
  r'\n+'
  t.lexer.lineno += len(t.value)
  t.value = t.value.replace('\n', '<br>')
  # print(" .......newline aaya ")
  return t

@lex.TOKEN("[ ]+")
def t_SPACE(t):
	r'[ ]+'
	t.value = t.value.replace(' ', '&nbsp;')
	# print(" .......space aaya ")
	return t;

@lex.TOKEN("[\\t]+")
def t_TAB(t):
	r'\t+'
	t.value = t.value.replace('\t', '&emsp;&emsp;')
	# print(" .......tab aaya ")
	return t;


@lex.TOKEN(ident_re)
def t_IDENT(t):
  t.type = reserved.get(t.value, 'IDENT')
  return t

@lex.TOKEN(rune_re)
def t_RUNE(t):
  t.value = ord(t.value[1:-1])
  return t

@lex.TOKEN(string_re)
def t_STRING(t):
  t.value = t.value[1:-1]
  return t

@lex.TOKEN(imag_re)
def t_IMAG(t):
  t.value = complex(t.value.replace('i','j'))
  return t

@lex.TOKEN(float_re)
def t_FLOAT(t):
  t.value = float(t.value)
  return t

@lex.TOKEN(hex_re)
def t_HEX(t):
  t.value = int(t.value)
  return t

@lex.TOKEN(int_re)
def t_INT(t):
  t.value = int(t.value)
  return t



ERROR_LIST = list([])
def t_error(t):
  print("Error in lexer character")
  ERROR_LIST.append(t.value[0])
  print(t)
  t.lexer.skip(1)



print("usage : %s <cfg-file> <go-source-file> <output-html-name>" % sys.argv[0])

if len(sys.argv)==4 :
  cfg_file = sys.argv[1]
  source_file = sys.argv[2]
  html_file = sys.argv[3]
  # print(sys.argv)
  # print(cfg_file, source_file, html_file)
else :
  print("Error in command line args")
  exit(-1)

try :
  lexer = lex.lex()
  with open(source_file) as s:
    data = s.read()+"\n"
    lexer.input(data)
  # print("data = ", data)

  with open(cfg_file) as cfp:
    token_colors = {}
    for line in cfp:
        line = line.strip().split(',')
        token_colors[line[0]] = line[1]

  html_str = '''<!DOCTYPE html>\n<html>\n<head>\n<title>Token Highlighting</title>\n</head>\n<body>\n'''
  for token in lexer:
      # print(token)
      html_str += '<span style="color:{};">{}</span>'.format(token_colors[token.type], token.value)
  html_str += '''\n</body>\n</html>\n'''

  with open(html_file,"w") as h:
    h.write(html_str)
   

except IOError as e:
  print("ERROR IN LEXER",e)
  exit(-1)    
