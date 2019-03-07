import sys
import os
import ply.yacc as yacc

from new_lexer import *

precedence = (
    ('right', 'AGN', 'NOT'),
    ('left', 'LOR'),
    ('left', 'LAND'),
    ('left', 'OR'),
    ('left', 'XOR'),
    ('left', 'AND'),
    ('left', 'EQL', 'NEQ'),
    ('left', 'LSS', 'GTR', 'LEQ', 'GEQ'),
    ('left', 'SHL', 'SHR'),
    ('left', 'ADD', 'SUB'),
    ('left', 'MUL', 'QUO', 'REM')
)

def p_source_file(p):
    '''SourceFile    : PackageClause Imports DeclList'''

def p_package_clause(p):
    '''PackageClause : PACKAGE IDENT SEMCLN'''

def p_imports(p):
    '''Imports    : empty
                | Imports Import SEMCLN'''

def p_import(p):
    '''Import     : IMPORT ImportStmt
               | IMPORT LPRN ImportStmtList OSemi RPRN
               | IMPORT LPRN RPRN'''

def p_import_stmt(p):
    '''ImportStmt : ImportHere string_literal'''

def p_import_stmt_list(p):
    '''ImportStmtList : ImportStmt
               | ImportStmtList SEMCLN ImportStmt'''

def p_import_here(p):
    '''ImportHere : empty
           | IDENT
           | DOT'''

def p_decl(p):
    '''Declaration : CommonDecl
                | FuncDecl
                | NonDeclStmt'''

def p_common_decl(p):
    '''CommonDecl : CONST ConstDecl
                | CONST LPRN ConstDecl OSemi RPRN
                | CONST LPRN ConstDecl SEMCLN ConstDeclList OSemi RPRN
                | CONST LPRN RPRN
                | VAR VarDecl
                | VAR LPRN VarDeclList OSemi RPRN
                | VAR LPRN RPRN
                | TYPE TypeDecl
                | TYPE LPRN TypeDeclList OSemi RPRN
                | TYPE LPRN RPRN'''

def p_var_decl(p):
    '''VarDecl   : DeclNameList NType
                | DeclNameList NType AGN ExprList
                | DeclNameList AGN ExprList'''

def p_const_decl(p):
    '''ConstDecl : DeclNameList NType AGN ExprList
                | DeclNameList AGN ExprList'''

def p_const_decl_1(p):
    '''ConstDecl1 : ConstDecl
                | DeclNameList NType
                | DeclNameList'''

def p_type_decl_name(p):
    '''TypeDeclName : IDENT'''

def p_type_decl(p):
    '''TypeDecl : TypeDeclName NType'''

dec p_inc_dec_op(p):
    '''Inc_dec_op : INC
                | DEC'''

def p_simple_stmt(p):
    '''SimpleStmt : Expr
                | Expr mod_assign_op Expr
                | ExprList AGN ExprList
                | ExprList DEFN ExprList
                | Expr Inc_dec_op'''

def p_case(p):
    '''Case : CASE ExprOrTypeList COLON
            | CASE ExprOrTypeList AGN Expr COLON
            | CASE ExprOrTypeList DEFN Expr COLON
            | DEFAULT COLON'''

def p_compound_stmt(p):
    '''CompoundStmt : LCURL StmtList RCURL'''

def p_case_block(p):
    '''CaseBlock : Case StmtList'''

def p_case_block_list(p):
    '''CaseBlockList : empty
                    | CaseBlockList CaseBlock'''

def p_loop_body(p):
    '''LoopBody : LCURL StmtList RCURL'''

def p_range_stmt(p):
    '''RangeStmt : ExprList AGN RANGE Expr
          | ExprList DEFN RANGE Expr
          | RANGE Expr'''

def p_for_header(p):
    '''ForHeader : OSimpleStmt SEMCLN OSimpleStmt SEMCLN OSimpleStmt
          | OSimpleStmt
          | RangeStmt'''

def p_for_body(p):
    '''ForBody : ForHeader LoopBody'''

def p_for_stmt(p):
    '''ForStmt : FOR ForBody'''

def p_if_header(p):
    '''IfHeader : OSimpleStmt
         | OSimpleStmt SEMCLN OSimpleStmt'''

def p_if_stmt(p):
    '''IfStmt : IF IfHeader LoopBody ElseIfList Else'''

def p_else_if(p):
    '''ElseIf : ELSE IF IfHeader LoopBody'''

def p_else_if_list(p):
    '''ElseIfList : empty
           | ElseIfList ElseIf'''

def p_else(p):
    '''Else : empty
     | ELSE CompoundStmt'''

def p_ntype(p):
    '''NType : FuncType
      |	OtherType
      |	PtrType
      |	DotName
      |	LPRN NType RPRN'''

