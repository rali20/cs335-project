#!/usr/bin/env python3

import codegen_decls as assembly
import new_parser
import pprint,sys,argparse


argparser = argparse.ArgumentParser()
argparser.add_argument("-i","--inputfile", help="Input go file like file.go")
argparser.add_argument("-s","--sfile", help="Name of (output) mips assembly file like out.s")
argparser.add_argument("-3","--tacfile", help="Name of 3ac file like out.tac")
argparser.add_argument("-d","--debug",help="Prints debug info like symbol table",
    action="store_true")
args = argparser.parse_args()

debug = False
if args.debug:
    debug = True

sfile = "out.s"
if args.sfile :
    sfile = args.sfile

tacfile = "out.tac"
if args.tacfile :
    tacfile = args.sfile

inputfile = "test.go"
if args.inputfile :
    inputfile = args.inputfile


print_scope_tree = False
print_symbol_table = False
print_3ac = False
if debug:
    print_scope_tree = False
    print_symbol_table = True
    print_3ac = True



with open(inputfile,"r") as f:
    data = f.read()
symbol_table,three_ac = new_parser.parser.parse(data)

if print_scope_tree:
    new_parser.print_scopeTree(symbol_table,dict({}),print_scope_tree)

asm = assembly.asm(symbol_table,three_ac,debug=print_3ac)
if print_symbol_table:
    print("===========Symbol table===========")
    asm.print_new_ST()
    print("")

def print_unimp(s):
    print(s," : ***Unimplimented***")
    # exit()

if print_3ac:
    print("\n===========3AC==========\n")
