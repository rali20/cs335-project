# TODO : Write AST for the given grammar

import sys
import ply.yacc as yacc
import ply.lex as lex
from lex_rules import *

precedence = (
    ('right','ASSIGN', 'NOT'),
    ('left', 'LOR'),
    ('left', 'LAND'),
    ('left', 'OR'),
    ('left', 'XOR'),
    ('left', 'AND'),
    ('left', 'EQL', 'NEQ'),
    ('left', 'LSS', 'GTR','LEQ','GEQ'),
    ('left', 'SHL', 'SHR'),
    ('left', 'ADD', 'SUB'),
    ('left', 'MUL', 'QUO','REM')
)


# Start
def p_start(p):
    '''start : SourceFile'''

# Packages
## SourceFile organization
def p_source_file(p):
    '''SourceFile : PackageClause SEMICOLON ImportDeclRep TopLevelDeclRep'''

def p_imp_decl_rep(p):
    '''ImportDeclRep : ImportDeclRep ImportDecl SEMICOLON
                     | empty'''

def p_toplevel_decl_rep(p):
    '''TopLevelDeclRep : TopLevelDeclRep TopLevelDecl SEMICOLON
                       | empty'''

## Package Clause
def p_package_clause(p):
    '''PackageClause : PACKAGE PackageName'''

def p_package_name(p):
    '''PackageName : IDENTIFIER'''

## Import Declaration
def p_imp_decl(p):
    '''ImportDecl : IMPORT ImportSpec
                  | IMPORT LPAREN ImportSpecRep RPAREN'''

def p_imp_spec_rep(p):
    '''ImportSpecRep : ImportSpec SEMICOLON ImportDeclRep
                     | empty'''


def p_imp_spec(p):
    '''ImportSpec : PkgNameDotOpt ImportPath'''

def p_pkg_name_dot(p):
    '''PkgNameDotOpt : PERIOD
                     | PackageName
                     | empty'''

def p_imp_path(p):
    '''ImportPath : STRING_LIT'''

# Blocks
def p_block(p):
    '''Block : LBRACE StatementList RBRACE'''

def p_stmt_list(p):
    '''StatementList : StatementList Statement SEMICOLON
                    | empty'''

## Declarations and Scope
def p_decl(p):
    '''Declaration : ConstDecl
                    | TypeDecl
                    | VarDecl'''

def p_toplevel_decl(p):
    '''TopLevelDecl : Declaration
                    | FunctionDecl'''

## Constant Declarations
def p_const_decl(p):
    '''ConstDecl : CONST ConstSpec
                | CONST LPAREN ConstSpecRep RPAREN'''

def p_const_spec_rep(p):
    '''ConstSpecRep : ConstSpecRep ConstSpec SEMICOLON
                    | empty'''

def p_const_spec(p):
    '''ConstSpec : IdentifierList Type ASSIGN ExpressionList'''


def p_ident_list(p):
    '''IdentifierList : IDENTIFIER IdentComRep'''

def p_ident_com_rep(p):
    '''IdentComRep : IdentComRep COMMA IDENTIFIER
                | empty'''

def p_expr_list(p):
    '''ExpressionList : Expression ComExprRep'''

def p_com_expr_rep(p):
    '''ComExprRep : COMMA Expression ComExprRep
                | empty'''

## Type Declarations
def p_type_decl(p):
    '''TypeDecl : TYPE TypeSpec
                | TYPE LPAREN TypeSpecRep RPAREN'''

def p_type_spec_rep(p):
    '''TypeSpecRep : TypeSpec SEMICOLON TypeSpecRep
                    | empty'''

def p_type_spec(p):
    '''TypeSpec : AliasDecl
                | TypeDef'''

## Alias Declarations
def p_alias_decl(p):
    '''AliasDecl : IDENTIFIER ASSIGN Type'''

## Type Definitions
def p_type_def(p):
    '''TypeDef : IDENTIFIER Type'''

## Variable Declarations
def p_var_decl(p):
    '''VarDecl : VAR VarSpec
               | VAR LPAREN VarSpecRep RPAREN'''

def p_var_spec_rep(p):
    '''VarSpecRep : VarSpec SEMICOLON VarSpecRep
                  | empty'''

def p_var_spec(p):
    '''VarSpec : IdentifierList Type ExprListOpt
                | IdentifierList ASSIGN ExpressionList'''

def p_expr_list_opt(p):
    '''ExprListOpt : ASSIGN ExpressionList
                    | empty'''