def p_non_expr_type(p):
'''NonExprType : FuncType
            | OtherType
            | MUL NonExprType'''

def p_other_type(p):
    '''OtherType : LSQR OExpr LSQR NType
          | MAP LSQR NType LSQR NType
          | StructType
          | InterfaceType'''

def p_struct_type(p):
    '''StructType : STRUCT LCURL StructDeclList OSemi RCURL
           | STRUCT LCURL RCURL'''

def p_interface_type(p):
    '''InterfaceType : INTERFACE LCURL InterfaceDeclList OSemi RCURL
              | INTERFACE LCURL RCURL'''

def p_func_decl(p):
    '''FuncDecl : FUNC FuncDecl_ FuncBody'''

def p_func_Decl_(p):
    '''FuncDecl_ : IDENT ArgList FuncRes
                | left_tuple OArgTypeListOComma right_tuple IDENT ArgList FuncRes'''

def p_func_type(p):
    '''FuncType : FUNC ArgList FuncRes'''

def p_arg_list(p):
    '''ArgList : LPRN OArgTypeListOComma RPRN
                | ArgList LPRN OArgTypeListOComma RPRN'''

def p_func_body(p):
    '''FuncBody : empty
                | LCURL StmtList RCURL'''

def p_func_res(p):
    '''FuncRes : empty
                | FuncRetType
                | left_tuple OArgTypeListOComma right_tuple'''

def p_struct_decl_list(p):
    '''StructDeclList : StructDecl
                    | StructDeclList SEMCLN StructDecl'''

def p_interface_decl_list(p):
    '''InterfaceDeclList : InterfaceDecl
                        | InterfaceDeclList SEMCLN InterfaceDecl'''

def p_struct_decl(p):
    '''StructDecl : NewNameList NType OLiteral
                    | Embed OLiteral
                    | LPRN Embed RPRN OLiteral
                    | MUL Embed OLiteral
                    | LPRN MUL Embed RPRN OLiteral
                    | MUL LPRN Embed RPRN OLiteral'''

def p_interface_decl(p):
    '''InterfaceDecl : NewName InDecl
                    | IDENT
                    | LPRN IDENT RPRN'''

def p_indecl(p):
    '''InDecl : LPRN OArgTypeListOComma RPRN FuncRes'''

def p_label_name(p):
    '''LabelName : NewName'''

def p_new_name(p):
    '''NewName : IDENT'''

def p_ptr_type(p):
    '''PtrType : MUL NType'''

def p_func_ret_type(p):
    '''FuncRetType : FuncType
                    | OtherType
                    | PtrType
                    | DotName'''

def p_dot_name(p):
    '''DotName : Name
                | Name DOT IDENT'''

def p_ocomma(p):
    '''OComma : empty
                | COMMA'''

def p_osemi(p):
    '''OSemi : empty
            | SEMCLN'''

def p_osimple_stmt(p):
    '''OSimpleStmt : empty
                | SimpleStmt'''

def p_onew_name(p):
    '''ONewName : empty
                | NewName'''

def p_oexpr(p):
    '''OExpr : empty
            | Expr'''

def p_oexpr_list(p):
    '''OExprList : empty
                | ExprList'''

def p_func_literal_decl(p):
    '''FuncLiteralDecl : FuncType'''

def p_func_literal(p):
    '''FuncLiteral : FuncLiteralDecl LCURL StmtList RCURL'''

def p_expr_list(p):
    '''ExprList : Expr
         | ExprList COMMA Expr'''

def p_expr_or_type_list(p):
    '''ExprOrTypeList : ExprOrType
               | ExprOrTypeList COMMA ExprOrType'''

def p_oliteral(p):
    '''OLiteral : empty
         | Literal'''

def p_literal(p):
    '''Literal : int_lit
        | float_lit
        | rune_lit
        | string_literal'''

def p_embed(p):
    '''Embed : IDENT'''

def p_decl_list(p):
    '''DeclList : empty
         | DeclList Declaration SEMCLN'''

def p_var_decl_list(p):
    '''VarDeclList : VarDecl
            | VarDeclList SEMCLN VarDecl'''

def p_const_decl_list(p):
    '''ConstDeclList : ConstDecl1
              | ConstDeclList SEMCLN ConstDecl1'''

def p_type_decl_list(p):
    '''TypeDeclList : TypeDecl
             | TypeDeclList SEMCLN TypeDecl'''

def p_decl_name_list(p):
    '''DeclNameList : DeclName
             | DeclNameList COMMA DeclName'''

def p_stmt_list(p):
    '''StmtList : Stmt
         | StmtList SEMCLN Stmt'''

def p_new_name_list(p):
    '''NewNameList : NewName
            | NewNameList COMMA NewName'''

def p_keyval_list(p):
    '''KeyvalList : Keyval
           | BareCompLitExpr
           | KeyvalList COMMA Keyval
           | KeyvalList COMMA BareCompLitExpr'''