for func in three_ac :
    asm.function_call(func)
    for codeline in three_ac[func] :
        if print_3ac:
            print('\033[92m'+str(codeline)+'\033[0m')
        arg1 = codeline.arg1
        arg2 = codeline.arg2
        dst = codeline.dst
        op = codeline.op
        codetype = codeline.type

        if codetype=="cmd" :
            if op=="BeginFunc" :
                asm.addInstr(['addi','$sp','$sp','-8'])
                asm.addInstr(['sw','$ra','4($sp)',''])
                asm.addInstr(['sw','$fp','0($sp)',''])
                asm.addInstr(['move','$fp','$sp',''])

                func_size = int(arg1)
                asm.addInstr(['addi','$sp','$sp','-'+str(func_size)])
                # store params
                lookup_result = asm.ST.lookup(asm.currFunc)
                num_params = len(lookup_result["arg_list"])
                for i in range(num_params):
                    lookup_result["arg_list"][i]
            elif op=="goto":
                asm.addInstr(["j",arg1,"",""])
            elif op=="return":
                r1 = asm.getReg(arg1,0)
                asm.addInstr(["move", "$v0", r1, ""])
                asm.addInstr(["move","$sp","$fp",""])
                asm.addInstr(["lw","$fp","-0($sp)",""])
                asm.addInstr(["lw","$ra","4($sp)",""])
                asm.addInstr(["addi","$sp","$sp","8"])
                asm.addInstr(["jr", "$ra", "",""])
            elif op=="pcall":
                if arg1=="print_int" :
                    asm.addInstr(["li", "$v0","1", ""])
                    asm.addInstr(["syscall","","",""])
                elif arg1=="print_str" :
                    asm.addInstr(["li", "$v0","4", ""])
                    asm.addInstr(["syscall","","",""])
                elif arg1=="print_float":
                    # asm.addInstr(["mov.s","$fp12","$a0",""])
                    # asm.addInstr(["li","$v0","2",""])
                    # asm.addInstr(["syscall","","",""])
                    print_unimp("print_float ")
                else :
                    asm.addInstr(["jal",arg1,"",""])
            elif op=="push_param":
                # r1 = asm.getReg(arg1,0)
                dr = asm.getParamReg(arg1)
                # asm.addInstr(["move",dr,r1,""])
            elif op=="pop_param":
                asm.paramReg = ['$a0','$a1','$a2','$a3']
            else :
                print_unimp(op)

        elif codetype=="op":
            if op=="return" or op=="EndFunc" :
                asm.addInstr(["move","$sp","$fp",""])
                asm.addInstr(["lw","$fp","-0($sp)",""])
                asm.addInstr(["lw","$ra","4($sp)",""])
                asm.addInstr(["addi","$sp","$sp","8"])
                asm.addInstr(["jr", "$ra", "",""])

        elif codetype=="label" :
            asm.addInstr([str(arg1)+':','','',''])

        elif codetype=="asn" :
            if op=="=":
                r1 = asm.getReg(arg1,0)
                dr=asm.getReg(dst,1)
                asm.addInstr(["move",dr,r1,""])
                asm.storeReg(dst,1)
            elif op=="int=":
                asm.addInstr(['ori',"$s0","$0",str(arg1)])
                asm.storeReg(dst,0)
            elif op=="float=":
                print_unimp(op)
            elif op=="str=":
                asm.addToString(dst,arg1)
            else:
                print_unimp(op)

        elif codetype=="uop" :
            if op=="call" :
                if arg1=="read_int" :
                    asm.addInstr(["li", "$v0","5", ""])
                    asm.addInstr(["syscall","","",""])
                else :
                    asm.addInstr(["jal",arg1,"",""])
                asm.addInstr(["move","$s0","$v0",""])
                asm.storeReg(dst,0)
            else :
                dr=asm.getReg(dst,1)
                if op=="iTf" : # int-to-float
                    print_unimp(op)
                elif op=="&":
                    off = asm.new_ST[arg1]["offset"]
                    asm.addInstr(["addi",dr,"$fp",str(-off)])
                elif op=="!":
                    print_unimp(op)
                elif op=="-":
                    r1=asm.getReg(arg1,0)
                    asm.addInstr(['sub',dr,'$0',dr]);
                elif op=="*":
                    asm.addInstr(['lw',dr,'0('+r1+')',''])
                else :
                    print_unimp(op)
                asm.storeReg(dst,1)

        elif codetype=="bop" :
            r1=asm.getReg(arg1,0)
            r2=asm.getReg(arg2,1)
            dr=asm.getReg(dst,2)
            if op=="int+":
                asm.addInstr(['add',dr,r1,r2])
            elif op=="int-":
                asm.addInstr(['sub',dr,r1,r2])
            elif op=="int*":
                asm.addInstr(['mult',r1,r2,''])
                asm.addInstr(['mflo',dr,'',''])
            elif op=="int/":
                asm.addInstr(['div',r1,r2,''])
                asm.addInstr(['mflo',dr,'',''])
            elif op=="%":
                asm.addInstr(['div',r1,r2,''])
                asm.addInstr(['mfhi',dr,'',''])
            elif op=="int<":
                asm.addInstr(['slt',dr,r1,r2])
            elif op=="|" :
                asm.addInstr(['or',dr,r2,r1])
            elif op=="&" :
                asm.addInstr(['and',dr,r2,r1])
            elif op=="<<":
                asm.addInstr(['sllv',dr,r1,r2])
            elif op==">>":
                asm.addInstr(['srlv',dr,r1,r2])
            elif op=="||":
                pass
            else :
                print_unimp(op)
            asm.storeReg(dst,2)

        elif codetype=="cbr" :
            r1=asm.getReg(arg1,0)
            r2=asm.getReg(arg2,1)
            if op=="int==":
                asm.addInstr(["beq", r1, r2, dst])
            elif op=="int>":
                asm.addInstr(["bgt", r1, r2, dst])
            elif op=="int<":
                asm.addInstr(["blt", r1, r2, dst])
            elif op=="int>=":
                asm.addInstr(["bge", r1, r2, dst])
            elif op=="int<=":
                asm.addInstr(["ble", r1, r2, dst])
            elif op=="int!=":
                asm.addInstr(["bne", r1, r2, dst])
            else :
                print_unimp(op)

        elif codetype=="pva" :
            r1=asm.getReg(arg1,0)
            dr=asm.getReg(dst,1)
            off = asm.new_ST[dst]["offset"]

            # asm.addInstr(["addi",dr,"$fp",str(-off)])
            asm.addInstr(['sw',r1,'0('+dr+')',''])

        elif codetype=="misc":
            reg = "$a"+str(arg2)
            asm.addInstr(["move", "$s0",reg,""])
            asm.storeReg(arg1,0)

        else :
            print_unimp(codeline)

        # print(" ")

asm.assembly_code["main"].append(["li","$v0","10",""])
asm.assembly_code["main"].append(["syscall","","",""])
# print("\n\n")
asm.printAssembly(sfile);
