import sys
import os
import pydot
import ply.yacc as yacc

import node_def as nd
from new_lexer import *

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

def p_start(p):
    '''start : SourceFile'''
    p[0] = p[1]

def p_type(p):
    '''Type : TypeName
            | TypeLit
            | LPRN Type RPRN'''
    if len(p) == 2 :
        p[0] = p[1]

def p_type_name(p):
    '''TypeName : TypeToken
                | QualifiedIdent'''
    p[0] = p[1]

def p_type_token(p):
    '''TypeToken : INT_T
                 | FLOAT_T
                 | UINT_T
                 | COMPLEX_T
                 | RUNE_T
                 | BOOL_T
                 | STRING_T
                 | TYPE IDENTIFIER'''
    if len(p) == 2 :
        p[0] = p[1]

def p_type_lit(p):
    '''TypeLit : ArrayType
               | StructType
               | PointerType'''
    if len(p) == 2 :
        p[0] = p[1]

def p_type_opt(p):
    '''TypeOpt : Type
               | epsilon'''
    if len(p) == 2 :
        p[0] = p[1]

def p_array_type(p):
  '''ArrayType : LSQR ArrayLength RSQR ElementType'''

def p_array_length(p):
  ''' ArrayLength : Expression '''

def p_element_type(p):
  ''' ElementType : Type '''

def p_struct_type(p):
  '''StructType : STRUCT LCURL FieldDeclRep RCURL '''

def p_field_decl_rep(p):
  ''' FieldDeclRep : FieldDeclRep FieldDecl SEMICOLON
                  | epsilon '''

def p_field_decl(p):
  ''' FieldDecl : IdentifierList Type'''

def p_point_type(p):
    '''PointerType : MUL BaseType'''

def p_base_type(p):
    '''BaseType : Type'''

def p_sign(p):
    '''Signature : Parameters TypeOpt'''

def p_params(p):
    '''Parameters : LPRN ParameterListOpt RPRN'''

def p_param_list_opt(p):
    '''ParameterListOpt : ParametersList
                             | epsilon'''

def p_param_list(p):
    '''ParametersList : ParameterDecl
                      | ParameterDeclCommaRep'''

def p_param_decl_comma_rep(p):
    '''ParameterDeclCommaRep : ParameterDeclCommaRep COMMA ParameterDecl
                             | ParameterDecl COMMA ParameterDecl'''

def p_param_decl(p):
    '''ParameterDecl : IdentifierList Type
                     | Type'''

def p_block(p):
    '''Block : LCURL StatementList RCURL'''

def p_stat_list(p):
    '''StatementList : StatementRep'''

def p_stat_rep(p):
    '''StatementRep : StatementRep Statement SEMICOLON
                    | epsilon'''

def p_decl(p):
  '''Declaration : ConstDecl
                 | TypeDecl
                 | VarDecl'''

def p_toplevel_decl(p):
  '''TopLevelDecl : Declaration
                  | FunctionDecl'''

def p_const_decl(p):
    '''ConstDecl : CONST ConstSpec
                 | CONST LPRN ConstSpecRep RPRN'''

def p_const_spec_rep(p):
    '''ConstSpecRep : ConstSpecRep ConstSpec SEMICOLON
                    | epsilon'''

def p_const_spec(p):
    '''ConstSpec : IdentifierList Type ASSIGN ExpressionList'''

def p_identifier_list(p):
    '''IdentifierList : IDENTIFIER IdentifierRep'''

def p_identifier_rep(p):
    '''IdentifierRep : IdentifierRep COMMA IDENTIFIER
                     | epsilon'''

def p_expr_list(p):
    '''ExpressionList : Expression ExpressionRep'''

def p_expr_rep(p):
    '''ExpressionRep : ExpressionRep COMMA Expression
                     | epsilon'''

def p_type_decl(p):
    '''TypeDecl : TYPE TypeSpec
                | TYPE LPRN TypeSpecRep RPRN'''

