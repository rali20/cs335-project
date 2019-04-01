import ply.yacc as yacc

from lexer import *

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

def p_source_file(p):
	'''SourceFile : DeclList'''

def p_top_level_decl(p):
	'''TopLevelDecl : CommonDecl
					| FuncDecl''' 

def p_common_decl(p):
    '''CommonDecl : CONST ConstDecl
                  | VAR VarDecl
                  | TYPE TypeDecl'''

def p_const_decl(p):
    '''ConstDecl : DeclNameList Type AGN ExprList'''

def p_var_decl(p):
    '''VarDecl : DeclNameList Type
               | DeclNameList Type AGN ExprList
'''

def p_type_decl(p):
    '''TypeDecl : TypeDeclName Type'''

def p_type_decl_name(p):
    '''TypeDeclName : IDENT'''

def p_simple_stmt(p):
    '''SimpleStmt : Expr
                  | ExprList AGN ExprList
                  | ExprList DEFN ExprList'''

def p_compound_stmt(p):
    '''StmtBlock : LCURL StartScope StmtList EndScope RCURL'''

def p_loop_body(p):
    '''LoopBody : LCURL StartScope StmtList EndScope RCURL'''

def p_for_header(p):
    '''ForHeader : OSimpleStmt SEMCLN OSimpleStmt SEMCLN OSimpleStmt
                 | OSimpleStmt'''

def p_for_body(p):
    '''ForBody : ForHeader LoopBody'''

def p_for_stmt(p):
    '''ForStmt : FOR StartScope ForBody EndScope'''

def p_if_stmt(p):
    '''IfStmt : IF StartScope Expr LoopBody ElseIfList ElseStmt EndScope'''

def p_else_if(p):
    '''ElseIf : ELSE IF Expr LoopBody'''

def p_else_if_list(p):
    '''ElseIfList : empty
                  | ElseIfList ElseIf'''

def p_else(p):
    '''ElseStmt : empty
                | ELSE StmtBlock'''

def p_type(p):
    '''Type : Name
			| StructType
			| ArrayType
            | PtrType
			| LPRN Type RPRN'''

def p_name(p):
	'''Name : IDENT'''

def p_array_type(p):
	'''ArrayType : LSQR Expr RSQR Type'''

def p_struct_type(p):
    '''StructType : STRUCT LCURL StructDeclList OSemi RCURL'''

def p_func_decl(p):
    '''FuncDecl : FUNC IDENT StartScope ArgList FuncRes FuncBody EndScope'''

def p_func_body(p):
    '''FuncBody : empty
                | LCURL StmtList RCURL'''

def p_arg_list(p):
    '''ArgList : LPRN OArgTypeListOComma RPRN'''

def p_func_res(p):
    '''FuncRes : empty
               | FuncRetType
               | LPRN_OR OArgTypeListOComma RPRN_OR'''

def p_struct_decl_list(p):
    '''StructDeclList : StructDecl
    				  | StructDeclList SEMCLN StructDecl'''

def p_struct_decl(p):
    '''StructDecl : FieldList Type'''

def p_label_name(p):
    '''LabelName : NewName'''

def p_new_name(p):
    '''NewName : IDENT'''

def p_ptr_type(p):
    '''PtrType : MUL Type'''

def p_func_ret_type(p):
    '''FuncRetType : ArrayType
				   | StructType
                   | PtrType
				   | Name'''

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

def p_oexpr_list(p):
    '''OExprList : empty
                 | ExprList'''

def p_expr_list(p):
    '''ExprList : Expr
    			| ExprList COMMA Expr'''

def p_literal(p):
    '''BasicLit : INTEGER_LIT
                | FLOAT_LIT
                | STRING_LIT'''

def p_decl_list(p):
    '''DeclList : empty
    			| DeclList TopLevelDecl SEMCLN'''

def p_decl_name_list(p):
    '''DeclNameList : DeclName
    				| DeclNameList COMMA DeclName'''

def p_stmt_list(p):
    '''StmtList : Stmt
                | StmtList SEMCLN Stmt'''

def p_field_list(p):
    '''FieldList : FieldName
            	 | FieldList COMMA FieldName'''

def p_field_name(p):
	'''FieldName : IDENT'''

def p_decl_name(p):
    '''DeclName : IDENT'''

def p_arg_type(p):
    '''ArgType : Type
        	   | IDENT Type'''

def p_arg_type_list(p):
    '''ArgTypeList : ArgType
                   | ArgTypeList COMMA ArgType'''

def p_oarg_type_list_ocomma(p):
    '''OArgTypeListOComma : empty
    					  | ArgTypeList OComma'''

def p_stmt(p):
    '''Stmt : empty
            | StmtBlock
            | CommonDecl
            | NonDeclStmt'''

def p_non_decl_stmt(p):
    '''NonDeclStmt : SimpleStmt
                   | ForStmt
                   | IfStmt
                   | BREAK ONewName
                   | CONTINUE ONewName
                   | GOTO NewName
                   | RETURN OExprList
                   | LabelName COLON Stmt'''

def p_pexpr(p):
	'''PExpr : Name
			 | BasicLit
			 | CompositeLit
			 | PExpr DOT IDENT
			 | PExpr LSQR Expr RSQR
			 | PseudoCall
			 | LPRN Expr RPRN'''

def p_other_type(p):
	'''OtherType : ArrayType
				 | PtrType
				 | StructType'''

def p_composite_lit(p):
	'''CompositeLit : OtherType LitVal'''

def p_lit_val(p):
	'''LitVal : LCURL RCURL
			  | LCURL ElementList OComma RCURL '''

def p_element_list(p):
	'''ElementList : KeyedElement
				   | ElementList COMMA KeyedElement'''

def p_keyed_element(p):
	'''KeyedElement : Element
					| FieldName COLON Element'''

def p_element(p):
	'''Element : Expr
			   | LitVal'''

def p_func_call(p):
	'''PseudoCall : Name LPRN RPRN
				  | Name LPRN ExprList RPRN'''

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

def p_uexpr(p):
    '''UExpr : PExpr
             | UnaryOp UExpr'''

def p_unary_op(p):
    '''UnaryOp : ADD
               | SUB
               | NOT
               | MUL
               | AND'''

def p_empty(p):
    '''empty : '''

def p_start_scope(p):
    '''StartScope : empty'''

def p_end_scope(p):
    '''EndScope : empty'''

def p_error(p):
    print(p)
    exit(-1)

parser = yacc.yacc()