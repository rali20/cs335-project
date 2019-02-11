# Hi, this is Rahul

import sys
import ply.yacc as yacc
import lexer


# Source
def p_start(p):
    '''start : SourceFile'''

# Types
def p_type(p):
    '''Type : TypeName
            | TypeList
            | LPAREN Type RPAREN'''

def p_type_name(p):
    '''TypeName : identifier | QualifiedIdent'''

def p_type_lit(p):
    '''TypeLit = ArrayType
               | StructType
               | PointerType
               | FunctionType'''

# Array Types
def p_array_type(p):
    '''ArrayType : LBRACK ArrayLength RBRACK ElementType'''

def p_array_length(p):
    '''ArrayLength : Expression'''

def p_element_type(p):
    '''ElementType : Type'''

# Struct Types
def p_struct_type(p):
    '''StructType : STRUCT LBRACE FieldDeclRep RBRACE'''

def p_field_decl_rep(p):
    '''FieldDeclRep : FieldDeclRep FieldDecl SEMICOLON
                    | empty'''

def p_field_decl(p):
    '''FieldDecl : IdentifierList Type'''

# Pointer Type
def p_pointer_type(p):
    '''PointerType : MUL BaseType'''

def p_base_type(p):
    '''BaseType : Type'''

# Function Types
def p_function_type(p):
    '''FunctionType : FUNC Signature'''

def p_signature(p):
    '''Signature : Parameters Result'''

def p_result(p):
    '''Result : Parameters
              | Type
              | empty'''

def p_parameters(p):
    '''Parameters : LPAREN  ParameterList RPAREN
                  | LPAREN  ParameterList COMMA RPAREN
                  | LPAREN empty RPAREN'''

def p_parameter_list_opt(p):
    '''ParameterListOpt :