def p_type_spec_rep(p):
    '''TypeSpecRep : TypeSpecRep TypeSpec SEMICOLON
                   | epsilon'''

def p_type_spec(p):
    '''TypeSpec : TypeDef'''

def p_type_def(p):
    '''TypeDef : IDENTIFIER Type'''

def p_var_decl(p):
    '''VarDecl : VAR VarSpec
               | VAR LPRN VarSpecRep RPRN'''

def p_var_spec_rep(p):
    '''VarSpecRep : VarSpecRep VarSpec SEMICOLON
                  | epsilon'''

def p_var_spec(p):
    '''VarSpec : IdentifierList Type ExpressionListOpt
               | IdentifierList ASSIGN ExpressionList'''

def p_expr_list_opt(p):
    '''ExpressionListOpt : ASSIGN ExpressionList
                         | epsilon'''

def p_short_var_decl(p):
  ''' ShortVarDecl : IDENTIFIER DEFINE Expression '''

def p_func_decl(p):
    '''FunctionDecl : FUNC FunctionName  Function
                    | FUNC FunctionName  Signature '''

def p_func_name(p):
    '''FunctionName : IDENTIFIER'''

def p_func(p):
    '''Function : Signature  FunctionBody'''

def p_func_body(p):
    '''FunctionBody : Block'''

def p_operand(p):
    '''Operand : Literal
               | OperandName
               | LPRN Expression RPRN'''

def p_literal(p):
    '''Literal : BasicLit'''

def p_basic_lit(p):
    '''BasicLit : INTEGER
                | OCTAL
                | HEX
                | FLOAT
                | IMAGINARY
                | RUNE
                | STRING'''

def p_operand_name(p):
    '''OperandName : IDENTIFIER'''

def p_quali_ident(p):
    '''QualifiedIdent : IDENTIFIER DOT TypeName'''

def p_prim_expr(p):
    '''PrimaryExpr : Operand
                   | PrimaryExpr Selector
                   | Conversion
                   | PrimaryExpr LSQR Expression RSQR
                   | PrimaryExpr Slice
                   | PrimaryExpr TypeAssertion
                   | PrimaryExpr LPRN ExpressionListTypeOpt RPRN'''

def p_selector(p):
    '''Selector : DOT IDENTIFIER'''

def p_slice(p):
    '''Slice : LSQR ExpressionOpt COLON ExpressionOpt RSQR
             | LSQR ExpressionOpt COLON Expression COLON Expression RSQR'''

def p_type_assert(p):
    '''TypeAssertion : DOT LPRN Type RPRN'''

def p_expr_list_type_opt(p):
    '''ExpressionListTypeOpt : ExpressionList
                             | epsilon'''

def p_expr(p):
    '''Expression : UnaryExpr
                  | Expression LOR Expression
                  | Expression LAND Expression
                  | Expression NEQ Expression
                  | Expression EQL Expression
                  | Expression LSS Expression
                  | Expression GTR Expression
                  | Expression LEQ Expression
                  | Expression GEQ Expression
                  | Expression OR Expression
                  | Expression XOR Expression
                  | Expression QUO Expression
                  | Expression REM Expression
                  | Expression SHL Expression
                  | Expression SHR Expression
                  | Expression ADD Expression
                  | Expression SUB Expression
                  | Expression MUL Expression
                  | Expression AND Expression'''

def p_expr_opt(p):
    '''ExpressionOpt : Expression
                     | epsilon'''

def p_unary_expr(p):
    '''UnaryExpr : PrimaryExpr
                 | UnaryOp UnaryExpr
                 | NOT UnaryExpr'''

def p_unary_op(p):
    '''UnaryOp : ADD
               | SUB
               | MUL
               | AND '''

def p_conversion(p):
    '''Conversion : TYPECAST Type LPRN Expression RPRN'''

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
  ''' SimpleStmt : epsilon
                 | ExpressionStmt
                 | IncDecStmt
                 | Assignment
                 | ShortVarDecl '''