## Short Variable Declaration
def p_short_var_decl(p):
    '''ShortVarDecl : IDENTIFIER DEFINE Expression'''

## Function Declaration
def p_func_decl(p):
    '''FunctionDecl : FUNC FunctionName Signature FunctionBody
                    | FUNC FunctionName Signature'''

def p_func_name(p):
    '''FunctionName : IDENTIFIER'''

def p_func_body(p):
    '''FunctionBody : Block'''

def p_signature(p):
    '''Signature : Parameters
                 | Parameters Type'''

def p_params(p):
    '''Parameters : LPAREN  ParameterList RPAREN
                  | LPAREN RPAREN'''

def p_param_list(p):
    '''ParameterList : ParameterDecl
                     | ParamDeclComRep'''

def p_param_list_rep(p):
    '''ParamDeclComRep : ParamDeclComRep COMMA ParameterDecl
                        | ParameterDecl COMMA ParameterDecl'''

def p_param_decl(p):
    '''ParameterDecl : IdentListOpt Type'''

def p_ident_list_opt(p):
    '''IdentListOpt : IdentifierList
                        | empty'''

# Types
def p_type(p):
    '''Type : TypeName
            | TypeLit
            | LPAREN Type RPAREN'''

def p_type_name(p):
    '''TypeName : Builtin
                | QualifiedIdent'''

def p_builtin(p):
    '''Builtin : INT
               | FLOAT
               | UINT
               | COMPLEX
               | RUNE
               | BOOL
               | STRING
               | TYPE IDENTIFIER'''

def p_type_lit(p):
    '''TypeLit : ArrayType
                | StructType
                | PointerType'''

## Array Types
def p_array_type(p):
    '''ArrayType : LBRACK ArrayLength RBRACK ElementType'''

def p_array_length(p):
    '''ArrayLength : Expression'''

def p_ele_type(p):
    '''ElementType : Type'''

## Struct Types
def p_struct_type(p):
    '''StructType : STRUCT LBRACE FieldDeclRep RBRACE'''

def p_field_decl_rep(p):
    '''FieldDeclRep : FieldDeclRep FieldDecl SEMICOLON
                    | empty'''

def p_field_decl(p):
    '''FieldDecl : IdentifierList Type'''

## Pointer Type
def p_ptr_type(p):
    '''PointerType : MUL Type'''

## Function Types


# Expressions
## Operands
def p_operand(p) :
    '''Operand : Literal
                | IDENTIFIER
                | LPAREN Expression RPAREN'''

def p_literal(p):
    '''Literal :  INT_LIT
                | FLOAT_LIT
                | IMAG
                | RUNE_LIT
                | OCTAL
                | HEX
                | STRING_LIT'''


## Qualified identifiers
def p_quali_ident(p):
    '''QualifiedIdent : IDENTIFIER PERIOD TypeName'''


#Composite literals
def p_composit_lit(p):
    '''CompositeLit : LiteralType LiteralValue'''

def p_lit_type(p):
    '''LiteralType : StructType
                    | ArrayType
                    | LBRACK ELLIPSIS RBRACK ElementType
                    | TypeName'''

def p_lit_value(p):
    '''LiteralValue : LBRACE RBRACE
                    | ElementList
                    | ElementList COMMA'''
def p_ele_list(p):
    '''ElementList : KeyedElement KeyedEleRep'''

def p_keyed_ele_rep(p):
    '''KeyedEleRep : KeyedEleRep COMMA KeyedElement
                   | empty'''

def p_keyed_element(p):
    '''KeyedElement : Element
                    | Key COLON Element'''

def p_key(p):
    '''Key : FieldName
            | Expression
            | LiteralValue'''

def p_field_name(p):
    '''FieldName : IDENTIFIER'''

def p_element(p):
    '''Element : Expression
               | LiteralValue'''

## Function literals
def p_func_lit(p):
    '''FunctionLit : FUNC Signature FunctionBody'''

## Primary Expressions
def p_prim_expr(p):
    '''PrimaryExpr : Operand
                    | Conversion
                    | PrimaryExpr Selector
                    | PrimaryExpr Index
                    | PrimaryExpr TypeAssertion
                    | PrimaryExpr Arguments'''

def p_selector(p):
    '''Selector : PERIOD IDENTIFIER'''

def p_index(p):
    '''Index : LBRACK Expression RBRACK'''

def p_type_assertion(p):
    '''TypeAssertion : PERIOD LPAREN Type RPAREN'''

def p_arg(p):
    '''Arguments : LPAREN ExpressionListTypeOpt RPAREN'''

