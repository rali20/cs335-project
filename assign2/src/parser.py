# TODO : Write AST for the given grammar

import sys
import ply.yacc as yacc
from lexer import *

# Source
def p_start(p):
    '''start : SourceFile'''

# Types
def p_type(p):
    '''Type : TypeName
            | TypeLit
            | LPAREN Type RPAREN'''

def p_type_name(p):
    '''TypeName : IDENTIFIER
                | QualifiedIdent'''

def p_type_lit(p):
    '''TypeLit : ArrayType
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
    '''IdentifierList : IDENTIFIER IdentComRep'''

def p_ident_com_rep(p):
    '''IdentComRep : IdentComRep COMMA IDENTIFIER
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
    '''AliasDecl : IDENTIFIER ASSIGN Type'''

# Type Definitions
def p_type_def(p):
    '''TypeDef : IDENTIFIER Type'''

# Variable Declarations
def p_var_decl(p):
    '''VarDecl : VAR VarSpec
               | VAR LPAREN VarSpecRep RPAREN'''

def p_var_spec_rep(p):
    '''VarSpecRep : VarSpec SEMICOLON VarSpecRep
                  | empty'''

def p_var_spec(p):
    '''VarSpec : IdentifierList Type ExpressionListOpt
               | IdentifierList ASSIGN ExpressionList'''

def p_expr_list_opt(p):
    '''ExpressionListOpt : ASSIGN ExpressionList
                         | empty'''

# Short Variable Declaration
def p_short_var_decl(p):
    '''ShortVarDecl : IdentifierList DEFINE ExpressionList'''

# Function Declaration
def p_func_decl(p):
    '''FunctionDecl : FUNC FunctionName Signature FunctionBody
                    | FUNC FunctionName Signature'''

def p_func_name(p):
    '''FunctionName : IDENTIFIER'''

def p_func_body(p):
    '''FunctionBody : Block'''

# Operands
def p_operand(p) :
    '''Operand : Literal
               | OperandName
               | LPAREN Expression RPAREN'''

def p_literal(p):
    '''Literal : BasicLit'''
              # | CompositeLit
              # | FunctionLit'''

def p_basic_lit(p):
    '''BasicLit : INT
                | FLOAT
                | IMAG
                | RUNE
                | OCTAL
                | HEX
                | STRING'''

def p_operand_name(p):
    '''OperandName : IDENTIFIER
                   | QualifiedIdent'''

# Qualified identifiers
def p_quali_ident(p):
    '''QualifiedIdent : PackageName PERIOD IDENTIFIER'''

#Composite literals
# def p_composit

# Function literals


#Primary Expresiions
def p_prim_expr(p):
    '''PrimaryExpr : Operand
                   | Conversion
                   | PrimaryExpr Selector
                   | PrimaryExpr Index
                   | PrimaryExpr Slice
                   | PrimaryExpr TypeAssertion
                   | PrimaryExpr Arguments'''

def p_selector(p):
    '''Selector : PERIOD IDENTIFIER'''

def p_index(p):
    '''Index : LBRACK Expression RBRACK'''

def p_slice(p):
    '''Slice : LBRACK ExpressionOpt COLON ExpressionOpt RBRACK
             | LBRACK ExpressionOpt COLON Expression COLON Expression RBRACK'''

def p_type_assertion(p):
    '''TypeAssertion : PERIOD LPAREN Type RPAREN'''

def p_expr_list_type_opt(p):
    '''ExpressionListTypeOpt : ExpressionList
                             | empty'''
    p[0] = p[1]

def p_arg(p):
    '''Arguments : LPAREN ExpressionListTypeOpt RPAREN'''

# Operators
def p_expr(p):
    '''Expression : UnaryExpr
                  | Expression binary_op Expression'''

def p_expr_opt(p):
    '''ExpressionOpt : Expression
                     | empty'''
    p[0] = p[1]

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