def p_labeled_statements(p):
  ''' LabeledStmt : Label COLON Statement '''

def p_label(p):
  ''' Label : IDENTIFIER '''

def p_expression_stmt(p):
  ''' ExpressionStmt : Expression '''

def p_inc_dec(p):
  ''' IncDecStmt : Expression INC
                 | Expression DEC '''

def p_goto(p):
  '''GotoStmt : GOTO Label '''

def p_assignment(p):
  ''' Assignment : ExpressionList assign_op ExpressionList'''

def p_assign_op(p):
  ''' assign_op : AssignOp'''

def p_AssignOp(p):
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
               | ASSIGN '''

def p_if_statement(p):
  ''' IfStmt : IF Expression Block  ElseOpt'''

def p_else_opt(p):
  ''' ElseOpt : ELSE IfStmt
              | ELSE  Block
              | epsilon '''

def p_switch_statement(p):
  ''' SwitchStmt : ExprSwitchStmt '''

def p_expr_switch_stmt(p):
  ''' ExprSwitchStmt : SWITCH Expression  LCURL ExprCaseClauseRep RCURL  '''

def p_expr_case_clause_rep(p):
  ''' ExprCaseClauseRep : ExprCaseClauseRep ExprCaseClause
                        | epsilon'''

def p_expr_case_clause(p):
  ''' ExprCaseClause : ExprSwitchCase COLON StatementList '''

def p_expr_switch_case(p):
  ''' ExprSwitchCase : CASE Expression
                     | DEFAULT '''

def p_for(p):
  '''ForStmt : FOR  ConditionBlockOpt Block '''

def p_conditionblockopt(p):
  '''ConditionBlockOpt : epsilon
             | Condition
             | ForClause'''

def p_condition(p):
  '''Condition : Expression '''

def p_forclause(p):
  '''ForClause : SimpleStmt SEMICOLON ConditionOpt SEMICOLON SimpleStmt'''

def p_conditionopt(p):
  '''ConditionOpt : epsilon
          | Condition '''

def p_return(p):
  '''ReturnStmt : RETURN ExpressionPureOpt'''

def p_expression_pure_opt(p):
  '''ExpressionPureOpt : Expression
             | epsilon'''

def p_break(p):
  '''BreakStmt : BREAK LabelOpt'''

def p_continue(p):
  '''ContinueStmt : CONTINUE LabelOpt'''

def p_labelopt(p):
  '''LabelOpt : Label
        | epsilon '''

def p_source_file(p):
    '''SourceFile : PackageClause SEMICOLON ImportDeclRep TopLevelDeclRep'''

def p_import_decl_rep(p):
  '''ImportDeclRep : epsilon
           | ImportDeclRep ImportDecl SEMICOLON'''

def p_toplevel_decl_rep(p):
  '''TopLevelDeclRep : TopLevelDeclRep TopLevelDecl SEMICOLON
                     | epsilon'''

def p_package_clause(p):
    '''PackageClause : PACKAGE PackageName'''

def p_package_name(p):
    '''PackageName : IDENTIFIER'''

def p_import_decl(p):
  '''ImportDecl : IMPORT ImportSpec
          | IMPORT LPRN ImportSpecRep RPRN '''

def p_import_spec_rep(p):
  ''' ImportSpecRep : ImportSpecRep ImportSpec SEMICOLON
            | epsilon '''

def p_import_spec(p):
  ''' ImportSpec : PackageNameDotOpt ImportPath '''


def p_package_name_dot_opt(p):
  ''' PackageNameDotOpt : DOT
                        | PackageName
                        | epsilon'''

def p_import_path(p):
  ''' ImportPath : STRING '''


def p_empty(p):
  '''epsilon : '''

def p_error(p):
  print(p)
  raise SyntaxError("Syntax error in the code!")


# Build the parser
parser = yacc.yacc()

with open("factorial.go") as f:
    data = f.read()
result = parser.parse(data)
print(result)
