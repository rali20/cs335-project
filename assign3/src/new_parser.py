import sys
import os
import ply.yacc as yacc

from new_lexer import *
from global_decls import *

root = ScopeTree(None, scopeName="global")
# global curr_scope
# print(curr_scope,1)
curr_scope = root
# print(curr_scope,2)

precedence = (
    ('right', 'AGN','ADD_AGN','SUB_AGN','MUL_AGN',
        'QUO_AGN','REM_AGN','AND_AGN','OR_AGN',
        'XOR_AGN','SHL_AGN','SHR_AGN','AND_NOT_AGN'),
    ('left', 'LOR'),
    ('left', 'LAND'),
    ('left', 'OR'),
    ('left', 'XOR'),
    ('left', 'AND'),
    ('left', 'EQL', 'NEQ'),
    ('left', 'LSS', 'GTR', 'LEQ', 'GEQ'),
    ('left', 'SHL', 'SHR', 'AND_NOT'),
    ('left', 'ADD', 'SUB'),
    ('left', 'MUL', 'QUO', 'REM'),
    ('right', 'NOT'),
    ('left', 'INC', 'DEC')
)

def p_start(p):
    '''start : SourceFile'''

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
    '''ImportStmt : ImportHere STRING_LIT'''

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
    global curr_scope
    if len(p)==5:
        # all types on right must be same as ntype
        for exp in p[4].value:
            if (p[2] != exp.type):
                # check if it is float = int case
                if exp.type=="int" and p[2]=="float":
                    exp.type = "float"
                    continue
                raise_typerror(p[1].value,  "type mis-match in var declaration")
        # incase type is declared to be some basic type e.g type new_int int;
        if p[2] in curr_scope.typeTable:
            p[2] = curr_scope.typeTable[p[2]]
        # insert
        for i in p[1].value:
            curr_scope.insert(i, type=p[2], is_var=1)

    elif len(p)==4:
        # check length of decllist and ExprList
        if len(p[1].value) != len(p[3].value):
            raise_out_of_bounds_error(p[1].value + p[3].value , "different number of variables and expressions")
        for i in range( len(p[1].value) ):
            curr_scope.insert(p[1].value[i], p[3].value[i].type, is_var=1)

    else:
        # incase type is declared to be some basic type e.g type new_int int;
        if p[2] in curr_scope.typeTable:
            p[2] = curr_scope.typeTable[p[2]]
        # insert
        for i in p[1].value:
            curr_scope.insert(i, type=p[2], is_var=1)

def p_const_decl(p):
    '''ConstDecl : DeclNameList NType AGN ExprList
                | DeclNameList AGN ExprList'''
    global curr_scope
    if len(p)==5:
        # check length of decllist and ExprList
        if len(p[1].value) != len(p[4].value):
            raise_out_of_bounds_error(p[1].value , "different number of variables and expressions")
        # all types on right must be same as ntype
        for exp in p[4].value:
            if (p[2] != exp.type):
                # check if it is float = int case
                if exp.type=="int" and p[2]=="float":
                    exp.type = "float"
                    continue
                raise_typerror(p[1].value, "type mis-match in const declaration")
        # incase type is declared to be some basic type e.g type new_int int;
        if p[2] in curr_scope.typeTable:
            p[2] = curr_scope.typeTable[p[2]]
        # insert all left sides
        for i in p[1].value:
            curr_scope.insert(i, p[2], is_var=0)
    else:
        # check length of decllist and ExprList
        if len(p[1].value) != len(p[3].value):
            raise_out_of_bounds_error(p[1].value + p[3].value , "different number of variables and expressions")
            # insert
        for i in range( len(p[1].value) ):
            curr_scope.insert(p[1].value[i], p[3].value[i].type, is_var=0)

