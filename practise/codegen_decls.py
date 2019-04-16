import pprint
tempReg = ['$s0','$s1','$s2']
class asm:
	def __init__(self, symbolTable, threeAddressCode):
		self.assembly_code = {}
		self.ST = symbolTable
		self.currFunc = ''
		self.TAC = threeAddressCode
		self.resetReg()
		self.stack = {}		# We have to variable name, value, type
		self.new_ST = {}
		self.unfold_tree(self.ST)
		pprint.pprint(self.new_ST)

	def unfold_tree(self,root):
		temp = root
		for var, val in temp.symbolTable.items():
			# val["parent"] = temp.identity["name"]
			uniq_id = val["uniq_id"]
			self.new_ST[uniq_id] = val
			if var[0:2]=="_T":
				self.new_ST[var] = val
		for i in temp.children:
			self.unfold_tree(i)


	def resetReg(self):
		self.registors = {
		'$0' : 0,				#$0		# always contains zero
		'$at': None , 			#$1		# assembler temporary
		'$v0': None , 			#$2		# Values from expression evaluation and function results
		'$v1': None ,			#$3		# Same as above
		'$a0': None ,			#$4		# First four parameters for function call
		'$a1': None ,			#$5		# Not preserved across function calls
		'$a2': None , 			#$6		#
		'$a3': None , 			#$7		#
		'$t0': None ,			#$8		# (temporaries) Caller saved if needed.
		'$t1': None ,			#$9		# Subroutines can use w/out saving.
		'$t2': None ,			#$10	# Not preserved across procedure calls
		'$t3': None ,			#$11	#
		'$t4': None ,			#$12	#
		'$t5': None ,			#$13	#
		'$t6': None ,			#$14	#
		'$t7': None ,			#$15	#
		'$s0': None , 			#$16	# (saved values) - Callee saved.
		'$s1': None , 			#$17	# A subroutine using one of these must save original
		'$s2': None , 			#$18	# and restore it before exiting.
		'$s3': None , 			#$19	# Preserved across procedure calls.
		'$s4': None , 			#$20	#
		'$s5': None , 			#$21	#
		'$s6': None , 			#$22	#
		'$s7': None , 			#$23	#
		'$t8': None ,			#$24	# (temporaries) Caller saved if needed. Subroutines can use w/out saving.
		'$t9': None ,			#$25	# Not preserved across procedure calls.
		'$k0': None , 			#$26	# reserved for use by the interrupt/trap handler
		'$k1': None , 			#$27	#
		'$gp': None , 			#$28	# Global pointer. Points to the middle of the 64K block of memory in the static data segment.
		'$sp': None , 			#$29	# stack pointer
		'$fp': None , 			#$30	# frame pointer, preserved across procedure calls
		'$ra': None ,			#s31	# return address
		}
		# self.regUsed = []
		self.paramReg = ['$a0','$a1','$a2','$a3']
		self.regFree = set({'$t0', '$t1','$t2','$t3','$t4','$t5','$t6','$t7','$s0','$s1','$s2','$s3','$s4','$s5', '$s6'})
		self.regAssignedVar = dict() # key-register value-variable
		self.varInfo = {}
		self.tempoffset = 0

	def function_call(self,function):
		print("===========", function)
		self.currFunc = function
		self.assembly_code[function] = []

	def addInstr(self,instr):
		print(self.currFunc,instr)
		self.assembly_code[self.currFunc].append(instr)

	def flushReg(self,reg):
		self.addInstr(['sw',reg,'-'+str(self.varInfo[self.regAssignedVar[reg]]['Offset'])+'($fp)',''])
		self.varInfo[self.regAssignedVar[reg]]['Reg'] = None


	def addToString(self,var,stringToStore):
		# print stringToStore
		self.addInstr(['.data','','',''])
		self.addInstr([var+':','.asciiz',stringToStore,''])
		self.addInstr(['.text','','',''])

	def getReg(self,var,num):
		print("getReg for ",var)
		reg = "$s"+str(num)
		off = self.new_ST[var]["offset"]
		if self.new_ST[var]["type"].name=="array" or self.new_ST[var]["type"].name=="structure":
			self.addInstr(["xor", reg,reg,""])
			self.addInstr(["addi",reg,"$fp",str(-off)])
			return reg
		self.addInstr(['lw','$s0','-'+str(off)+'($fp)',''])
		return reg


	def getReg1(self,var):
		pass


	def storeReg(self,var,num):
		if self.new_ST[var]["type"].name=="array" or self.new_ST[var]["type"].name=="structure":
			return
		reg = "$s"+str(num)
		off = self.new_ST[var]["offset"]
		self.addInstr(['sw',reg,'-'+str(off)+'($fp)',''])




	def getParamReg(self,var):
		param_reg = self.paramReg.pop(0)
		off = self.new_ST[var]["offset"]
		if(param_reg):
			self.regAssignedVar[param_reg] = var
			self.addInstr(['lw',param_reg,str(-offset)+'($fp)'],"")

			self.varInfo[var]['Reg'] = param_reg
		else:
			print("No more free param regs")
		return param_reg

	def storeParam(self,func_name):
		off = 4
		for idx in range(len(self.ST.mainsymbtbl[func_name]['Parameters']) - 1) :
			self.addInstr(['lw','$s7',str(-(4+off))+'($sp)',''])
			self.addInstr(['sw','$s7',str(-(off ))+'($fp)',''])
			off += 4
		self.addInstr(['lw','$s7',str(-4)+'($sp)',''])
		self.addInstr(['sw','$s7',str(0)+'($fp)',''])

	def savePrevValues(self,z,paramcount):
		counter = paramcount + 4
		for prev in tempReg:
			self.addInstr(['sw',prev,'-'+str(counter)+"($sp)",''])
			counter +=4
		self.addInstr(['sw','$ra','-'+str(counter)+'($sp)',''])
		self.addInstr(['sw','$fp','-'+str(counter+4)+'($sp)',''])
		self.addInstr(['sw','$sp','-'+str(counter+8)+'($sp)',''])

	def printAssembly(self):
		file = open("out.s",'w')
		file.write(".data\n newline : .asciiz \"\\n\" \n.text\nmain:\n")
		for line in self.assembly_code["main"]:
			file.write("\t")
			if line[1] == '':
				file.write("\t%s\n" %line[0])
			elif line[1] == '.asciiz':
				file.write("\t%s\t\t %s %s %s\n" %(line[0],line[1],line[2],line[3]))
			elif line[2] == '':
				file.write("\t%s\t\t %s\n" %(line[0],line[1]))
			elif line[3] == '':
				file.write("\t%s\t\t %s,%s\n" %(line[0],line[1],line[2]))
			else:
				file.write("\t%s\t\t %s,%s,%s\n" %(line[0],line[1],line[2],line[3]))
		for function in self.assembly_code.keys():
			if(not ( function == "main" or function == 'Main' )):
				file.write("\n%s:\n" %function)
				for line in self.assembly_code[function]:
					file.write("\t")
					if line[1] == '':
						file.write("\t%s\n" %line[0])
					elif line[1] == '.asciiz':
						file.write("\t%s\t\t %s %s %s\n" %(line[0],line[1],line[2],line[3]))
					elif line[2] == '':
						file.write("\t%s\t\t %s\n" %(line[0],line[1]))
					elif line[3] == '':
						file.write("\t%s\t\t %s,%s\n" %(line[0],line[1],line[2]))
					else:
						file.write("\t%s\t\t %s,%s,%s\n" %(line[0],line[1],line[2],line[3]))
		file.close()
