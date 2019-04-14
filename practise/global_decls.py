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
global uniq_id
uniq_id = 0 #every variable is assigned a unique id to simplify code generation
global uniq_id_to_real
uniq_id_to_real = {}

global offset
offset = 0

class container(object):
    def __init__(self, name=None,type=None, value=None, size=None):
        self.name = name
        self.code = list()
        self.extra = dict()
        self.type = type
        self.value = value
        self.size = size

class dType(object):
    def __init__(self,name=None,base=None,length=None,field_dict=None,size=None):
        self.name = name
        self.base = base
        self.length = length
        self.field_dict = field_dict # key - field_name, value - field_type
        self.size = size

class ScopeTree:
    def __init__(self, parent, scopeName=None, scope_type=None):
        self.children = []
        self.parent = parent
        self.symbolTable = {} #{"var": [type, value, offset]}
        self.typeTable = self.parent.typeTable if parent is not None else {}
        self.labelTable = {}
        self.temp_offset = 0 #used in calculating spcae acquired by a function (temp+variables)
        if scopeName is None:
            global scope_count
            self.identity = {"name":scope_count}
            scope_count += 1
        else:
            self.identity = {"name":scopeName}
            scope_count += 1
        self.identity["type"] = scope_type

    def insert(self,id,type,is_var=1,arg_list=None,ret_type=None):
        if id in self.symbolTable:
            if self.symbolTable[id]["type"].name != "func" :
                raise_general_error(id+": Already declared")
        self.symbolTable[id] = {"type":type,  "is_var":is_var,
            "arg_list":arg_list,"ret_type":ret_type, "name":id}
        global uniq_id
        self.symbolTable[id]["uniq_id"] = "$var"+str(uniq_id)
        global uniq_id_to_real
        uniq_id_to_real["$var"+str(uniq_id)] = [self, id]

        global offset
        self.symbolTable[id]["offset"] = offset
        offset += self.symbolTable[id]["size"]
        self.temp_offset += self.symbolTable[id]["size"]

        to_return =  "$var"+str(uniq_id)
        uniq_id += 1
        return to_return

    def sizeof(self,typ):
        if typ in self.typeTable:
            return self.typeTable[typ]["size"]
        if typ in self.symbolTable:
            return self.symbolTable[typ]["size"]
        if typ=="int" or typ=="float" or typ=="string" or typ=="pointer":
            return 4 #string is considered to be pointer
        elif type(typ)==container:
            size=0
            if typ.type=="structure":
                for field in typ.extra["field_list"]:
                    size += typ.extra["field_list"][field].size
                return size
            elif typ.type=="array":
                len = typ.extra["length"]
                return len*self.sizeof(typ.extra["base"])
            elif typ.type=="pointer":
                return 4 #assuming we have 32 bit architecture


    def find_uniq_id(self, id):
        return self.lookup(id)["uniq_id"]


    def insert_type(self, new_type, Type):
        self.typeTable[new_type] = {"type":Type}
        self.typeTable[new_type]["size"] = self.sizeof(Type)

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
            return self.parent.lookup(id)

    def lookup_by_uniq_id(self,uniq_id):
        global uniq_id_to_real
        then_scope, then_id = uniq_id_to_real[uniq_id]
        return then_scope.symbolTable[then_id]

    def new_temp(self, type=None,size=None):
        global temp_count
        temp_count += 1
        temp_id = "$T"+str(temp_count)
        if size is None:
            size=self.sizeof(type)
        self.insert(temp_id,type=type,size=size)
        return temp_id

    def new_label(self):
        global label_count
        label_count += 1
        return "#L"+str(label_count)

    def insert_label(self, id=None, value=None):
        if id in self.labelTable:
            return
        self.labelTable[id]=value

    def find_label(self, id=None):
        print(self.identity,self.labelTable)
        if id in self.labelTable:
            return self.labelTable[id]
        else:
            return self.parent.find_label(id)

    def reset_offset(self):
        global offset
        offset = 0

class Tac(object):
    def __init__(self, op=None, arg1=None, arg2=None, dst=None):
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.dst = dst

class LBL(Tac):
    '''Label Operation -> arg1 :'''
    def __init__(self, arg1):
        super().__init__(arg1=arg1)

    def __str__(self):
        return " ".join([str(self.arg1),":"])

class BOP(Tac):
    '''Binary Operation -> dst = arg1 op arg2'''
    def __init__(self, op, arg1, arg2, dst):
        super().__init__(op=op,arg1=arg1,arg2=arg2,dst=dst)
    def __str__(self):
        return " ".join([self.dst,"=",str(self.arg1),self.op,str(self.arg2)])

class UOP(Tac):
    '''Unary Operation -> dst = op arg1'''
    def __init__(self,dst,op,arg1):
        super().__init__(dst=dst,op=op,arg1=arg1)
    def __str__(self):
        return " ".join([self.dst,"=",self.op,str(self.arg1)])

class ASN(Tac):
    '''Assignment Operation -> dst = arg1'''
    def __init__(self,arg1,dst):
        super().__init__(arg1=arg1,dst=dst)
    def __str__(self):
        return " ".join([self.dst,"=",str(self.arg1)])

class PVA(Tac):
    '''Pointer Value Assignment -> * dst = arg1'''
    def __init__(self,arg1,dst):
        super().__init__(arg1=arg1,dst=dst)
    def __str__(self):
        return " ".join(["*",self.dst,"=",str(self.arg1)])

class CBR(Tac):
    '''Conditional Branch -> if arg1 op arg2 goto dst'''
    def __init__(self, op, arg1, arg2, dst):
        super().__init__(op=op,arg1=arg1,arg2=arg2,dst=dst)
    def __str__(self):
        return " ".join(["if",str(self.arg1),self.op,str(self.arg2),"goto",self.dst])

class OP(Tac):
    '''Operation -> op'''
    def __init__(self,op):
        super().__init__(op=op)
    def __str__(self):
        return self.op

class CMD(Tac):
    '''Command -> op arg1'''
    def __init__(self,op,arg1):
        super().__init__(op=op,arg1=arg1)
    def __str__(self):
        return " ".join([self.op,str(self.arg1)])

def raise_typerror(p, s=""):
    print("Type error: ", p)
    print(s)
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
        print(temp.identity["name"])
        for i in temp.children:
            print("child:", i.identity["name"])
        print("symbolTable:")
        for var, val in temp.symbolTable.items():
            print(var, val)
        print("TypeTable:")
        for new_type, Type in temp.typeTable.items():
            print(new_type, Type)

        for i in temp.children:
            print_scopeTree(i,source_root, flag=flag)
    three_ac = ""
    for line in source_root.code :
        three_ac = three_ac + str(line) + "\n"
    return three_ac[:-1]