def p_const_decl_1(p):
    '''ConstDecl1 : ConstDecl
                | DeclNameList NType
                | DeclNameList'''
    global curr_scope
    if len(p)==3:
        # incase type is declared to be some basic type e.g type new_int int;
        if p[2] in curr_scope.typeTable:
            p[2] = curr_scope.typeTable[p[2]]
        # insert
        for i in p[1].value:
            curr_scope.insert(i, p[2], is_var=0)

def p_type_decl_name(p):
    '''TypeDeclName : IDENT'''
    p[0] = p[1]

def p_type_decl(p):
    '''TypeDecl : TypeDeclName NType'''
    global curr_scope
    if p[2] in curr_scope.typeTable:
        p[2] = curr_scope.typeTable[p[2]]
    curr_scope.insert_type(p[1], p[2])
    # p[0] = container()
    # p[0].value = p[1]
    # p[0].type = p[2]

def p_inc_dec_op(p):
    '''IncDecOp : INC
                | DEC'''

def p_simple_stmt(p):
    '''SimpleStmt : Expr
                | Expr ShortAgnOp Expr
                | ExprList AGN ExprList
                | ExprList DEFN ExprList
                | Expr IncDecOp'''

def p_quick_assign_op(p):
    '''ShortAgnOp : ADD_AGN
                | SUB_AGN
                | MUL_AGN
                | QUO_AGN
                | REM_AGN
                | AND_AGN
                | OR_AGN
                | XOR_AGN
                | SHL_AGN
                | SHR_AGN
                | AND_NOT_AGN'''

def p_case(p):
    '''Case : CASE ExprList COLON
            | DEFAULT COLON'''

def p_compound_stmt(p):
    '''CompoundStmt : LCURL StartScope StmtList EndScope RCURL'''

def p_case_block(p):
    '''CaseBlock : Case StmtList'''

def p_case_block_list(p):
    '''CaseBlockList : empty
                    | CaseBlockList CaseBlock'''

def p_loop_body(p):
    '''LoopBody : LCURL StartScope StmtList EndScope RCURL'''

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
    '''ForStmt : FOR StartScope ForBody EndScope'''

def p_if_header(p):
    '''IfHeader : Expr
                | OSimpleStmt SEMCLN Expr'''

def p_if_stmt(p):
    '''IfStmt : IF StartScope IfHeader LoopBody ElseIfList ElseStmt EndScope'''

def p_else_if(p):
    '''ElseIf : ELSE IF IfHeader LoopBody'''

def p_else_if_list(p):
    '''ElseIfList : empty
                  | ElseIfList ElseIf'''

def p_else(p):
    '''ElseStmt : empty
                | ELSE CompoundStmt'''

def p_ntype(p):
    '''NType : FuncType
             |	OtherType
             |	PtrType
             |	DotName
             |	LPRN NType RPRN'''
    if len(p)==2:
        p[0] = p[1]
    else:
        p[0] = p[2]


def p_non_expr_type(p):
    '''NonExprType : FuncType
            | OtherType
            | MUL NonExprType'''

def p_other_type(p):
    '''OtherType : LSQR Expr RSQR NType
          | MAP LSQR NType RSQR NType
          | StructType
          | InterfaceType'''

def p_struct_type(p):
    '''StructType : STRUCT LCURL StructDeclList OSemi RCURL
           | STRUCT LCURL RCURL'''

def p_interface_type(p):
    '''InterfaceType : INTERFACE LCURL InterfaceDeclList OSemi RCURL
              | INTERFACE LCURL RCURL'''

def p_func_decl(p):
    '''FuncDecl : FUNC IDENT StartScope ArgList FuncRes FuncBody EndScope
                | FUNC LPRN_OR StartScope OArgTypeListOComma RPRN_OR IDENT ArgList FuncRes FuncBody EndScope'''

def p_func_body(p):
    '''FuncBody : empty
                | LCURL StmtList RCURL'''

def p_func_type(p):
    '''FuncType : FUNC ArgList FuncRes'''

def p_arg_list(p):
    '''ArgList : LPRN OArgTypeListOComma RPRN'''


