import ply.lex as lex

keywords = {
    'BREAK', 'CONST', 'CONTINUE', 'ELIF',
    'ELSE', 'FOR', 'FUNC', 'GOTO',
    'IF', 'RETURN', 'STRUCT', 'TYPE',
    'VAR' }

operators = {
    'ADD',  # +
    'SUB',  # -
    'MUL',  # *
    'QUO',  # /
    'REM',  # %

    'AND',  # &
    'OR', # |
    'SHL',  # <<
    'SHR',  # >>
    'AGN',  # =
    'NOT',  # !

    'LAND', # &&
    'LOR',  # ||
    'EQL',  # ==
    'LSS',  # <
    'GTR',  # >
    'NEQ',  # !=
    'LEQ',  # <=
    'GEQ',  # >=
    'DEFN',   # :=

    'LPRN', # (
    'LSQR', # [
    'LCURL',  # {
    # 'LPRN_OR',  # (|
    'COMMA',  # ,
    'DOT',  # .

    'RPRN',    # )
    'RSQR',    # ]
    'RCURL',    # }
    # 'RPRN_OR',  # |)
    'SEMCLN',  # ;
    'COLON'     # :
}

reserved = {}
for r in keywords:
    reserved[r.lower()] = r

types = {'INTEGER_LIT', 'FLOAT_LIT',
        'STRING_LIT', 'IDENT'}

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
t_SHL = r'<<'
t_SHR = r'>>'
t_LAND = r'&&'
t_LOR = r'\|\|'
t_EQL = r'=='
t_LSS = r'<'
t_GTR = r'>'
t_AGN = r'='
t_NOT = r'!'
t_NEQ = r'!='
t_LEQ = r'<='
t_GEQ = r'>='
t_DEFN = r':='
t_LPRN = r'\('
t_LSQR = r'\['
t_LCURL = r'\{'
# t_LPRN_OR = r'\(\|'
t_COMMA = r','
t_DOT = r'\.'
t_RPRN = r'\)'
t_RSQR = r'\]'
t_RCURL = r'\}'
# t_RPRN_OR = r'\|\)'
t_SEMCLN = r';'
t_COLON = r':'

decimal_lit = r"(0|([1-9][0-9]*))"
float_lit = r"[0-9]*\.[0-9]+([eE][-+]?[0-9]+)?"

string_lit = r"""("[^"]*")|('[^']*')"""
identifier_lit = r"[_a-zA-Z]+[a-zA-Z0-9_]*"

@lex.TOKEN(identifier_lit)
def t_IDENT(t):
    t.type = reserved.get(t.value, 'IDENT')
    return t

@lex.TOKEN(string_lit)
def t_STRING_LIT(t):
    t.value = t.value[1:-1]
    return t

@lex.TOKEN(float_lit)
def t_FLOAT_LIT(t):
    t.value = float(t.value)
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
