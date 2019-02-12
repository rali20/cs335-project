# Hi, this is Rahul

# Write AST for the given grammar


import sys
import ply.yacc as yacc
import lexer


#



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

def p_type_opt(p):
    '''TypeOpt : Type
               | empty'''

# Array Types
def p_array_type(p):
    '''ArrayType : LBRACK ArrayLength RBRACK ElementType'''

def p_array_length(p):
    '''ArrayLength : Expression'''

def p_ele_type(p):
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
def p_ptr_type(p):
    '''PointerType : MUL BaseType'''

def p_base_type(p):
    '''BaseType : Type'''

# Function Types
def p_func_type(p):
    '''FunctionType : FUNC Signature'''

def p_signature(p):
    '''Signature : Parameters Result'''

def p_result(p):
    '''Result : Parameters
              | Type
              | empty'''

def p_params(p):
    '''Parameters : LPAREN  ParameterList RPAREN
                  | LPAREN  ParameterList COMMA RPAREN
                  | LPAREN empty RPAREN'''

def p_param_list(p):
    '''ParameterList : ParameterDecl ParameterListRep'''

def p_param_list_rep(p):
    '''ParameterListRep : COMMA ParameterDecl ParameterListRep
                        | empty'''

def p_param_decl(p):
    '''ParameterDecl : IdentifierListOpt EllipsisOpt Type'''

def p_ident_list_opt(p):
    '''IdentifierListOpt : IdentifierList
                         | empty'''

def p_ellipsis_opt(p):
    '''EllipsisOpt : ELLIPSIS
                   | empty'''

# Blocks
def p_block(p):
    '''Block : LBRACE StatementList RBRACE'''

def p_stmt_list(p):
    '''StatementList : StatementList Statement SEMICOLON
                     | empty'''

# Declarations and Scope
def p_decl(p):
    '''Declaration : ConstDecl
                   | TypeDecl
                   | VarDecl'''

def p_toplevel_decl(p):
    '''TopLevelDecl : Declaration
                    | FunctionDecl'''

# Constant Declarations
def p_const_decl(p):
    '''ConstDecl : CONST ConstSpec
                 | CONST LPAREN ConstSpecRep RPAREN'''

def p_const_spec_rep(p):
    '''ConstSpecRep : ConstSpecRep ConstSpec SEMICOLON
                    | empty'''

def p_const_spec(p):
    '''ConstSpec : IdentifierList TAExpListOpt'''

def p_taexp_list_opt(p):
    '''TAExpListOpt : TypeOpt ASSIGN ExpressionList
                    | empty'''

def p_ident_list(p):
    '''IdentifierList : identifier IdentComRep'''

def p_ident_com_rep(p):
    '''IdentComRep : IdentComRep COMMA identifier
                   | empty'''

def p_expr_list(p):
    '''ExpressionList : Expression ComExprRep'''

def p_com_expr_rep(p):
    '''ComExprRep : COMMA Expression ComExprRep
                  | empty'''

# Type Declarations
def p_type_decl(p):
    '''TypeDecl : TYPE TypeSpec
                | TYPE LPAREN TypeSpecRep RPAREN'''

def p_type_spec_rep(p):
    '''TypeSpecRep : TypeSpec SEMICOLON TypeSpecRep
                   | empty'''

def p_type_spec(p):
    '''TypeSpec : AliasDecl
                | TypeDef'''

# Alias Declarations
def p_alias_decl(p):
    '''AliasDecl : identifier ASSIGN Type'''

# Type Definitions
def p_type_def(p):
    '''TypeDef : identifier Type'''

# Variable Declarations
def p_var_decl(p):
    '''VarDecl : VAR VarsSpec
               | VAR LPAREN VarSpec RPAREN'''

def p_var_spec_rep(p):
    '''VarSpec : VarSpec SEMICOLON VarSpecRep
               | empty'''

def p_var_spec(p):
    '''VarSpec : IdentifierList Type ExpressionListOpt
               | IdentifierList ASSIGN ExpressionList'''

# Operand DECLARATIONS
def p_operand(p) :
    '''Operand : Literal
               | OperandName
               | LPAREN Expression RPAREN'''

def p_literal(p):
    '''Litrel : BasicLit
              | CompositeLit
              | FunctionLit'''

def p_basic_lit(p):
    '''BasicLit : int_re
                | float_re
                | imag_re
                | rune_re
                | octal_re
                | hex_re
                | ident_re
                | string_re'''

def p_operand_name(p):
    '''OperandName : identifier
                   | QualifiedIdent'''

# Qualified identifiers
def p_quali_ident(p):
    '''QualifiedIdent : PackageName DOT identifier'''

#Composite literals
def p_composit

# Function literals


#Primary Expresiions
def p_prim_expr(p):
    '''PrimaryExpr : Operand
                   | Conversion
                   | PrimaryExpr Selector
                   | PrimaryExpr Index
                   | Primary Slice
                   | Primary TypeAssertion
                   | PrimaryExpr Arguments'''

def p_selector(p):
    '''Selector : DOT identifier'''

def p_index(p):
    '''Index : LBRACK Expression RBRACK'''

def p_slice(p):
    '''Slice : LBRACK ExpressionOpt COLON ExpressionOpt RBRACK
             | LBRACK ExpressionOpt COLON Expression COLON Expression RBRACK'''

def p_type_assertion(p):
    '''TypeAssertion : DOT LPAREN Type RPAREN'''

def p_arg(p):
    '''Arguments : LPAREN ExpressionListTypeOpt RPAREN'''

#Operators
def p_expr(p):
    '''Expression : UnaryExpr
                  | Expression binary_op Expresion'''

def p_unary_expr(p):
    '''UnaryExpr
