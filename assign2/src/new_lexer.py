import sys
import ply.lex as lex

keywords = {'STRUCT', 'FUNC', 'CONST', 'TYPE', 'VAR',
            'IF', 'ELSE', 'SWITCH', 'CASE', 'PRINT', 'SCAN',
            'DEFAULT', 'FOR', 'RETURN', 'BREAK', 'CONTINUE',
            'GOTO', 'PACKAGE', 'IMPORT', 'INT_T', 'FLOAT_T',
            'UINT_T', 'COMPLEX_T', 'RUNE_T', 'BOOL_T', 'STRING_T', 'TYPECAST'}

operators = {'PLUS', 'MINUS', 'STAR', 'DIVIDE', 'MOD',
            'ASSIGN', 'AND', 'LOGICAL_AND', 'INCR', 'DECR',
             'LPAREN', 'RPAREN', 'OR', 'XOR', 'LSHIFT', 'RSHIFT',
              'PLUS_ASSIGN', 'MINUS_ASSIGN', 'STAR_ASSIGN',
              'DIVIDE_ASSIGN', 'MOD_ASSIGN', 'AND_ASSIGN', 'OR_ASSIGN',
              'XOR_ASSIGN', 'LSHIFT_ASSIGN', 'RSHIFT_ASSIGN', 'LOGICAL_OR',
              'EQUALS', 'LESSER', 'GREATER', 'NOT', 'NOT_ASSIGN',
              'LESS_EQUALS', 'MORE_EQUALS', 'QUICK_ASSIGN',
              'LSQUARE', 'RSQUARE', 'LCURL',
             'RCURL', 'COMMA', 'DOT', 'SEMICOLON', 'COLON'}

reserved = {}
for r in keywords:
	reserved[r.lower()] = r

types = {'INTEGER', 'OCTAL', 'HEX', 'FLOAT', 'STRING', 'IMAGINARY', 'RUNE'}

identity = {'IDENTIFIER'}

tokens = list(operators) + list(types) + \
              list(identity) + list(reserved.values())

t_ignore_COMMENT = r'(/\*([^*]|\n|(\*+([^*/]|\n])))*\*+/)|(//.*)'
t_ignore = ' \t'
t_PLUS = r'\+'
t_MINUS = r'-'
t_STAR = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'
t_ASSIGN = r'='
t_AND = r'&'
t_LOGICAL_AND = r'&&'
t_INCR = r'\+\+'
t_DECR = r'--'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_OR = r'\|'
t_XOR = r'\^'
t_LSHIFT = r'<<'
t_RSHIFT = r'>>'
t_PLUS_ASSIGN = r'\+='
t_MINUS_ASSIGN = r'-='
t_STAR_ASSIGN = r'\*='
t_DIVIDE_ASSIGN = r'/='
t_MOD_ASSIGN = r'%='
t_AND_ASSIGN = r'&='
t_OR_ASSIGN = r'\|='
t_XOR_ASSIGN = r'\^='
t_LSHIFT_ASSIGN = r'<<='
t_RSHIFT_ASSIGN = r'>>='
t_LOGICAL_OR = r'\|\|'
t_EQUALS = r'=='
t_LESSER = r'<'
t_GREATER = r'>'
t_NOT = r'!'
t_NOT_ASSIGN = r'!='
t_LESS_EQUALS = r'<='
t_MORE_EQUALS = r'>='
t_QUICK_ASSIGN = r':='
t_LSQUARE = r'\['
t_RSQUARE = r'\]'
t_LCURL = r'\{'
t_RCURL = r'\}'
t_COMMA = r','
t_DOT = r'\.'
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
