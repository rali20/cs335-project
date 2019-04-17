#!/bin/bash
./codegen.py -i $1 -d
spim -f out.s
