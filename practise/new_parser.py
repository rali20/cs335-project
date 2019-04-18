#!/usr/bin/env python3

import sys
import os
import ply.yacc as yacc
import argparse
import pprint

from lexer import *
from global_decls import *

global root
root = ScopeTree(None, scopeName="global")
curr_scope = root

precedence = (
    ('right', 'AGN'),
    ('left', 'LOR'),
    ('left', 'LAND'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQL', 'NEQ'),
    ('left', 'LSS', 'GTR', 'LEQ', 'GEQ'),
    ('left', 'SHL', 'SHR'),
    ('left', 'ADD', 'SUB'),
    ('left', 'MUL', 'QUO', 'REM'),
    ('right', 'NOT')
)

def p_start(p):
    '''start : SourceFile'''
    global root
    p[1].extra["__init__"] = p[1].code
    p[0] = root,p[1].extra

def p_source_file(p):
    '''SourceFile : empty
                  | DeclList'''
    p[0] = p[1]

def p_decl_list(p):
    '''DeclList : TopLevelDecl
    			| TopLevelDecl DeclList'''
    p[0] = container()
    if len(p) == 2:
        if p[1].type == "FuncDecl":
            p[0].extra = p[1].extra
        else :
            p[0].code = p[1].code
    else :
        p[0] = p[2]
        if p[1].type == "FuncDecl":
            p[0].extra = {**p[0].extra,**p[1].extra}
        else :
            p[0].code = p[1].code+ p[2].code

def p_top_level_decl(p):
    '''TopLevelDecl : CommonDecl SEMCLN
    				| FuncDecl'''
    p[0] = container()
    if len(p)==2 :
        p[0].type = "FuncDecl"
        if p[1].extra["type"] == "defn":
            p[0].extra[p[1].extra["name"]] = p[1].code
    else :
        p[0].type = "CommonDecl"
        p[0].code = p[1].code

def p_common_decl(p):
    '''CommonDecl : CONST ConstDecl
                  | VAR VarDecl
                  | TYPE TypeDecl'''
    p[0] = container()
    p[0].code = p[2].code

def p_var_decl(p):
    '''VarDecl : DeclNameList Type
               | DeclNameList Type AGN ExprList'''
    global curr_scope
    # print("===========", p[2])
    p[0] = container()

    if len(p)==5:
        # check length of decllist and ExprList
        if len(p[1].value) != len(p[4].value):
            raise_out_of_bounds_error(p[1].value,
                "different number of variables and expressions",line=p.slice[3].lineno)
        p[0].code = p[4].code
        # all types on right must be same as Type
        for i in range(len(p[4].value)):
            p[1].value[i] = curr_scope.insert(p[1].value[i],type=p[2].type,is_var=1)
            exp = p[4].value[i]
            if (p[2].type.name != exp.type.name):
                # check if it is float = int case
                if  p[2].type.name=="float" and exp.type.name=="int":
                    p[0].code.append(UOP(dst=p[1].value[i], op="iTf", arg1=exp.value))
                else:
                    raise_typerror(p[2].type.name+' != '+exp.type.name,  "type mis-match in var declaration",line=p.slice[3].lineno)
            else:
                p[0].code.append(ASN(dst=p[1].value[i], arg1=exp.value))
    else:
        for i in range(len(p[1].value)):
            p[1].value[i] = curr_scope.insert(p[1].value[i],type=p[2].type,is_var=1)

def p_decl_name_list(p):
    '''DeclNameList : Name
    				| DeclNameList COMMA Name'''
    if len(p)==2:
        p[0] = container(value=[p[1]])
    else:
        p[0] = p[1]
        p[0].value.append(p[3])

def p_const_decl(p):
    '''ConstDecl : DeclNameList Type AGN ExprList'''
    global curr_scope
    p[0] = container()
    # incase type is declared to be some basic type e.g type new_int int;
    if p[2] in curr_scope.typeTable:
        p[2] = curr_scope.typeTable[p[2]]["type"]
    p[0].code = p[4].code
    # all types on right must be same as Type
    for i in range(len(p[4].value)):
        # first insert
        p[1].value[i] = curr_scope.insert(p[1].value[i], type=p[2], is_var=0)
        exp = p[4].value[i]
        if (p[2] != exp.type):
            # check if it is float = int case
            if exp.type=="int" and p[2]=="float":
                exp.type = "float"
                p[0].code.append(UOP(dst=p[1].value[i], op="iTf", arg1=exp.value))
            else:
                raise_typerror(p[1].value,  "type mis-match in var declaration",line=p.slice[3].lineno)
        else:
            p[0].code.append(ASN(dst=p[1].value[i], arg1=exp.value))

def p_type_decl_name(p):
    '''TypeDeclName : IDENT'''
    p[0] = p[1]

def p_type_decl(p):
    '''TypeDecl : TypeDeclName Type'''
    global curr_scope
    p[0] = container()
    if p[2].type in curr_scope.typeTable:
        p[2].type = curr_scope.typeTable[p[2].type]["type"]
    curr_scope.insert_type(p[1], p[2].type)

def p_simple_stmt(p):
    '''SimpleStmt : Expr
                  | ExprList AGN ExprList
                  | ExprList DEFN ExprList'''
    # a,b = 1
    # a,b,c = 2,3,2
    # check if const is changed
    global curr_scope
    if len(p)==2:
        p[0] = p[1]
    else:
        if len(p[1].value) != len(p[3].value):
            raise_out_of_bounds_error(p[1].value+p[3].value,
                "error in short var decl/assignment",line=p.slice[2].lineno)
        if p[2] == ":=" :
            raise_general_error("\n := is not implemented by us. sorry! \n",line=p.slice[2].lineno)
            pass
        elif p[2] == "=" :
            p[0] = container()
            # for expr in p[1].value:
            #     if curr_scope.lookup_by_uniq_id(expr.value)["is_var"]==0:
            #         raise_typerror(expr.value, ": Can't assign to a constant")
            p[0].code += p[3].code
            for i in range(len(p[1].value)):
                expr = p[1].value[i]
                valexpr = p[3].value[i]
                flag = False
                if "dereference" in expr.extra :
                    flag = expr.extra["dereference"]
                if expr.type.name == valexpr.type.name :
                    if expr.type.name in set({"int","float","string","pointer"}) :
                        if not flag :
                            p[0].code += expr.code
                            p[0].code.append(ASN(dst=expr.value,arg1=valexpr.value))
                        else :
                            p[0].code += expr.code[:-1]
                            p[0].code.append(PVA(dst=expr.extra["left_place"],arg1=valexpr.value))
                    else :
                        raise_general_error("Not Implemented",line=p.slice[2].lineno)
                elif (expr.type.name == "float") and (valexpr.type.name == "int") :
                    if not flag :
                        p[0].code += expr.code
                        p[0].code.append(UOP(dst=expr.value,op="iTf",arg1=valexpr.value))
                    else :
                        p[0].code += expr.code[:-1]
                        new_place = curr_scope.new_temp(type=valexpr.type)
                        p[0].code.append(UOP(dst=new_place,op="iTf",arg1=valexpr.value))
                        p[0].code.append(PVA(dst=expr.extra["left_place"],arg1=new_place))
                else :
                    raise_typerror(expr.type.name + ' != '  +valexpr.type.name, "in assignment : operands are different type",line=p.slice[2].lineno)

def p_stmt_block(p):
    '''StmtBlock : LCURL StartScope StmtList EndScope RCURL'''
    p[0] = p[3]

def p_block(p):
    '''Block : LCURL StmtList RCURL'''
    p[0] = p[2]

def p_for_header(p):
    '''ForHeader : OSimpleStmt SEMCLN OSimpleStmt SEMCLN OSimpleStmt
                 | OSimpleStmt'''
    p[0] = container()
    if len(p)==2 :
        p[0].value = [container(),p[1],container()]
    else :
        p[0].value = [p[1],p[3],p[5]]

def p_for_body(p):
    '''ForBody : ForHeader Block'''
    global curr_scope
    p[0] = container()
    block = p[2]
    initial,expr,update = p[1].value
    labelBegin = curr_scope.new_label()
    labelAfter = curr_scope.find_label("#forAfter")
    labelUpdate = curr_scope.find_label("#forUpdate")
    p[0].code += initial.code
    p[0].code.append(LBL(arg1=labelBegin))
    p[0].code += expr.code
    p[0].code.append(CBR(arg1=expr.value,op=expr.type.name+"==",arg2=0,dst=labelAfter))
    p[0].code += block.code
    p[0].code.append(LBL(arg1=labelUpdate))
    p[0].code += update.code
    # need to take care of break, continue - unlabelled
    p[0].code.append(CMD(op="goto",arg1=labelBegin))
    p[0].code.append(LBL(arg1=labelAfter))

def p_for_stmt(p):
    '''ForStmt : FOR beginFor ForBody endFor'''
    p[0] = p[3]
    p[4].identity["type"] = "ForLoop"

def p_begin_for(p):
    '''beginFor :'''
    global curr_scope
    curr_scope = curr_scope.makeChildren()
    labelAfter = curr_scope.new_label()
    labelUpdate = curr_scope.new_label()
    curr_scope.insert_label(id="#forAfter",value=labelAfter)
    curr_scope.insert_label(id="#forUpdate",value=labelUpdate)

def p_end_for(p):
    '''endFor :'''
    global curr_scope
    to_return = curr_scope
    curr_scope = curr_scope.parent
    p[0] = to_return

def p_if_stmt(p):
    '''IfStmt : IF Expr StmtBlock
              | IF Expr StmtBlock ElseStmt
              | IF Expr StmtBlock ElifList ElseStmt'''
    global curr_scope
    if len(p)==4 :
        labelAfter = curr_scope.new_label()
        p[0] = p[2]
        p[0].code.append(CBR(arg1=p[2].value,op=p[2].type.name+"==",arg2=0,dst=labelAfter))
        p[0].code += p[3].code
        p[0].code.append(LBL(arg1=labelAfter))
    elif len(p)==5 :
        labelElse = curr_scope.new_label()
        labelAfter = curr_scope.new_label()
        p[0] = p[2]
        p[0].code.append(CBR(arg1=p[2].value,op=p[2].type.name+"==",arg2=0,dst=labelElse))
        p[0].code += p[3].code
        p[0].code.append(CMD(op="goto",arg1=labelAfter))
        p[0].code.append(LBL(arg1=labelElse))
        p[0].code += p[4].code
        p[0].code.append(LBL(arg1=labelAfter))
    else :
        labelAfter = curr_scope.new_label()
        # If
        labelFalse = curr_scope.new_label()
        p[0] = p[2]
        p[0].code.append(CBR(arg1=p[2].value,op=p[2].type.name+"==",arg2=0,dst=labelFalse))
        p[0].code += p[3].code
        p[0].code.append(CMD(op="goto",arg1=labelAfter))
        p[0].code.append(LBL(arg1=labelFalse))
        # ElifList
        for expr,block in p[4].value :
            labelFalse = curr_scope.new_label()
            p[0].code += expr.code
            p[0].code.append(CBR(arg1=expr.value,op=expr.type.name+"==",arg2=0,dst=labelFalse))
            p[0].code += block.code
            p[0].code.append(CMD(op="goto",arg1=labelAfter))
            p[0].code.append(LBL(arg1=labelFalse))
        # Else
        p[0].code += p[5].code
        p[0].code.append(LBL(arg1=labelAfter))

def p_else_if_list(p):
    '''ElifList : ElifStmt
                | ElifList ElifStmt'''
    if len(p)==2 :
        p[0] = container()
        p[0].value = [ p[1].value ]
    else :
        p[0] = p[1]
        p[0].value.append(p[2].value)

def p_else_if(p):
    '''ElifStmt : ELIF Expr StmtBlock'''
    p[0] = container()
    p[0].value = [p[2],p[3]]

def p_else_stmt(p):
    '''ElseStmt : ELSE StmtBlock'''
    p[0] = p[2]

def p_type(p):
    '''Type : Name
			| StructType
			| ArrayType
            | PtrType
			| LPRN Type RPRN'''
    global curr_scope
    p[0] = container()
    if len(p)==2:
        if str(p.slice[1]) == "Name" :
            if p[1] in curr_scope.typeTable :
                p[0].type = curr_scope.typeTable[p[1]]
            else :
                p[0].type = dType(name=p[1])
                p[0].type.size = curr_scope.sizeof(p[0].type)
        else:
            p[0] = p[1]
    else:
        p[0] = p[2]

def p_array_type(p):
    '''ArrayType : LSQR Expr RSQR Type'''
    global curr_scope
    p[0] = container()
    p[0].code = p[4].code + p[2].code
    p[0].type = dType(name="array",length=p[2].extra["array_length"],base=p[4].type)
    p[0].type.size = curr_scope.sizeof(p[0].type)

def p_struct_type(p):
    '''StructType : STRUCT LCURL StructDeclList OSemi RCURL'''
    # StructDeclList is a dictionary {ident:dType()}
    global curr_scope
    p[0] = container()
    p[0].type = dType(name="structure",field_dict=p[3])
    size = curr_scope.sizeof(p[0].type)
    p[0].type.size = size

def p_func_decl(p):
    '''FuncDecl : FUNC IDENT beginFunc Parameters FuncRes FuncBody endFunc'''
    p[0] = container()
    p[7]["scope"].identity["name"] = p[2]
    global curr_scope
    p[0].extra["name"] = p[2]
    if p[6] is None :
        if not curr_scope.lookup(p[2]) :
            curr_scope.insert(p[2], type=dType(name="func"), arg_list=p[4].type,
                ret_type=p[5].type, is_var=0)
        else :
            raise_typerror("name = "+p[2], "identifier type mismatch/ function redeclared",line=p.slice[2].lineno)
        p[0].extra["type"] = "decl"
    else :
        lookup_result =  curr_scope.lookup(p[2])
        if lookup_result :
            if lookup_result["is_var"] :
                raise_typerror("name = "+p[2], "Function Defined multiple times",line=p.slice[2].lineno)
        curr_scope.insert(p[2], type=dType(name="func"), arg_list=p[4].type,ret_type=p[5].type, is_var=1)
        # p[0].code.append(LBL(arg1="func "+p[2]))
        p[0].code.append(CMD(op="BeginFunc",arg1=p[7]["offset"]))
        p[0].code += p[4].code
        p[0].code += p[6].code
        p[0].code.append(OP(op="EndFunc"))
        p[0].extra["type"] = "defn"

def p_begin_func(p):
    '''beginFunc :'''
    global curr_scope
    global offset
    offset = 0
    curr_scope.reset_offset()
    curr_scope = curr_scope.makeChildren()

def p_parameters(p):
    '''Parameters : LPRN RPRN
                  | LPRN ParamList RPRN'''
    if len(p)==3 :
        p[0] = container()
        p[0].type = list()
    else :
        p[0] = p[2]
        for i in range(len(p[2].value)):
            reg = len(p[2].value)-i-1
            p[0].code.append(MISC(op="store", arg1=p[2].value[i], arg2=reg))

def p_param_list(p):
    '''ParamList : ParamDecl
                 | ParamList COMMA ParamDecl'''
    if len(p)==2 :
        p[0] = p[1]
    else :
        p[0] = p[1]
        p[0].type += p[3].type
        p[0].value += p[3].value
        p[0].code += p[3].code

def p_param_Decl(p):
    '''ParamDecl : IDENT Type'''
    global curr_scope
    p[0] = container()
    typ = None
    if type(p[2])==container:
        typ = p[2].type
    else:
        typ = p[2]
    p[0].type = [p[2].type]
    u_id = curr_scope.insert(id=p[1],type=p[2].type)
    p[0].value = [u_id]


def p_func_body(p):
    '''FuncBody : SEMCLN
                | Block'''
    if p[1] == ";" :
        p[0] = None
    else :
        p[0] = p[1]

def p_func_res(p):
    '''FuncRes : empty
               | Type'''
    global curr_scope
    p[0] = container()
    if str(p.slice[1]) == "empty" :
        p[0].type = dType()
        curr_scope.insert_type("#return",dType())
    else :
        p[0].type = p[1].type
        curr_scope.insert_type("#return",p[1].type)

def p_end_func(p):
    '''endFunc :'''
    global curr_scope
    offset = curr_scope.temp_offset
    p[0] = {"offset":offset, "scope":curr_scope}
    # offset gives you the total space used by any (scope+it's scildren scopes)
    curr_scope = curr_scope.parent

def p_struct_decl_list(p):
    '''StructDeclList : StructDecl
                      | StructDeclList SEMCLN StructDecl'''
    global curr_scope
    if len(p)==2:
        p[0] = {}
        for field_name in p[1].value:
            p[0][field_name] = p[1].type
    else:
        p[0] = p[1]
        for field_name in p[3].value:
            p[0][field_name] = p[3].type

def p_struct_decl(p):
    '''StructDecl : FieldList Type'''
    # consider only the first rule
    # FieldList is a list
    p[0] = container()
    p[0].value = p[1]
    p[0].type = p[2].type

def p_label_name(p):
    '''LabelName : NewName'''
    global curr_scope
    curr_scope.insert(p[1], type=dType(name="label"), is_var=0)
    p[0] = p[1]

def p_new_name(p):
    '''NewName : IDENT'''
    p[0] = p[1]

def p_field_name(p):
    '''FieldName : IDENT'''
    p[0] = p[1]

def p_ptr_type(p):
    '''PtrType : MUL Type'''
    p[0] = container()
    p[0].type = dType(name="pointer",base=p[2].type)
    # TODO why array here? why not pointer?

def p_osemi(p):
    '''OSemi : empty
             | SEMCLN'''

def p_osimple_stmt(p):
    '''OSimpleStmt : empty
                   | SimpleStmt'''
    p[0] = p[1]

def p_oexpr(p):
    '''OExpr : empty
             | Expr'''
    p[0] = p[1]

def p_expr_list(p):
    '''ExprList : Expr
                | ExprList COMMA Expr'''
    if len(p)==2:
        p[0] = container()
        p[0].value = [p[1]]
        p[0].code = p[1].code
    else:
        p[0] = p[1]
        p[0].value.append(p[3])
        p[0].code += p[3].code

def p_basic_lit(p):
    '''BasicLit : INTEGER_LIT
                | FLOAT_LIT
                | STRING_LIT'''
    global curr_scope
    if type(p[1]) == int:
        new_place = curr_scope.new_temp(type=dType(name="int"))
        p[0] = container(type=dType(name="int"), value=new_place)
        p[0].extra["array_length"] = p[1]
        p[0].code.append(ASN(dst=new_place, arg1=p[1],op="int="))
    elif type(p[1]) == float:
        new_place = curr_scope.new_temp(type=dType(name="float"))
        p[0] = container(type=dType(name="float"), value=new_place)
        p[0].code.append(ASN(dst=new_place, arg1=p[1],op="float="))
    else :
        new_place = curr_scope.new_temp(type=dType(name="string"))
        p[0] = container(type=dType(name="string"), value=new_place)
        p[0].code.append(ASN(dst=new_place, arg1=p[1],op="str="))


def p_stmt_list(p):
    '''StmtList : empty
                | StmtList Stmt'''
    p[0] = container()
    if len(p) == 2:
        p[0] = container()
    else :
        p[0] = p[1]
        p[0].code += p[2].code

def p_field_list(p):
    '''FieldList : FieldName
            	 | FieldList COMMA FieldName'''
    if len(p)==2:
        p[0] = [p[1]]
    else:
        p[0] = p[1]
        p[0].append(p[3])

def p_name(p):
    '''Name : IDENT'''
    p[0] = p[1]

def p_stmt(p):
    '''Stmt : StmtBlock
            | CommonDecl SEMCLN
            | NonDeclStmt'''
    p[0] = p[1]

def p_non_decl_stmt(p):
    '''NonDeclStmt : ForStmt
                   | IfStmt
                   | SimpleStmt SEMCLN
                   | BREAK SEMCLN
                   | CONTINUE SEMCLN
                   | GOTO NewName SEMCLN
                   | RETURN OExpr SEMCLN
                   | LabelName COLON Stmt'''
    global curr_scope
    p[0] = container()
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3 :
        if p[1] == "break" :
            brk_lbl = curr_scope.find_label("#forAfter")
            p[0].code.append(CMD(op="goto",arg1=brk_lbl))
        elif p[1] == "continue" :
            cont_lbl = curr_scope.find_label("#forUpdate")
            p[0].code.append(CMD(op="goto",arg1=cont_lbl))
        else :
            p[0] = p[1]
    else :
        p[0] = container()
        if str(p.slice[1]) == "LabelName" :
            p[0].code.append(LBL(arg1=p[1]))
            p[0].code += p[3].code
        elif p[1] == "goto" :
            p[0].code.append(CMD(op="goto",arg1=p[2]))
        else : # return
            p[0] = container()
            ret_type = curr_scope.typeTable["#return"]
            if ret_type.name == p[2].type.name :
                if ret_type.name is None :
                    p[0].code.append(OP(op="return"))
                else :
                    p[0].code += p[2].code
                    p[0].code.append(CMD(op="return",arg1=p[2].value))
            else :
                raise_typerror(str(ret_type.name) +' == ' + p[2].type.name, "in return statement : "
                    + "type mismatch",line=p.slice[1].lineno)

def p_pexpr(p):
    '''PExpr : Name
             | BasicLit
             | FuncCall
             | LPRN Expr RPRN
             | PExpr DOT IDENT
             | PExpr LSQR Expr RSQR'''
    global curr_scope
    p[0] = container()
    if len(p)==2 :
        if str(p.slice[1]) == "Name":
            lookup_result = curr_scope.lookup(p[1])
            if lookup_result is not None:
                # p[0].value = p[1] #name is a string
                p[0].value = lookup_result["uniq_id"]
                p[0].type = lookup_result["type"]
            else:
                raise_general_error("undeclared variable : " + p[1])
        else :
            p[0] = p[1]
    elif len(p)==4 :
        if p[1] == "(" :
            p[0] = p[2]
        else : # structure access
            if p[1].type.name != "structure":
                raise_typerror("arg_type = "+p[1].type.name, "in primay expression : "
                    + "DOT can be used only with structures",line=p.slice[2].lineno)

            field_dict = p[1].type.field_dict
            if p[3] not in field_dict:
                raise_typerror("selector = "+p[3], "in primay expression : "
                    + "field not in structure",line=p.slice[2].lineno)
            # find the address/offset first
            field_offset=0
            for field_name in field_dict:
                if field_name == p[3]:
                    break
                else:
                    field_offset += field_dict[field_name].size
            flag = False
            if "dereference" in p[1].extra :
                flag = p[1].extra["dereference"]

            new_place = curr_scope.new_temp(type=field_dict[p[3]])
            new_place1 = curr_scope.new_temp(type=dType(name="int"))
            new_place2 = curr_scope.new_temp(type=dType(name="int"))

            if not flag :
                p[0].code += p[1].code
                p[0].code.append(ASN(dst=new_place2, arg1=str(field_offset),op="int="))
                p[0].code.append(BOP(dst=new_place1,op="int+",arg1=p[1].value,arg2=new_place2))
                p[0].code.append(UOP(dst=new_place,op="*",arg1=new_place1))
            else :
                p[0].code += p[1].code[:-1]
                p[0].code.append(ASN(dst=new_place2, arg1=str(field_offset),op="int="))
                p[0].code.append(BOP(dst=new_place1,op="int+",arg1=p[1].extra["left_place"],arg2=new_place2))
                p[0].code.append(UOP(dst=new_place,op="*",arg1=new_place1))

            p[0].value = new_place
            p[0].type = field_dict[p[3]]
            p[0].extra["dereference"] = True
            p[0].extra["left_place"] = new_place1
    else : # array access
        if p[3].type.name != "int" :
            raise_typerror("index_type = "+p[3].type.name, "in primay expression : "
                + "index has to be int",line=p.slice[2].lineno)

        access_code = list()
        if p[1].type.name != "array" :
            raise_typerror("arg_type = "+p[1].type.name, "in primay expression : "
                + "non array type trying to access array",line=p.slice[2].lineno)

        flag = False
        if "dereference" in p[1].extra :
            flag = p[1].extra["dereference"]

        base_size = p[1].type.base.size
        new_place = curr_scope.new_temp(type=p[1].type.base)
        new_place1 = curr_scope.new_temp(type=dType(name="int"))
        new_place2 = curr_scope.new_temp(type=dType(name="int"))
        base_size_temp = curr_scope.new_temp(type=dType(name="int"))

        if not flag :
            p[0].code += p[1].code
            p[0].code += p[3].code
            access_code.append(ASN(dst=base_size_temp,arg1=base_size,op="int="))
            access_code.append(BOP(dst=new_place2,arg1=p[3].value,op="int*",arg2=base_size_temp))
            access_code.append(BOP(dst=new_place1,arg1=p[1].value,op="int+",arg2=new_place2))
            access_code.append(UOP(dst=new_place,op="*",arg1=new_place1))
        else :
            p[0].code += p[1].code[:-1]
            p[0].code += p[3].code
            access_code.append(ASN(dst=base_size_temp,arg1=base_size,op="int="))
            access_code.append(BOP(dst=new_place2,arg1=p[3].value,op="int*",arg2=base_size_temp))
            access_code.append(BOP(dst=new_place1,arg1=p[1].extra["left_place"],op="int+",arg2=new_place2))
            access_code.append(UOP(dst=new_place,op="*",arg1=new_place1))

        p[0].value = new_place
        p[0].type = p[1].type.base
        p[0].extra["dereference"] = True
        p[0].extra["left_place"] = new_place1
        # for now
        p[0].code += access_code

def p_func_call(p):
    '''FuncCall : Name LPRN RPRN
    			| Name LPRN ExprList RPRN'''
    global curr_scope
    p[0] = container()
    lookup_result = curr_scope.lookup(p[1])
    if lookup_result is None:
        raise_general_error("undeclared function: " + p[1],line=p.slice[2].lineno)
    if len(p)==4 :
        if lookup_result["ret_type"] is None :
            p[0].code.append(CMD(op="pcall",arg1=p[1]))
            p[0].type = dType(name="void")
        else :
            p[0].type = lookup_result["ret_type"]
            new_place = curr_scope.new_temp(type=lookup_result["ret_type"])
            p[0].code.append(UOP(dst=new_place,op="call",arg1=p[1]))
            p[0].value = new_place
    else :
        p[0].code += p[3].code
        type_list = lookup_result["arg_list"]
        expr_list = p[3].value
        num_args = len(type_list)
        if num_args != len(expr_list) :
            raise_typerror(str(num_args)+' != '+str(len(expr_list)),"No of arguments do not match in function "+p[1],line=p.slice[2].lineno)
        pop_size = 0
        for i in range(num_args-1,-1,-1):
            expr = expr_list[i]
            if type_list[i].name != expr.type.name :
                # print(type_list[i].__dict__,expr.type.__dict__)
                raise_typerror(type_list[i].name + " != "+ expr.type.name,
                    "type mismatch in function "+p[1],line=p.slice[2].lineno)
            pop_size += curr_scope.sizeof(expr.type)
            p[0].code.append(CMD(op="push_param",arg1=expr.value))
        if lookup_result["ret_type"].name is None :
            p[0].code.append(CMD(op="pcall",arg1=p[1]))
            p[0].value = None
            p[0].type = dType(name="void")
        else :
            p[0].type = lookup_result["ret_type"]
            new_place = curr_scope.new_temp(type=lookup_result["ret_type"])
            p[0].code.append(UOP(dst=new_place,op="call",arg1=p[1]))
            p[0].value = new_place
        p[0].code.append(CMD(op="pop_param",arg1=pop_size))

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
            | Expr QUO Expr
            | Expr REM Expr
            | Expr SHL Expr
            | Expr SHR Expr
            | Expr ADD Expr
            | Expr SUB Expr
            | Expr MUL Expr
            | Expr AND Expr'''
    # check if undeclared variable is used
    global curr_scope
    if len(p) == 2 :
        p[0] = p[1]
    else:
        p[0] = container()
        p[0].code = p[1].code + p[3].code
        # int only operators
        if p[2] in set({"||","&&","&","|","<<",">>","%"}):
            new_place = curr_scope.new_temp(type=dType(name="int"))
            if p[1].type.name == "int" and p[3].type.name == "int":
                 p[0].code.append(BOP(dst=new_place,arg1=p[1].value,op=p[2],arg2=p[3].value))
                 p[0].type = p[1].type
            else :
                raise_typerror("arg1_type = "+p[1].type.name+", arg2_type = "+p[3].type.name, "in expression : "
                    + p[2] + " operator takes int operands only",line=p.slice[2].lineno)
        # int or float
        elif (p[2] in set({"+","-","*","/"})):
            if ((p[1].type.name == "int" and p[3].type.name == "int")
                    or (p[1].type.name == "float" and p[3].type.name == "float")) :
                new_place = curr_scope.new_temp(type=dType(name=p[1].type.name))
                p[0].code.append(BOP(dst=new_place,arg1=p[1].value,op=p[1].type.name+str(p[2]),arg2=p[3].value))
                p[0].type = p[1].type
                # print("BOP:int only",p[0].code[0])
            elif p[1].type.name == "int" and p[3].type.name == "float" :
                new_place = curr_scope.new_temp(type=dType(name="float"))
                new_place1 = curr_scope.new_temp(type=dType(name="float"))
                p[0].code.append(UOP(dst=new_place1,op="iTf",arg1=p[1].value))
                p[0].code.append(BOP(dst=new_place,arg1=new_place1,op="float"+str(p[2]),arg2=p[3].value))
                p[0].type = p[3].type
            elif p[1].type.name == "float" and p[3].type.name == "int" :
                new_place = curr_scope.new_temp(type=dType(name="float"))
                new_place1 = curr_scope.new_temp(type=dType(name="float"))
                p[0].code.append(UOP(dst=new_place1,op="iTf",arg1=p[3].value))
                p[0].code.append(BOP(dst=new_place,arg1=p[1].value,op="float"+str(p[2]),arg2=new_place1))
                p[0].type = p[1].type
            else :
                raise_typerror("arg1_type = "+p[1].type.name+", arg2_type = "+p[3].type.name, "in expression : "
                    + p[2] + " operator takes int or float operands only",line=p.slice[2].lineno)

        elif p[2] in set({"<",">",">=","<=","!=","=="}):
            new_label = curr_scope.new_label()
            new_label1 = curr_scope.new_label()
            if ((p[1].type.name == "int" and p[3].type.name == "int")
                    or (p[1].type.name == "float" and p[3].type.name == "float")) :
                new_place = curr_scope.new_temp(type=dType(name=p[1].type.name))
                p[0].code.append(CBR(arg1=p[1].value,op=p[1].type.name+str(p[2]),arg2=p[3].value,dst=new_label))
                p[0].code.append(ASN(dst=new_place,op=p[1].type.name+"=",arg1=0))
                p[0].code.append(CMD(op="goto",arg1=new_label1))
                p[0].code.append(LBL(arg1=new_label))
                p[0].code.append(ASN(dst=new_place,op=p[1].type.name+"=",arg1=1))
                p[0].code.append(LBL(arg1=new_label1))
                p[0].type = p[1].type
                # print("BOP:int only",p[0].code[0])
            elif p[1].type.name == "int" and p[3].type.name == "float" :
                new_place = curr_scope.new_temp(type=dType(name="float"))
                new_place1 = curr_scope.new_temp(type=dType(name="float"))
                p[0].code.append(UOP(dst=new_place1,op="iTf",arg1=p[1].value))
                p[0].code.append(CBR(arg1=p[1].value,op=p[3].type.name+str(p[2]),arg2=p[3].value,dst=new_label))
                p[0].code.append(ASN(dst=new_place,op=p[3].type.name+"=",arg1=0))
                p[0].code.append(CMD(op="goto",arg1=new_label1))
                p[0].code.append(LBL(arg1=new_label))
                p[0].code.append(ASN(dst=new_place,op=p[3].type.name+"=",arg1=1))
                p[0].code.append(LBL(arg1=new_label1))
                p[0].type = p[3].type
            elif p[1].type.name == "float" and p[3].type.name == "int" :
                new_place = curr_scope.new_temp(type=dType(name="float"))
                new_place1 = curr_scope.new_temp(type=dType(name="float"))
                p[0].code.append(UOP(dst=new_place1,op="iTf",arg1=p[3].value))
                p[0].code.append(CBR(arg1=p[1].value,op=p[1].type.name+str(p[2]),arg2=p[3].value,dst=new_label))
                p[0].code.append(ASN(dst=new_place,op=p[1].type.name+"=",arg1=0))
                p[0].code.append(CMD(op="goto",arg1=new_label1))
                p[0].code.append(LBL(arg1=new_label))
                p[0].code.append(ASN(dst=new_place,op=p[1].type.name+"=",arg1=1))
                p[0].code.append(LBL(arg1=new_label1))
                p[0].type = p[1].type
            else :
                raise_typerror("arg1_type = "+p[1].type.name+", arg2_type = "+p[3].type.name, "in expression : "
                    + p[2] + " operator takes int or float operands only",line=p.slice[2].lineno)
        else :
            raise_general_error(p[2]+": operator not supported",line=p.slice[2].lineno)
        p[0].value = new_place



def p_uexpr(p):
    '''UExpr : PExpr
             | UnaryOp UExpr'''
    global curr_scope
    p[0] = container()
    if len(p)==2:
        p[0] = p[1]
    else:
        if p[1] == "+" :
            p[0] = p[2]
        elif p[1] == "!" :
            p[0] = p[2]
            if p[2].type.name == "int" :
                new_place = curr_scope.new_temp(type=dType(name="int"))
                p[0].code.append(UOP(dst=new_place,
                    op=p[1],arg1=p[2].value))
                p[0].type = dType(name="int")
                p[0].value = new_place
            else :
                raise_typerror("arg_type = "+p[2].type.name, "in unary expression : "
                    + p[1] + " operator takes int or float operands only",line=p.stack[-1].lineno)
        elif p[1] == "-" :
            p[0] = p[2]
            if (p[2].type.name == "int") or (p[2].type.name == "float") :
                new_place = curr_scope.new_temp(type=dType(name=p[2].type.name))
                p[0].code.append(UOP(dst=new_place,
                    op=p[1],arg1=p[2].value))
                p[0].type = dType(name=p[2].type.name)
                p[0].value = new_place
            else :
                raise_typerror("arg_type = "+p[2].type.name, "in unary expression : "
                    + p[1] + " operator takes int or float operands only",line=p.stack[-1].lineno)
        elif p[1] == "*" :
            # dereferencing the pointer
            if p[2].type.name != "pointer" :
                raise_typerror("arg_type = "+p[2].type.name, "in unary expression : "
                    + p[1] + " operator takes pointer type operands only",line=p.stack[-1].lineno)

            new_place = curr_scope.new_temp(type=p[2].type.base)
            p[0].code += p[2].code
            p[0].code.append(UOP(dst=new_place,op=p[1],arg1=p[2].value))
            p[0].extra["left_place"] = p[2].value

            p[0].type = p[2].type.base
            p[0].extra["dereference"] = True
            p[0].value = new_place
        else : # address of -> &
            p[0] = p[2]
            new_place = curr_scope.new_temp(type=dType(name="pointer",base=p[2].type))
            p[0].code.append(UOP(dst=new_place,
                op=p[1],arg1=p[2].value))
            p[0].value = new_place
            p[0].type = dType(name="pointer",base=p[2].type)

def p_unary_op(p):
    '''UnaryOp : ADD
               | SUB
               | NOT
               | MUL
               | AND'''
    p[0] = p[1]

def p_empty(p):
    '''empty : '''
    p[0] = container()
    p[0].type = dType()

def p_start_scope(p):
    '''StartScope : empty'''
    global curr_scope
    curr_scope = curr_scope.makeChildren()

def p_end_scope(p):
    '''EndScope : empty'''
    global curr_scope
    to_return = curr_scope
    offset_used_by_child = curr_scope.temp_offset
    curr_scope = curr_scope.parent
    curr_scope.temp_offset += offset_used_by_child
    p[0] = to_return

def p_error(p):
    print("\033[91m Syntax Error \033[0m : line",p.lineno,"position",p.lexpos)
    print("\033[92m token (type,value) \033[0m :",(p.type,p.value))
    exit(-1)

parser = yacc.yacc()

if __name__ == "__main__" :
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-i","--input", help="Input go file like file.go")
    argparser.add_argument("-d","--debug",help="Prints debug info like symbol table",
        action="store_true")
    args = argparser.parse_args()
    # print(args)
    input_file = args.input if args.input is not None else "test.go"

    debug = False
    if args.debug :
        debug = True
    with open(input_file, "r") as f:
        data = f.read()
    symbol_table,func_tac = parser.parse(data)
    print_scopeTree(symbol_table,func_tac,flag=debug)
    print("-"*15 + "START 3AC" + "-"*15)
    print(print_threeAC(func_tac))
    print("-"*16 + "END 3AC" + "-"*16)