def p_func_res(p):
    '''FuncRes : empty
               | FuncRetType
               | LPRN_OR OArgTypeListOComma RPRN_OR'''

def p_struct_decl_list(p):
    '''StructDeclList : StructDecl
                    | StructDeclList SEMCLN StructDecl'''

def p_interface_decl_list(p):
    '''InterfaceDeclList : InterfaceDecl
                        | InterfaceDeclList SEMCLN InterfaceDecl'''

def p_struct_decl(p):
    '''StructDecl : NewNameList NType OTag
                    | Embed OTag
                    | LPRN Embed RPRN OTag
                    | MUL Embed OTag
                    | LPRN MUL Embed RPRN OTag
                    | MUL LPRN Embed RPRN OTag'''

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
    #2nd rule's type is not being taken care of
    if len(p)==2:
        p[0] = p[1]
    else:
        p[0] = p[1]+"."+p[3]

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
    if len(p)==2:
        p[0] = container()
        p[0].value = [p[1]]
    else:
        p[0] = p[1]
        p[0].value.append(p[3])


def p_expr_or_type_list(p):
    '''ExprOrTypeList : ExprOrType
               | ExprOrTypeList COMMA ExprOrType'''

def p_otag(p):
    '''OTag : empty
         | STRING_LIT'''

def p_literal(p):
    '''Literal : INTEGER_LIT
        | OCTAL_LIT
        | HEX_LIT
        | IMAGINARY_LIT
        | FLOAT_LIT
        | RUNE_LIT
        | STRING_LIT'''
    if(type(p[1])==int):
        p[0] = container(type="int", value=p[1])
    elif(type(p[1])==float):
        p[0] = container(type="float", value=p[1])
    elif(type(p[1])==str):
        p[0] = container(type="string", value=p[1])


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
    # if len(p)==2:
    #     p[0] = container()
    #     p[0].value = [p[1].value]
    #     p[0].type =

def p_decl_name_list(p):
    '''DeclNameList : DeclName
             | DeclNameList COMMA DeclName'''
    if len(p)==2:
        p[0] = container(value=[p[1].value])
    else:
        p[0] = container()
        p[0].value = p[1].value
        p[0].value.append(p[3].value)

def p_stmt_list(p):
    '''StmtList : Stmt
         | StmtList SEMCLN Stmt'''

def p_new_name_list(p):
    '''NewNameList : NewName
            | NewNameList COMMA NewName'''

def p_keyval_list(p):
    '''KeyvalList : Keyval
           | CompLitExpr
           | KeyvalList COMMA Keyval
           | KeyvalList COMMA CompLitExpr'''

def p_braced_keyval_list(p):
    '''BracedKeyvalList : empty
                 | KeyvalList OComma'''

def p_decl_name(p):
    '''DeclName : IDENT'''
    p[0] = container(value=p[1])

