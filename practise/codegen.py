#!/usr/bin/python3

import codegen_decls as assembly
import new_parser
import pprint,sys

debug = True
input_file = "test.go"
with open(input_file,"r") as f:
    data = f.read()
symbol_table,three_ac = new_parser.parser.parse(data)

asm = assembly.asm(symbol_table,three_ac)
for func in three_ac :
    asm.function_call(func)
    for codeline in three_ac[func] :
        arg1 = codeline.arg1
        arg2 = codeline.arg2
        dst = codeline.dst
        op = codeline.op
        codetype = codeline.type

        if codetype=="cmd" :
            if op=="BeginFunc" :
                asm.addInstr(['addi','$sp','$sp','-8'])
                asm.addInstr(['sw','$ra','4($sp)'])
                asm.addInstr(['sw','$fp','0($sp)'])
                asm.addInstr(['move','$fp','$sp',''])

                func_size = int(arg1)
                asm.addInstr(['addi','$sp','$sp','-'+str(func_size)])
            elif op=="goto":
                asm.addInstr(["j",arg1,"",""])
            elif op=="return":
                r1 = asm.getReg(arg1,0)
                asm.addInstr(["move", "$v0", r1, ""])
                asm.addInstr(["jr", "$ra", "",""])
            elif op=="pcall":
                if arg1=="print_int" :
                    asm.addInstr(["li", "$v0","1", ""])
                    asm.addInstr(["syscall","","",""])
                elif arg1=="print_str" :
                    asm.addInstr(["li", "$v0","4", ""])
                    asm.addInstr(["syscall","","",""])
                else :
                    asm.addInstr(["jal",arg1,"",""])
            elif op=="push_param":
                r1 = asm.getReg(arg1,0)
                dr = asm.getParamReg(arg1)
                asm.addInstr(["move",dr,r1,""])
            elif op=="pop_param":
                pass
            elif op=="assign_addr":
                pass

        elif codetype=="op":
            if op=="return":
                pass
            elif op=="EndFunc":
                asm.addInstr(['sw','$ra','-'+str(ra_offest)+'($fp)'])
                asm.addInstr(['la','$fp',str(main_size)+'($sp)',''])
                asm.addInstr(['sub','$sp','$sp',str(main_size)])
        elif codetype=="label" :
            asm.addInstr([str(arg1)+':','','',''])

        elif codetype=="asn" :
            if op=="=":
                r1 = asm.getReg(arg1,0)
                asm.storeReg(dst,0)
            elif op=="i=":
                asm.addInstr(['ori',"$s0","$0",str(arg1)])
                asm.storeReg(dst,0)
            elif op=="f=":
                pass
                # asm.addInstr(['addi',"$s0","$zero",arg1])
                # asm.storeReg(dst,0)
                # TODO baad me karte hain
            elif op=="s=":
                asm.addToString(dst,arg1)

        elif codetype=="uop" :
            if op=="call" :
                dr=asm.getReg(dst,0)
                if arg1=="read_int" :
                    asm.addInstr(["li", "$v0","5", ""])
                    asm.addInstr(["syscall","","",""])
                else :
                    asm.addInstr(["jal",arg1,"",""])
                asm.addInstr(["move",dr,"$v0",""])
                asm.storeReg(dst,0)
            else :
                r1=asm.getReg(arg1,0)
                dr=asm.getReg(dst,1)
                if op=="iTf" : # int-to-float
                    pass
                elif op=="&":
                    pass
                elif op=="!":
                    pass
                elif op=="-":
                    pass
                elif op=="*":
                    asm.addInstr(['lw',dr,r1,''])
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
                asm.addInstr(['slt',dr,r1,r2,''])
            elif op=="int>":
                pass
            elif op=="int>=":
                pass
            elif op=="int<=":
                pass
            elif op=="int!=":
                pass
            elif op=="int==":
                pass
            elif op=="|" :
                asm.addInstr(['or',dr,r2,r1])
            elif op=="&" :
                asm.addInstr(['and',dr,r2,r1])
            else :
                pass
            asm.storeReg(dst,2)


        elif codetype=="cbr" :
            if op=="==":
                r1 = asm.getReg(arg1,0) #we are using arg2=0 everywhere
                asm.addInstr(["beq", r1, "$0", dst])

        elif codetype=="pva" :
            r1=asm.getReg(arg1,0)
            dr=asm.getReg(dst,1)
            asm.addInstr(['sw',r1,'0('+dr+')',''])


print("\n\n")
asm.printAssembly();
# print("\n")
# for func in asm.assembly_code:
#     print('\033[95m'+func+'\033[0m'+" :")
#     code = asm.assembly_code[func]
#     for instr in code:
#         temp = " ".join(instr)
#         print(",".join(temp.split(" ")))
