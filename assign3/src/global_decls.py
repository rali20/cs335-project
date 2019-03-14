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

# possible scopes: package, global, functions, ....
global curr_scope
curr_scope = None
class ScopeTree:
    def __init__(self, parent, scopeName=None):
        self.children = []
        self.parent = parent
        self.symbolTable = {} #{"var": [type, size, value, offset]}
        self.identity = {"name":scopeName}
    def insert(self, id, type):
        self.symbolTable[id] = [type]
    def makeChildren(self, childName=None):
        child = ScopeTree(self, childName)
        self.children.append(child)
        return child
    def lookup(self, id):
        if id in self.symbolTable:
            return self.symbolTable[id]
        else:
            return self.parent.lookup(id)


class container:
    def __init__(self, Type=None, Value=None):
        self.type = None
        self.value = None

class Tac(object):
    def __init__(self, type=None, op=None, arg1=None, arg2=None, dst=None):
        self.type = type
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.dst = dst
