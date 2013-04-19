#! /usr/bin/python
'''
Date: 18th April, 2013
Purpose: To test the tokenizing of lexer.py.
'''

import os, random, subprocess, sys


PWD = os.getcwd()
TOKENS = {
	'=': 'ASSIGN',
	':': 'COLON',
	',': 'COMMA',
	'.': 'DOT',
	'**': 'DOUBLESTAR',
	'==': 'EQUAL',
	'>': 'GREATER',
	'>=': 'GREATEREQUAL',
	'{': 'LBRACE',
	'[': 'LBRACKET',
	'<': 'LESS',
	'<=': 'LESSEQUAL',
	'(': 'LPAREN',
	'-': 'MINUS',
	'\n': 'NEWLINE',
	'!=': 'NOTEQUAL',
	'%': 'PERCENT',
	'+': 'PLUS',
	'}': 'RBRACE',
	']': 'RBRACKET',
	')': 'RPAREN',
	'/': 'SLASH',
	'*': 'STAR',

	'and': 'AND',
	'break': 'BREAK',
	'class': 'CLASS',
	'continue': 'CONTINUE',
	'def': 'DEF',
	'elif': 'ELIF',
	'else': 'ELSE',
	'for': 'FOR',
	# 'from': 'FROM',
	'if': 'IF',
	# 'import': 'IMPORT',
	'in': 'IN',
	'is': 'IS',
	'not': 'NOT',
	'or': 'OR',
	'print': 'PRINT',
	'return': 'RETURN',
	'while': 'WHILE',
	'None': 'ENDMARKER',

	'NAME': ["int", "float", "str", "Graph", "Node", "Edge"],
	'NUMBER': [0, 42, -17, 0.00, 3.14, -2.718],
	'STRING': ['"The Shawshank Redemption"', '"Schindler\'s List"',
				'"The Godfather: Part II"', '"Se7en"'],
}


def generate_random_tokens(count):
	prog_file = os.path.join(PWD, "tmp_%d_%d.gr" % (count, random.randint(32768, 65536)))
	lexer_file = os.path.join(PWD, prog_file.replace(".gr", ".lex"))
	output_file = os.path.join(PWD, prog_file.replace(".gr", ".out"))
	prog_buffer = open(prog_file, "w")
	lexer_buffer = open(lexer_file, "w")

	for i in xrange(0, count):
		token = random.choice(TOKENS.keys())
		value = TOKENS[token]

		if type(value) == list:
			chosen_token = str(random.choice(value))
			prog_buffer.write(chosen_token)
			prog_buffer.write(" ")
			lexer_buffer.write(chosen_token)
			lexer_buffer.write(" ")
			lexer_buffer.write(token)
			lexer_buffer.write("\n")
		else:
			prog_buffer.write(token)
			prog_buffer.write(" ")
			lexer_buffer.write(token)
			lexer_buffer.write(" ")
			lexer_buffer.write(value)
			lexer_buffer.write("\n")

	prog_buffer.flush()
	prog_buffer.close()
	lexer_buffer.flush()
	lexer_buffer.close()
	return prog_file, lexer_file, output_file


if PWD.endswith("glang"):
	lexer = os.path.join(PWD, "frontend/lexer.py")
elif PWD.endswith("tests"):
	lexer = os.path.join(PWD, "../frontend/lexer.py")
else:
	print "Run from glang or glang/tests directory."
	sys.exit(-1)

prog_file, lexer_file, output_file = generate_random_tokens(int(sys.argv[1]))
subprocess.call(["python", lexer, prog_file, output_file])
subprocess.call(["diff", lexer_file, output_file])
