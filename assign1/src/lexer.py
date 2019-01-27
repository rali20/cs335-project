#!/usr/bin/python3

import sys
import ply.lex as lex
from tokenizer import *


# Tkns = dict({})
# for t in tokens:
#   Tkns[t] = [t,0]

# Reading from source file
print("usage : %s <cfg-file> <go-source-file> <output-html-name>" % sys.argv[0])

if len(sys.argv)==4 :
  cfg_file = sys.argv[1]
  source_file = sys.argv[2]
  html_file = sys.argv[3]
else :
  print("Error in command line args")
  exit(-1)

try :
  lexer = lex.lex()
  with open(source_file) as sfp:
    data = sfp.read()+"\n"
    lexer.input(data)
     
#    for tkn in lexer:
#      Tkns[tkn.type][1] += 1
#      if tkn.value in Tkns[tkn.type]:
#        continue
#      Tkns[tkn.type].append(tkn.value)

    with open(cfg_file) as cfp:
      token_colors = { line.split(",")[0]:line.split(",")[1] for line in cfp.read().split("\n") }
    
    with open(html_file,"w") as hfp:
      html_str = '''<!DOCTYPE html><html><head><title>Token Highlighting</title></head><body>'''
      for tkn in lexer:
        html_str += '<span style="color:%s;"'% token_colors[tkn.type] + tkn.value + "</span>"
      html_str += '''</body></html>'''
      hfp.write(html_str)  

    # print(data)
    # print("-"*40)
    # print("TOKEN VALUE","|","TOKEN TYPE")
    # print("-"*40)
    # for tkn in lexer:
    #   print(tkn.value,tkn.type)  

except IOError as e:
  print("ERROR IN LEXER",e)
  exit(-1)    
