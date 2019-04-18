all:
	rm -rf bin/
	mkdir bin
	cp src/new_parser.py bin/new_parser.py
	cp src/codegen.py bin/codegen.py
	cp src/lexer.py bin/lexer.py
	cp src/codegen_decls.py bin/codegen_decls.py
	cp src/global_decls.py bin/global_decls.py
	cp src/compile bin/compile
	chmod +x bin/new_parser.py
	chmod +x bin/codegen.py
	chmod +x bin/compile
	find . -type f -name '*.pyc' -delete; \
	find . -type f -name '*.s' -delete; \
	find . -type f -name '*.out' -delete; \
	find . -type f -name '*.tac' -delete; \
	find . -type f -name 'parsetab.py' -delete; \
	find . -type f -name 'parser.out' -delete; \

clean:
	find . -type f -name '*.pyc' -delete; \
	find . -type f -name '*.out' -delete; \
	find . -type f -name '*.s' -delete; \
	find . -type f -name '*.tac' -delete; \
	find . -type f -name 'parsetab.py' -delete; \
	find . -type f -name 'parser.out' -delete; \
	rm -rf __pycache__
	rm -rf bin/