def p_name(p):
    '''Name : IDENT'''
    p[0] = p[1]

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
                | DEFER Expr
                | GOTO NewName
                | RETURN OExprList'''

def p_dot_dot_dot(p):
    '''DotDotDot : ELPS
                | ELPS NType'''

def p_pexpr(p):
    '''PExpr : PExprNoParen
            | LPRN ExprOrType RPRN'''
    if len(p)==2:
        p[0] = p[1]
    else:
        p[0] = p[2]


def p_pexp_no_paren(p):
    '''PExprNoParen : Name
                    | PExpr DOT IDENT
                    | PExpr DOT LPRN ExprOrType RPRN
                    | PExpr DOT LPRN TYPE RPRN
                    | PExpr LSQR Expr RSQR
                    | PExpr LSQR OExpr COLON OExpr RSQR
                    | PExpr LSQR OExpr COLON OExpr COLON OExpr RSQR
                    | PseudoCall
                    | ConvType LPRN Expr OComma RPRN
                    | CompType LCURL BracedKeyvalList RCURL
                    | FuncLiteral
                    | ForCompExpr'''
    global curr_scope
    p[0] = container()
    if len(p)==2:
        p[0].value = p[1] #name is a string
        p[0].type = curr_scope.lookup(p[1])["type"]
    # elif len(p)==

def p_exp_no_paren2(p):
    '''PExprNoParen : Literal'''
    # literal is a container with value and type
    p[0] = p[1]

def p_conv_type(p):
    '''ConvType : FuncType
                | OtherType'''

def p_comp_type(p):
    '''CompType : OtherType'''

def p_key_val(p):
    '''Keyval : Expr COLON CompLitExpr'''

def p_comp_lit_exp(p):
    '''CompLitExpr : Expr
                   | LCURL BracedKeyvalList RCURL'''

def p_exp_or_type(p):
    '''ExprOrType : Expr
           | NonExprType'''

def p_name_or_type(p):
    '''NameOrType : NType'''

def p_switch_stmt(p):
    '''SwitchStmt : SWITCH StartScope IfHeader LCURL CaseBlockList RCURL EndScope'''

def p_expr(p):
    '''Expr : UExpr
            | Expr LOR Expr
            | Expr LAND Expr
            | Expr EQL Expr
            | Expr NEQ Expr
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
            | Expr AND Expr
            | Expr AND_NOT Expr'''
    if len(p)==4:
        p[0] = container()
        if p[1].type != p[3].type:
            # check if it is float = int case
            if (p[1].type=="float" or p[3].type=="float") and (p[1].type=="int" or p[3].type=="int"):
                p[1].type = "float"
                p[3].type = "float"
            else:
                raise_typerror(p, "type error in expression operations")
        p[0].type = p[1].type
        p[0].value = str(p[1].value) + p[2] + str(p[3].value)
    else:
        p[0] = p[1]


def p_uexpr(p):
    '''UExpr : PExpr
             | UnaryOp UExpr'''
    if len(p)==2:
        p[0] = p[1]
    else:
        p[0] = p[2] #default
        # switch (p[1]){
        # case "+":
        #     p[0] = p[2]
        #     break
        # case "-":
        #     p[0] = p[2]
        #     break;
        # case "!":
        #     if p[2].type == "float":
        #         raise_typerror(p, "Invalid operand for float")
        #     p[0].type = p[2].type
        #     p[0].value = p[1]+p[2].value
        #     break;
        # # case "^": to do
        # }



def p_unary_op(p):
    '''UnaryOp : ADD
               | SUB
               | NOT
               | XOR
               | MUL
               | AND'''
    p[0] = p[1]

def p_for_comp_expr(p):
    '''ForCompExpr : LSQR Expr OR RangeStmt RSQR'''

def p_pseudocall(p):
    '''PseudoCall : PExpr LPRN RPRN
                  | PExpr LPRN ExprOrTypeList OComma RPRN
                  | PExpr LPRN ExprOrTypeList ELPS OComma RPRN'''

def p_empty(p):
    '''empty : '''

def p_start_scope(p):
    '''StartScope : empty'''
    global curr_scope
    curr_scope = curr_scope.makeChildren()

def p_end_scope(p):
    '''EndScope : empty'''
    global curr_scope
    curr_scope = curr_scope.parent

def p_error(p):
    global curr_scope
    print(p)
    print("syntax error")
    print(curr_scope.identity)


# root = ScopeTree("global", None)
# # global curr_scope
# curr_scope = root
parser = yacc.yacc()


with open("factorial.go", "r") as f:
    data = f.read()
result = parser.parse(data)


def print_scopeTree(node):
    temp = node
    print("")
    print("me:", temp.identity)
    for i in temp.children:
        print("child:", i.identity)
    print("symbolTable:")
    for var, val in temp.symbolTable.items():
        print(var, val["type"], val["is_var"])
    print("TypeTable:")
    for new_type, Ntype in temp.typeTable.items():
        print(new_type, Ntype)

    for i in temp.children:
        print_scopeTree(i)
print_scopeTree(root)
