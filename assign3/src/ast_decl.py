class IfStmt(object):
    """IfStmt : IF Expr Block ElseOpt """

    def __init__(self, arg):
        self.condition = None
        self.block = None
        self.else_opt = None


global expr


class Expression(object):
    '''Expression : UnaryExpr | BinaryExpr'''

    def __init__(self):
        super(Expression, self)
        self._fields = []


global ast_imports
ast_imports = []

# global ast_expr = {  }