#Conversion
def p_conversion(p):
    '''Conversion : Type LPAREN Expression RPAREN'''

#Statements
def p_statement(p):
    '''Statement : Declaration
                 | LabeledStmt
                 | SimpleStmt
                 | ReturnStmt
                 | BreakStmt
                 | ContinueStmt
                 | GotoStmt
                 | FallthroughStmt
                 | Block
                 | IfStmt
                 | SwitchStmt
                 | SelectStmt
                 | ForStmt
                 | DeferStmt'''

def p_simple_stmt(p):
    '''SimpleStmt : EmptyStmt
                  | ExpressionStmt
                  | IncDecStmt
                  | Assignment
                  | ShortVarDecl'''

#Empty Statements
def p_empty_stmt(p):
    '''EmptyStmt : empty'''

#labeled statements
def p_labeled_statements(p):
    '''LabeledStmt : Label COLON Statement'''

def p_label(p):
    '''Label : IDENTIFIER'''

#Expression Statement
def p_expression_stmt(p):
    '''ExpressionStmt : Expression'''

#Send Statement NOt written because of Channel

#IncDec Statement
def p_inc_dec(p):
    '''IncDecStmt : Expression INC
                  | Expression DEC'''

#Assignments
def p_assignmnt(p):
    '''Assignment : ExpressionList assign_op ExpressionList'''

def p_assign_op(p):
  ''' assign_op : AssignOp'''
  p[0] = ["assign_op", p[1]]

def p_AssignOp(p):
  ''' AssignOp : ADD_ASSIGN
               | SUB_ASSIGN
               | MUL_ASSIGN
               | QUO_ASSIGN
               | REM_ASSIGN
               | AND_ASSIGN
               | OR_ASSIGN
               | XOR_ASSIGN
               | LSHIFT_ASSIGN
               | RSHIFT_ASSIGN
               | ASSIGN'''
  p[0] = ["AssignOp", p[1]]



###################################################

#For Statement
def p_for_stmt(p):
    '''ForStmt : FOR ''' #####Not Completed

def p_condition(p):
    '''Condition : Expression '''

def p_forclause(p):
    '''ForClause : InitStmt SEMICOLON ConditionOpt SEMICOLON PostStmt'''

def p_init_stmt(p):
    '''InitStmt : SimpleStmt'''

def p_post_stmt(p):
    '''PostStmt : SimpleStmt'''


#Return Statement
def p_return_stmt(p):
    '''ReturnStmt : RETURN ExpressionListOpt'''

#Break Statement
def p_break_stmt(p):
    '''BreakStmt : BREAK LabelOpt'''

#Continue Statement
def p_continue_stmt(p):
    '''ContinueStmt : CONTINUE LabelOpt'''

#GOto Statement
def p_goto(p):
    '''GotoStmt : GOTO Label'''

#Fallthrough Statement
def p_fallthrough_stmt(p):
    '''FallthroughStmt : FALLTHROUGH'''

def p_defer_stmt(p):
    '''DeferStmt : defer Expression'''

#SourceFile organization
def p_source_file(p):
    '''SourceFile : PackageClause SEMICOLON ImportDeclRep TopLevelDeclRep'''

def p_package_clause(p):
    '''PackageClause : PACKAGE PackageName'''

def p_package_name(p):
    '''PackageName : IDENTIFIER'''

def p_imp_decl(p):
    '''ImportDecl : IMPORT ImportSpec
                  | IMPORT LPAREN ImportSpecRep RPAREN'''

def p_imp_spec(p):
    '''ImportSpec : PackageNamePERIODOpt ImportPath'''

def p_imp_path(p):
    '''ImportPath : STRING'''

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    print("Syntax error in input!")



parser = yacc.yacc()
while True:
    try:
        s = raw_input('calc > ')
    except EOFError:
        break
    if not s: continue
    result = parser.parse(s)
    print(result)
