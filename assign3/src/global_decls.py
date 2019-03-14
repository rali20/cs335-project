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
global scope_count
scope_count = 0

class ScopeTree:
    def __init__(self, parent, scopeName=None):
        self.children = []
        self.parent = parent
        self.symbolTable = {} #{"var": [type, size, value, offset]}
        self.typeTable = {}
        if scopeName is None:
            global scope_count
            self.identity = {"name":scope_count}
            scope_count += 1
        else:
            self.identity = {"name":scopeName}
            scope_count += 1

    def insert(self, id, type, is_var=1):
        self.symbolTable[id] = {"type":type, "is_var":is_var}

    def insert_type(self, new_type, Ntype):
        self.typeTable["new_type"] = Ntype

    def makeChildren(self, childName=None):
        child = ScopeTree(self, childName)
        self.children.append(child)
        return child

    def lookup(self, id):
        if id in self.symbolTable:
            return self.symbolTable[id]
        else:
            if self.parent is None:
                raise_general_error("undeclared variable: " + id)
            return self.parent.lookup(id)


class container:
    def __init__(self, type=None, value=None):
        self.type = type
        self.value = value

def raise_typerror(p, s=""):
    print("Type error", s)
    print(p)
    exit(-1)

def raise_out_of_bounds_error(p, s="" ):
    print("out of bounds error")
    print(p)
    print(s)
    exit(-1)

def raise_general_error(s):
    print(s)
    exit(-1)