def p_braced_keyval_list(p):
    '''BracedKeyvalList : empty
                 | KeyvalList OComma'''

def p_decl_name(p):
    '''DeclName : IDENT'''

def p_name(p):
    '''Name : IDENT'''

def p_arg_type(p):
    '''ArgType : NameOrType
        | IDENT NameOrType
        | IDENT DotDotDot
        | DotDotDot'''

def p_arg_type_list(p):
    '''ArgTypeList : ArgType
            | ArgTypeList COMMA ArgType'''


def p_oarg_type_list_ocomma(p):
    '''OArgTypeListOComma : empty
                   | ArgTypeList OComma'''

def p_stmt(p):
    '''Stmt : empty
            | CompoundStmt
            | CommonDecl
            | NonDeclStmt'''

def p_non_decl_stmt(p):
    '''NonDeclStmt : SimpleStmt
                | ForStmt
                | SwitchStmt
                | IfStmt
                | LabelName COLON Stmt
                | FALLTHROUGH
                | BREAK ONewName
                | CONTINUE ONewName
                | DEFER PseudoCall
                | GOTO NewName
                | RETURN OExprList'''

def p_dot_dot_dot(p):
    '''DotDotDot : ELPS
                | ELPS NType'''

def p_pexpr(p):
    '''PExpr : PExprNoParen
            | LPRN ExprOrType RPRN'''

def p_pexp_no_paren(p):
    '''PExprNoParen : Literal
                    | Name
                    | PExpr DOT IDENT
                    | PExpr DOT LPRN ExprOrType RPRN
                    | PExpr DOT LPRN TYPE RPRN
                    | PExpr LSQR Expr LSQR
                    | PExpr LSQR OExpr COLON OExpr LSQR
                    | PExpr LSQR OExpr COLON OExpr COLON OExpr LSQR
                    | PseudoCall
                    | ConvType SHL Expr OComma SHR
                    | CompType left_banana BracedKeyvalList right_banana
                    | PExpr left_banana BracedKeyvalList right_banana
                    | FuncLiteral
                    | ForCompExpr'''

def p_conv_type(p):
    '''ConvType : FuncType
                | OtherType'''

def p_comp_type(p):
    '''CompType : OtherType'''

def p_start_comp_lit(p):
    '''StartCompLit : empty'''

def p_key_val(p):
    '''Keyval : Expr COLON CompLitExpr'''

def p_bare_comp_lit_exp(p):
    '''BareCompLitExpr : Expr
                | left_banana BracedKeyvalList right_banana'''

def p_comp_lit_exp(p):
    '''CompLitExpr : Expr
            | left_banana BracedKeyvalList right_banana'''

def p_exp_or_type(p):
    '''ExprOrType : Expr
           | NonExprType'''

def p_name_or_type(p):
    '''NameOrType : NType'''

def p_switch_stmt(p):
    '''SwitchStmt : SWITCH IfHeader LCURL CaseBlockList RCURL'''

def p_mul_op(p):
    '''Mul_op : QUO
            | REM
            | SHL
            | SHR
            | AND
            | AND_XOR'''

def p_prec5expr_(p):
    '''Prec5Expr_ : UExpr
           | Prec5Expr_ Mul_op UExpr
           | Prec5Expr_ MUL UExpr'''

def p_prec4expr_(p):
    '''Prec4Expr_ : Prec5Expr_
           | Prec4Expr_ ADD Prec5Expr_
           | Prec4Expr_ SUB Prec5Expr_
           | Prec4Expr_ XOR Prec5Expr_
           | Prec4Expr_ OR Prec5Expr_'''

def p_rel_rop(p):
    '''Rel_op : EQL
                | NEQ
                | LEQ
                | GEQ
                | GTR
                | LSS'''

def p_prec3expr_(p):
    '''Prec3Expr_ : Prec4Expr_
           | Prec3Expr_ Rel_op Prec4Expr_'''

def p_prec2expr_(p):
    '''Prec2Expr_ : Prec3Expr_
           | Prec2Expr_ LAND Prec3Expr_'''

def p_expr(p):
    '''Expr       : Prec2Expr_
           | Expr LOR Prec2Expr_'''

def p_uexpr(p):
    '''UExpr : PExpr
      | NAND UExpr
      | MUL UExpr
      | ADD UExpr
      | SUB UExpr
      | XOR UExpr'''

def p_for_comp_expr(p):
    '''ForCompExpr : LSQR Expr pipe RangeStmt LSQR'''

def p_pseudocall(p):
    '''PseudoCall : PExpr LPRN RPRN
           | PExpr LPRN ExprOrTypeList OComma RPRN
           | PExpr LPRN ExprOrTypeList ELPS OComma RPRN'''
