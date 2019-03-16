# possible scopes: package, global, functions, ....
global curr_scope
curr_scope = None
global scope_count
scope_count = 0

global temp_count
temp_count = 0
global label_count
label_count = 0

class ScopeTree:
    def __init__(self, parent, scopeName=None):
        self.children = []
        self.parent = parent
        self.symbolTable = {} #{"var": [type, size, value, offset]}
        self.typeTable = self.parent.typeTable if parent is not None else {}
        if scopeName is None:
            global scope_count
            self.identity = {"name":scope_count}
            scope_count += 1
        else:
            self.identity = {"name":scopeName}
            scope_count += 1

    def insert(self, id, type, is_var=1, arg_list=None, size=None, ret_type=None, length=None, base=None):
        self.symbolTable[id] = {"type":type, "base":base, "is_var":is_var,"size":size, "arg_list":arg_list, "ret_type":ret_type, "length":length}

    def insert_type(self, new_type, Ntype):
        self.typeTable[new_type] = Ntype

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

    def new_temp():
        temp_count += 1
        return "$"+str(temp_count)

    def new_label():
        label_count += 1
        return "#"+str(label_count)
# class container:
#     def __init__(self, type=None, value=None):
#         self.type = value
#         self.value = type

class Builtin(object):
    def __init__(self,name,width=None):
        self.name = name
        self.width = width
        self.base = None
    def __len__(self):
        return self.width
    def __repr__(self):
        return self.name

class Int(Builtin):
    def __init__(self):
        super().__init__("int",4)

class Float(Builtin):
    def __init__(self):
        super().__init__("float",8)

class String(Builtin):
    def __init__(self):
        super().__init__("string")

class Byte(Builtin):
    def __init__(self):
        super().__init__("byte",1)

class Void(Builtin):
     def __init__(self):
        super().__init__("void")

class Error(Builtin):
     def __init__(self):
        super().__init__("error")

typeOp = set({"arr","struct","ptr","func","interface","slice","map"})
class Derived(object):
    def __init__(self,op,base,arg=None):
        self.arg = dict(arg)
        if op in typeOp:
            self.op = op
        if isinstance(base,(Derived,Builtin)) and (not isinstance(base,(Error,Void))) :
            self.base = base
            if op == "arr" :
                self.name = "arr" + base.name
            elif op == "struct" :
                self.name = "struct" + arg["name"]
# i am saying use attributes for array - base, just like for func type
# curr_scope.symbolTable["any_array_ident"] = {"type":"array"}? Is that what you wanna say?
class Tac(object):
    def __init__(self, type=None, op=None, arg1=None, arg2=None, dst=None):
        self.type = type
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.dst = dst

class LBL(Tac):
    '''Label Operation -> label:'''
    pass

class BOP(Tac):
    '''Binary Operation -> dst = arg1 op arg2'''
    def __init__(self, type, op, arg1, arg2, dst):
        super().__init__(type,op,arg1,arg2,dst)

class UOP(Tac):
    '''Unary Operation -> dst = op arg1'''
    def __init__(self,type,op,arg1):
        super.__init__(type,op,arg1)

class ASN(Tac):
    '''Assignment Operation -> dst = arg1'''
    def __init__(self,type,arg1,dst):
        super.__init__(type,arg1=arg1,dst=dst)

class JMP(Tac):
    '''Jump Operation -> goto dst'''
    def __init__(self,type,dst):
        super.__init__(type,dst=dst)

class JIF(Tac):
    '''Jump If -> if arg1 goto dst'''
    def __init__(self,type,arg1,dst):
        super.__init__(type,arg1=arg1,dst=dst)

class CBR(Tac):
    '''Conditional Branch -> if arg1 op arg2 goto dst'''
    def __init__(self, type, op, arg1, arg2, dst):
        super().__init__(type,op,arg1,arg2,dst)

# class BOP(Tac):
#     '''Binary Operation
#         dst = arg1 op arg2
#         op can be :
#             +  : Add
#             -  : Subtract
#             *  : Multiply
#             &  : Bitwise AND
#             |  : Bitwise OR
#             ^  : Bitwise XOR
#             && : Logical AND
#             || : Logical OR
#     '''
#     def __init__(self, type, op, arg1, arg2, dst):
#         super().__init__(type,op,arg1,arg2,dst)
#
# class LOP(Tac):
#     '''Logical Operation
#         dst = arg1 op arg2
#         op can be :
#             <  : Less Than
#             >  : Greater Than
#             <= : Less Than Equal
#             >= : Greater Than Equal
#             == : Equals
#             != : Not Equals
#     '''
#     def __init__(self, type, op, arg1, arg2, dst):
#         super().__init__(type,op,arg1,arg2,dst)
#
# class SOP(Tac):
#     '''Shift Operation
#         dst = arg1 op arg2
#         op can be :
#             << : Bitwise Shift Left
#             >> : Bitwise Shift Right
#     '''
#     def __init__(self, type, op, arg1, arg2, dst):
#         super().__init__(type,op,arg1,arg2,dst)
#
# class DOP(Tac):
#     '''Division Operation
#         dst = arg1 op arg2
#         op can be :
#             / : Divide
#             % : Remainder
#     '''
#     def __init__(self, type, op, arg1, arg2, dst):
#         super().__init__(type,op,arg1,arg2,dst)


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


def extract_package(package_name):
    return package_name.split("/")[-1]


def print_scopeTree(node):
    temp = node
    print("")
    print("me:", temp.identity)
    for i in temp.children:
        print("child:", i.identity)
    print("symbolTable:")
    for var, val in temp.symbolTable.items():
        print(var, val)
    print("TypeTable:")
    for new_type, Ntype in temp.typeTable.items():
        print(new_type, Ntype)

    for i in temp.children:
        print_scopeTree(i)