def p_expr_list_type_opt(p):
    '''ExpressionListTypeOpt : ExpressionList
                            | empty'''


## Operators
def p_expr(p):
    '''Expression : UnaryExpr
                | Expression binary_op Expression'''

def p_expr_opt(p):
    '''ExpressionOpt : Expression
                    | empty'''

def p_unary_expr(p):
    '''UnaryExpr : PrimaryExpr
                | UnaryOp UnaryExpr'''

def p_binary_op(p):
    '''binary_op : LOR
                | LAND
                | rel_op
                | add_op
                | mul_op'''

def p_rel_op(p):
    '''rel_op : EQL
            | NEQ
            | LSS
            | GTR
            | LEQ
            | GEQ'''

def p_add_op(p):
    '''add_op : ADD
            | SUB
            | OR
            | XOR'''

def p_mul_op(p):
    '''mul_op : MUL
            | QUO
            | REM
            | SHL
            | SHR
            | AND
            | AND_NOT'''

def p_unary_op(p):
    '''UnaryOp : ADD
                | SUB
                | NOT
                | XOR
                | MUL
                | AND
                | ARROW'''

## Conversion
def p_conversion(p):
    '''Conversion : Type LPAREN Expression RPAREN'''

# Statements
def p_statement(p):
    '''Statement : Declaration
                | LabeledStmt
                | SimpleStmt
                | ReturnStmt
                | BreakStmt
                | ContinueStmt
                | GotoStmt
                | Block
                | IfStmt
                | SwitchStmt
                | ForStmt'''

def p_simple_stmt(p):
    '''SimpleStmt : empty
                | ExpressionStmt
                | IncDecStmt
                | Assignment
                | ShortVarDecl'''

## Labeled statements
def p_labeled_statements(p):
    '''LabeledStmt : Label COLON Statement'''

def p_label(p):
    '''Label : IDENTIFIER'''

## Expression Statement
def p_expression_stmt(p):
    '''ExpressionStmt : Expression'''

## IncDec Statement
def p_inc_dec(p):
    '''IncDecStmt : Expression INC
                  | Expression DEC'''

## Assignments
def p_assignmnt(p):
    '''Assignment : ExpressionList AssignOp ExpressionList'''

def p_assign_op(p):
    ''' AssignOp : ADD_ASSIGN
                    | SUB_ASSIGN
                    | MUL_ASSIGN
                    | QUO_ASSIGN
                    | REM_ASSIGN
                    | AND_ASSIGN
                    | OR_ASSIGN
                    | XOR_ASSIGN
                    | SHL_ASSIGN
                    | SHR_ASSIGN
                    | ASSIGN'''

## If Statements
def p_if_stmt(p):
    '''IfStmt : IF Expression Block ElseOpt'''

def p_else_opt(p):
    '''ElseOpt : ELSE IfStmt
               | ELSE Block
               | empty'''

## For Statement
def p_for_stmt(p):
    '''ForStmt : FOR Block
               | FOR ForClause Block
               | FOR Condition Block'''

def p_condition(p):
    '''Condition : Expression '''

def p_forclause(p):
    '''ForClause : SimpleStmt SEMICOLON ConditionOpt SEMICOLON SimpleStmt'''

def p_cond_opt(p):
    '''ConditionOpt : Expression
                    | empty'''

## Return Statement
def p_return_stmt(p):
    '''ReturnStmt : RETURN
                | RETURN ExpressionList'''

## Break Statement
def p_break_stmt(p):
    '''BreakStmt : BREAK
                | BREAK Label'''

## Continue Statement
def p_continue_stmt(p):
    '''ContinueStmt : CONTINUE
                    | CONTINUE Label'''

## Goto Statement
def p_goto(p):
    '''GotoStmt : GOTO Label'''

## Switch Statements
def p_switch_stmt(p):
    '''SwitchStmt : SWITCH ExpressionOpt LBRACE ExprCaseClause RBRACE'''

def p_expr_case_clause(p):
    '''ExprCaseClause : empty
                    | ExprCaseClause ExprSwitchCase COLON StatementList'''

def p_expr_switch_case(p):
    '''ExprSwitchCase : CASE ExpressionList
                    | DEFAULT'''

def p_empty(p):
    '''empty :'''
    pass

def p_error(p):
    print("Syntax error in input!")
    print(p)

lexer = lex.lex()
parser = yacc.yacc()

with open('input.go','r') as fp:
    code = fp.read()

result = parser.parse(code)
print(result)
