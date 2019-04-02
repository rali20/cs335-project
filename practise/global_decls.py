## Coding Conventions
# 'p' variables in p_<fun> are container() type
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
                return None
                # raise_general_error("undeclared variable: " + id)
            return self.parent.lookup(id)

    def new_temp(self):
        global temp_count
        temp_count += 1
        return "$"+str(temp_count)

    def new_label(self):
        global label_count
        label_count += 1
        return "#"+str(label_count)

class container(object):
    def __init__(self,type=None,value=None):
        self.code = list()
        self.place = None
        self.extra = dict()
        self.type = type
        self.value = value

class Tac(object):
    def __init__(self, op=None, arg1=None, arg2=None, dst=None, type=None):
        self.type = type
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.dst = dst

class LBL(Tac):
    '''Label Operation -> label :'''
    def __init__(self, arg1, type="LBL"):
        super().__init__(type,arg1=arg1)

    def __str__(self):
        return " ".join([str(self.arg1),":"])

class BOP(Tac):
    '''Binary Operation -> dst = arg1 op arg2'''
    def __init__(self, op, arg1, arg2, dst, type="BOP"):
        super().__init__(op=op,arg1=arg1,arg2=arg2,dst=dst,type=type)
    def __str__(self):
        return " ".join([self.dst,"=",str(self.arg1),self.op,str(self.arg2)])

class UOP(Tac):
    '''Unary Operation -> dst = op arg1'''
    def __init__(self,op,arg1,type="UOP"):
        super().__init__(op=op,arg1=arg1,type=type)
    def __str__(self):
        return " ".join([self.dst,"=",self.op,str(self.arg1)])

class ASN(Tac):
    '''Assignment Operation -> dst = arg1'''
    def __init__(self,arg1,dst,type="ASN"):
        super().__init__(arg1=arg1,dst=dst,type=type)
    def __str__(self):
        return " ".join([self.dst,"=",str(self.arg1)])

class JMP(Tac):
    '''Jump Operation -> goto dst'''
    def __init__(self,dst,type="JMP"):
        super().__init__(dst=dst,type=type)
    def __str__(self):
        return " ".join(["goto",self.dst])

class CBR(Tac):
    '''Conditional Branch -> if arg1 op arg2 goto dst'''
    def __init__(self, op, arg1, arg2, dst, type="CBR"):
        super().__init__(op=op,arg1=arg1,arg2=arg2,dst=dst,type=type)
    def __str__(self):
        return " ".join(["if",str(self.arg1),self.op,str(self.arg2),"goto",self.dst])


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


def print_scopeTree(node,source_root,flag=False):
    temp = node
    if flag :
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
            print_scopeTree(i,source_root)
    three_ac = ""
    for line in source_root.code :
        three_ac = three_ac + str(line) + "\n"
    return three_ac[:-1]
