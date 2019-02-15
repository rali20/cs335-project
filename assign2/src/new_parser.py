import sys
import os
import pydot
import ply.yacc as yacc

import node_def as nd
from new_lexer import *
import ast_decl

precedence = (
    ('right','AGN', 'NOT'),
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
    else :
        p[0] = p[2]

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
                 | TYPE IDENT'''
    if len(p) > 2 :
        leaf_node = nd.node(p[2])
        p[0] = nd.one_child_node(leaf_node,"Type")
    else :
        leaf_node = nd.node(p[1])
        p[0] = nd.one_child_node(leaf_node,"BuiltinType")


def p_type_lit(p):
    '''TypeLit : ArrayType
               | StructType
               | PtrType'''
    if len(p) == 2 :
        p[0] = p[1]

def p_array_type(p):
  '''ArrayType : LSQR ArrayLength RSQR ElementType'''
  p[0] = nd.two_child_node(p[2],p[4],"ArrayType")

def p_array_length(p):
  ''' ArrayLength : Expr '''
  p[0] = p[1]

def p_element_type(p):
  ''' ElementType : Type '''
  p[0] = p[1]

def p_struct_type(p):
  '''StructType : STRUCT LCURL FieldDeclRep RCURL '''
  p[0] = nd.one_child_node(p[3],"StructType")

def p_field_decl_rep(p):
  ''' FieldDeclRep : FieldDecl SEMCLN FieldDeclRep
                  | epsilon '''
  if len(p) > 2 :
       p[0] = nd.two_child_node(p[1],p[3],"FieldDecls")

def p_field_decl(p):
  ''' FieldDecl : IdentList Type'''
  p[0] = nd.two_child_node(p[1],p[2],"FieldDecl")

def p_point_type(p):
    '''PtrType : MUL BaseType'''
    p[0] = nd.one_child_node(p[2],"PointerTo")

def p_base_type(p):
    '''BaseType : Type'''
    p[0] = p[1]

def p_sign(p):
    '''Signature : Parameters
                 | Parameters Type'''
    if len(p) > 2 :
        p[0] = nd.two_child_node(p[1],p[2],"Signature")
    else :
        p[0] = nd.one_child_node(p[1],"Signature")

def p_params(p):
    '''Parameters : LPRN RPRN
                  | LPRN ParamList RPRN'''
    if len(p) > 3 :
        p[0] = nd.one_child_node(p[2], "Parameters")
    else :
        p[0] = nd.node("NULL")

def p_param_list(p):
    '''ParamList : ParamDecl
                      | ParamDeclCommaRep'''
    p[0] = p[1]

def p_param_decl_comma_rep(p):
    '''ParamDeclCommaRep : COMMA ParamDecl ParamDeclCommaRep
                             | ParamDecl COMMA ParamDecl'''
    if p[1]==',':
        p[0] = nd.two_child_node(p[2],p[3],"ParameterList")
    else :
        p[0] = nd.two_child_node(p[1],p[3],"ParameterList")

def p_param_decl(p):
    '''ParamDecl : IdentList Type
                     | Type'''
    if len(p) == 2 :
        p[0] = p[1]
    else :
        p[0] = nd.two_child_node(p[1],p[2],"ParameterDecl")

def p_block(p):
    '''Block : LCURL StmtList RCURL'''
    p[0] = p[2]

def p_stat_rep(p):
    '''StmtList : Statement SEMCLN StmtList
                     | epsilon'''
    if len(p) > 2 :
        p[0] = nd.two_child_node(p[1],p[3],"Statements")
    else :
        p[0] = p[1]

def p_decl(p):
  '''Declaration : ConstDecl
                 | TypeDecl
                 | VarDecl'''
  p[0] = p[1]

def p_top_level_decl(p):
  '''TopLvlDecl : Declaration
                  | FuncDecl
                  | MethodDecl'''
  p[0] = p[1]

def p_const_decl(p):
    '''ConstDecl : CONST ConstSpec
                 | CONST LPRN ConstSpecRep RPRN'''
    if len(p) > 3:
        p[0] = p[3]
    else :
        p[0] = p[1]

def p_const_spec_rep(p):
    '''ConstSpecRep : ConstSpec SEMCLN ConstSpecRep
                    | epsilon'''
    if len(p) > 2 :
        p[0] = nd.two_child_node(p[1],p[3],"ConstSpecs")
    else :
        p[0] = p[1]

def p_const_spec(p):
    '''ConstSpec : IdentList Type AGN ExprList'''
    p[0] = nd.three_child_node(p[1],p[2],p[4],"ConstSpec")

def p_ident_list(p):
    '''IdentList : IDENT IdentRep'''
    leaf_node = nd.node(p[1])
    p[0] = nd.two_child_node(leaf_node, p[2], "IdentifierList")

def p_ident_rep(p):
    '''IdentRep : COMMA IDENT IdentRep
                     | epsilon'''
    if len(p) > 2 :
        p[0] = nd.two_child_node(p[2], p[3], "IdentifierList")
    else :
        p[0] = p[1]

def p_expr_list(p):
    '''ExprList : Expr
                      | Expr COMMA ExprList'''
    if len(p) > 2 :
        p[0] = nd.two_child_node(p[1], p[2], "ExprList")
    else :
        p[0] = p[1]

def p_type_decl(p):
    '''TypeDecl : TYPE TypeSpec
                | TYPE LPRN TypeSpecRep RPRN'''
    if len(p) < 4 :
        p[0] = p[2]
    else :
        p[0] = p[3]

def p_type_spec_rep(p):
    '''TypeSpecRep : TypeSpec SEMCLN TypeSpecRep
                   | epsilon'''
    if len(p) > 2:
        p[0] = nd.two_child_node(p[1],p[3],"TypeSpecs")

def p_type_spec(p):
    '''TypeSpec : TypeDef'''
    p[0] = p[1]

def p_type_def(p):
    '''TypeDef : IDENT Type'''
    leaf_node = nd.node(p[1])
    p[0] = nd.two_child_node(leaf_node, p[2], "Typedef")

def p_var_decl(p):
    '''VarDecl : VAR VarSpec
               | VAR LPRN VarSpecRep RPRN'''
    if len(p) < 4 :
        p[0] = p[2]
    else :
        p[0] = p[3]

def p_var_spec_rep(p):
    '''VarSpecRep : VarSpec SEMCLN VarSpecRep
                  | epsilon'''
    if len(p) > 2 :
        p[0] = nd.two_child_node(p[1],p[3],"VarSpecs")

def p_var_spec(p):
    '''VarSpec : IdentList Type AGN ExprList
               | IdentList AGN ExprList
               | IdentList Type'''
    if len(p) == 5:
        p[0] = nd.three_child_node(p[1],p[2],p[3],"VarSpecs")
    elif len(p) == 4 :
        p[0] = nd.two_child_node(p[1],p[3],"VarSpecInfer")
    else :
        p[0] = nd.two_child_node(p[1],p[2],"VarSpec")

def p_short_var_decl(p):
  ''' ShortVarDecl : IDENT DEFN Expr '''
  p[0] = p[0] = nd.two_child_node(p[1],p[3],"ShortVarDecl")

def p_func_decl(p):
    '''FuncDecl : FUNC FuncName  Signature  FuncBody
                    | FUNC FuncName  Signature '''
    if len(p) == 5 :
        p[0] = nd.three_child_node(p[2],p[3],p[4],"Function")
    else :
        p[0] = nd.two_child_node(p[2], p[3], "FuncDecl")

def p_func_name(p):
    '''FuncName : IDENT'''
    p[0] = nd.node(p[1])

def p_func_body(p):
    '''FuncBody : Block'''
    p[0] = p[1]

def p_method_decl(p):
    '''MethodDecl : FUNC Receiver MethodName Signature
                  | FUNC Receiver MethodName Signature FuncBody'''
    if len(p)==5:
        p[0] = nd.three_child_node(p[2], p[3], p[4], "MethodDecl")
    else:
        p[0] = nd.four_child_node(p[2], p[3], p[4], p[5], "MethodDecl")

def p_receiver(p):
    '''Receiver : Parameters'''
    p[0] = p[1]

def p_method_name(p):
    '''MethodName : IDENT'''
    p[0] = p[1]

def p_operand(p):
    '''Operand : Literal
               | OperandName
               | LPRN Expr RPRN'''
    if len(p) > 2 :
        p[0] = p[2]
    else :
        p[0] = p[1]

def p_literal(p):
    '''Literal : BasicLit'''
    p[0] = p[1]

def p_basic_lit(p):
    '''BasicLit : INTEGER
                | OCTAL
                | HEX
                | FLOAT
                | IMAGINARY
                | RUNE
                | STRING'''
    p[0] = p[1]

def p_operand_name(p):
    '''OperandName : IDENT'''
    p[0] = p[1]

def p_quali_ident(p):
    '''QualifiedIdent : IDENT DOT TypeName'''
    p[0] = nd.two_child_node(p[1],  p[3], "QualifiedIdent")

def p_prim_expr(p):
    '''PmryExpr : Operand
                   | Conversion
                   | PmryExpr Slice
                   | PmryExpr Selector
                   | PmryExpr TypeAssertion
                   | PmryExpr LSQR Expr RSQR
                   | PmryExpr LPRN ExprListTypeOpt RPRN'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p)==3:
        p[0] = nd.two_child_node(p[1], p[2], "PrimaryExpr")
    elif len(p)==5:
        p[0] = nd.two_child_node(p[1], p[3], "PrimaryExpr")

def p_selector(p):
    '''Selector : DOT IDENT'''
    leaf_node = nd.node(p[2])
    p[0] = nd.one_child_node(leaf_node,"Selector")

def p_slice(p):
    '''Slice : LSQR ExprOpt COLON ExprOpt RSQR
             | LSQR ExprOpt COLON Expr COLON Expr RSQR'''
    if len(p)==6:
        p[0] = nd.two_child_node(p[2], p[4], "Slice")
    else:
        p[0] = nd.three_child_node(p[2], p[4], p[6], "Slice")

def p_type_assert(p):
    '''TypeAssertion : DOT LPRN Type RPRN'''
    p[0] = p[3]

def p_expr_list_type_opt(p):
    '''ExprListTypeOpt : ExprList
                             | epsilon'''
    p[0] = p[1]

# def p_method_expr(p):
#     '''MethodExpr : ReceiverType DOT MethodName'''
#     p[0] = nd.two_child_node(p[1],p[3],"MethodExpr")

# def p_receiver_type(p):
#     '''ReceiverType : Type'''
#     p[0] = p[1]

def p_expr(p):
    '''Expr : UnaryExpr
                  | Expr LOR Expr
                  | Expr LAND Expr
                  | Expr NEQ Expr
                  | Expr EQL Expr
                  | Expr LSS Expr
                  | Expr GTR Expr
                  | Expr LEQ Expr
                  | Expr GEQ Expr
                  | Expr OR Expr
                  | Expr XOR Expr
                  | Expr QUO Expr
                  | Expr REM Expr
                  | Expr SHL Expr
                  | Expr SHR Expr
                  | Expr ADD Expr
                  | Expr SUB Expr
                  | Expr MUL Expr
                  | Expr AND Expr'''
    if len(p) != 2:
        p[0] = nd.two_child_node(p[1], p[3], p[2])
    else:
        p[0] = p[1]

def p_expr_opt(p):
    '''ExprOpt : Expr
                     | epsilon'''
    p[0] = p[1]

def p_unary_expr(p):
    '''UnaryExpr : PmryExpr
                 | UnaryOp UnaryExpr
                 | NOT UnaryExpr'''
    if len(p)==2:
        p[0] = p[1]
    else:
        p[0] = nd.two_child_node(p[1], p[2], "UnaryExpr")

def p_unary_op(p):
    '''UnaryOp : ADD
               | SUB
               | MUL
               | AND '''
    p[0] = p[1]

def p_conversion(p):
    '''Conversion : TYPECAST Type LPRN Expr RPRN'''
    p[0] = nd.two_child_node(p[2], p[4], "Conversion")

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
    p[0] = p[1]

def p_simple_stmt(p):
  ''' SimpleStmt : epsilon
                 | ExprStmt
                 | IncDecStmt
                 | Assignment
                 | ShortVarDecl '''
  p[0] = p[1]


def p_labeled_statements(p):
  ''' LabeledStmt : Label COLON Statement '''
  p[0] = nd.two_child_node(p[1], p[3], "LabeledStmt")

def p_label(p):
  ''' Label : IDENT '''
  p[0] = p[1]

def p_expression_stmt(p):
  ''' ExprStmt : Expr '''
  p[0] = p[1]

def p_inc_dec(p):
  ''' IncDecStmt : Expr INC
                 | Expr DEC '''
  p[0] = nd.two_child_node(p[1], p[2], "IncDecStmt")

def p_goto(p):
  '''GotoStmt : GOTO Label '''
  p[0] = nd.one_child_node(p[2], "GoToStmt")

def p_assignment(p):
  ''' Assignment : ExprList AssignOp ExprList'''
  p[0] = three_child_node(p[1],p[3],p[2])

def p_assign_op(p):
  ''' AssignOp : ADD_AGN
               | SUB_AGN
               | MUL_AGN
               | QUO_AGN
               | REM_AGN
               | AND_AGN
               | OR_AGN
               | XOR_AGN
               | SHL_AGN
               | SHR_AGN
               | AGN '''
  p[0] = p[1]

def p_if_statement(p):
  ''' IfStmt : IF Expr Block  ElseOpt'''
  p[0] = nd.three_child_node(p[2], p[3], p[4], "IfStmt")

def p_else_opt(p):
  ''' ElseOpt : ELSE IfStmt
              | ELSE  Block
              | epsilon '''
  if len(p)==2:
      p[0] = p[1]
  else:
      p[0] = p[2]

def p_switch_statement(p):
  ''' SwitchStmt : ExprSwitchStmt '''
  p[0] = p[1]

def p_expr_switch_stmt(p):
  ''' ExprSwitchStmt : SWITCH Expr  LCURL ExprCaseClauseRep RCURL  '''
  p[0] = nd.two_child_node(p[2], p[4], "ExprSwitchStmt")

def p_expr_case_clause_rep(p):
  ''' ExprCaseClauseRep : ExprCaseClauseRep ExprCaseClause
                        | epsilon'''
  if len(p) == 1:
      p[0] = p[1]
  else:
      p[0] = nd.two_child_node(p[1], p[2], "CaseClause")

def p_expr_case_clause(p):
  ''' ExprCaseClause : ExprSwitchCase COLON StmtList '''
  p[0] = nd.two_child_node(p[1], p[3], "ExprCaseClause")

def p_expr_switch_case(p):
  ''' ExprSwitchCase : CASE Expr
                     | DEFAULT '''
  if len(p) == 3:
      p[0] = nd.one_child_node(p[2],"Case")
  else :
      p[0] = nd.node("Default")

def p_for(p):
  '''ForStmt : FOR  CondBlk Block
             | FOR Block'''
  if len(p) > 3 :
      p[0] = nd.two_child_node(p[2],p[3],"ForStmt")
  else :
      p[0] = nd.one_child_node(p[2],"InfLoop")


def p_cond_blk_opt(p):
  '''CondBlk : Condition
             | ForClause'''
  p[0] = p[1]

def p_condition(p):
  '''Condition : Expr '''
  p[0] = p[1]

def p_forclause(p):
  '''ForClause : SimpleStmt SEMCLN SEMCLN SimpleStmt
               | SimpleStmt SEMCLN Condition SEMCLN SimpleStmt'''
  if len(p) > 5:
      p[0] = nd.three_child_node(p[1],p[3],p[5],"ForClause")
  else :
      p[0] = nd.two_child_node(p[1],p[4],"InfLoopFor")

def p_return(p):
  '''ReturnStmt : RETURN
                | RETURN Expr'''
  if len(p)>2 :
      p[0] = nd.one_child_node(p[2],p[1])
  else :
      p[0] = nd.node(p[1])

def p_break(p):
  '''BreakStmt : BREAK
               | BREAK Label'''
  if len(p)>2 :
      p[0] = nd.one_child_node(p[2],p[1])
  else :
      p[0] = nd.node(p[1])

def p_continue(p):
  '''ContinueStmt : CONTINUE
                  | CONTINUE Label'''
  if len(p)>2 :
      p[0] = nd.one_child_node(p[2],p[1])
  else :
      p[0] = nd.node(p[1])

def p_source_file(p):
    '''SourceFile : PkgClause SEMCLN ImportDeclRep TopLvlDeclRep'''
    p[3] = nd.multiple_node_parent(ast_decl.ast_imports, "Imports")
    p[0] = nd.three_child_node(p[1],p[3],p[4],"SourceFile")

def p_import_decl_rep(p):
  '''ImportDeclRep : epsilon
           |  ImportDecl SEMCLN ImportDeclRep'''
  # if len(p) > 2 :
  #     # p[0] = nd.two_child_node(p[1],p[3],"ImportDecls")
  # p[0] = nd.multiple_node_parent(ast_decl.ast_imports, "Imports")
  #
  # else :
  #     p[0] = p[1]

def p_top_level_decl_rep(p):
  '''TopLvlDeclRep : TopLvlDeclRep TopLvlDecl SEMCLN
                     | epsilon'''
  if len(p) > 2 :
      p[0] = nd.two_child_node(p[1],p[2],"TopLvlDecls")
  else :
      p[0] = p[1]

def p_pkg_clause(p):
    '''PkgClause : PACKAGE PkgName'''
    p[0] = p[2]

def p_pkg_name(p):
    '''PkgName : IDENT'''
    leaf_node = nd.node(p[1])
    p[0] = nd.one_child_node(leaf_node,"PackageName")

def p_import_decl(p):
  '''ImportDecl : IMPORT ImportSpec
                | IMPORT LPRN ImportSpecRep RPRN '''
  # if len(p)==3:
  #     p[0] = nd.two_child_node(nd.node(p[1]), p[2], "ImportDecl")
  # else:
  #     p[0] = nd.two_child_node(nd.node(p[1]), p[3], "ImportDecl")

def p_import_spec_rep(p):
  ''' ImportSpecRep : ImportSpecRep ImportSpec SEMCLN
                    | epsilon '''
  # if len(p) == 4:
  #     p[0] = nd.two_child_node(p[1], p[2], "ImportSpecRep")
  # else:
  #     p[0] = p[1]

def p_import_spec(p):
  ''' ImportSpec : PkgNameDotOpt ImportPath '''
  # p[0] = nd.two_child_node(p[1], p[2], "ImportSpec")


def p_pkg_name_dot_opt(p):
  ''' PkgNameDotOpt : DOT
                        | PkgName
                        | epsilon'''
  if(p[1]=="."):
      p[0] = nd.node(".")
  else:
      p[0] = p[1]

def p_import_path(p):
  ''' ImportPath : STRING '''
  ast_decl.ast_imports.append(p[1])
  # leaf_node = nd.node(p[1])
  # p[0] = nd.one_child_node(leaf_node,"ImportPath")

def p_epsilon(p):
  '''epsilon : '''
  # p[0] = nd.node("NULL")
  p[0] = None

def p_error(p):
  print(p)
  raise SyntaxError("Syntax error in the code!")


# Build the parser
parser = yacc.yacc()

with open("factorial.go", "r") as f:
    data = f.read()
result = parser.parse(data)
# print(result)
print(ast_decl.ast_imports)
nd.graph_plot()
