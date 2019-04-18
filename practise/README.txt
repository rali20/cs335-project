--------------------------------------------------------
                         README
--------------------------------------------------------
This is a compiler for translating golang to mips32
using python3 as intermediate language.

Features implemented here are :
1. Native Data Types (int,string)
2. Variables and Expressions
3. Control Structures
		- Conditionals (if,if_then_else)
		- Loops (for,while)
4. Input/Output Statements
		- print_int(), read_int(), print_str()
5. Arrays (any dimension)
6. Functions
		- Recursive also
7. User Defined Types
		- struct, typedef
8. Pointers (multi-level)

Note :
1. The syntax used here is a subset and modified
of actual golang language.
2. Semicolon required after statements but NOT after '}'
3. No use of package name, import statements
4. To use recursion function need to be declared first
5. To use I/O statements need to include declarations
for those fuctions (see examples in tests/)
6. Floats not implemented in mips assembly

Requirements :
	python3 (ply,pprint)
	spim

To compile and run
	$ make
	$ ./bin/compile <file.go>

For debugging purpose compile using
	$ ./bin/codegen.py -h # Shows usage
 	$ ./bin/codegen.py -i <file.go> -d # Basic usage

	$ ./bin/new_parser.py -h # Shows usage
	$ ./bin/new_parser.py -i <file.go> -d # Prints 3AC

CONTRIBUTORS
	NAME              ROLLNO      CONTRIBUTION
	Rahul B S         160540          45%
	Amit Yadav        160099          40%
	Prasant Kardam    160499          15%

This is a course project for COMPILER DESIGN (CS335)
at Indian Institute of Technology, Kanpur
Instructor : Prof. Amey Karkare
Academic Year : 2018-19 (Spring)
--------------------------------------------------------
