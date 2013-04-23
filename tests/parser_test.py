#! /usr/bin/python
'''
Date: 22nd April, 2013
Purpose: To test the parsing of parser.py.
Usage: python parser_test.py <number_of_stmts>
'''

import os, random, string, subprocess, sys


PWD = os.getcwd()
TOKENS = {
	'DECLARED': {},
	'NAME': ["int", "float", "str", "Graph", "Node", "Edge"],
	'UNDECLARED': list(string.lowercase),
}


def generate_declaration():
	var = random.choice(TOKENS["UNDECLARED"])
	TOKENS["UNDECLARED"].remove(var)
	name = random.choice(TOKENS["NAME"])
	TOKENS["DECLARED"][var] = name
	return "%s %s\n" %(name, var)


def generate_definition():
	pass


def generate_gr(count):
	prog_file = os.path.join(PWD, "tmp_%d_%d.gr" % (count, random.randint(32768, 65536)))
	expected_file = os.path.join(PWD, prog_file.replace(".gr", ".exp"))
	parser_file = os.path.join(PWD, prog_file.replace(".gr", ".yacc"))
	prog_buffer = open(prog_file, "w")
	tabs = 0

	prog_buffer.write("def void main():\n")
	tabs += 1

	for i in xrange(count):
		prog_buffer.write("\t" * tabs)
		prog_buffer.write(generate_declaration())

	prog_buffer.flush()
	prog_buffer.close()
	return prog_file, expected_file, parser_file


if len(sys.argv) == 1:
	print "Usage: python", sys.argv[0], "<number_of_stmts>"
	sys.exit(-1)

if PWD.endswith("glang"):
	parser = os.path.join(PWD, "frontend/parser.py")
elif PWD.endswith("tests"):
	parser = os.path.join(PWD, "../frontend/parser.py")
else:
	print "Run from glang or glang/tests directory."
	sys.exit(-1)

prog_file, expected_file, parser_file = generate_gr(int(sys.argv[1]))
subprocess.call(["python", parser, prog_file, parser_file])
