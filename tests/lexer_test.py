#! /usr/bin/python
'''
Date: 21st April, 2013
Purpose: To test the tokenizing of lexer.py.
Usage: python lexer_test.py <number_of_tokens>
'''

import os, random, subprocess, sys


PWD = os.getcwd()
TOKENS = {
	'=': 'ASSIGN',
	':': 'COLON',
	',': 'COMMA',
	'dedent': 'DEDENT',
	'.': 'DOT',
	'**': 'DOUBLESTAR',
	'==': 'EQUAL',
	'>': 'GREATER',
	'>=': 'GREATEREQUAL',
	'\t': 'INDENT',
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
	expected_file = os.path.join(PWD, prog_file.replace(".gr", ".exp"))
	lexer_file = os.path.join(PWD, prog_file.replace(".gr", ".lex"))
	prog_buffer = open(prog_file, "w")
	expected_buffer = open(expected_file, "w")
	braces = 0
	brackets = 0
	parens = 0
	tabs = 0

	for i in xrange(0, count):
		token = random.choice(TOKENS.keys())
		value = TOKENS[token]

		if type(value) == list:
			chosen_token = str(random.choice(value))
			prog_buffer.write(chosen_token)
			prog_buffer.write(" ")
			expected_buffer.write(chosen_token)
			expected_buffer.write(" ")
			expected_buffer.write(token)
			expected_buffer.write("\n")
		else:
			if value == "LBRACE":
				braces += 1
			elif value == "RBRACE":
				if braces == 0:
					continue
				else:
					braces -= 1
			elif value == "LBRACKET":
				brackets += 1
			elif value == "RBRACKET":
				if brackets == 0:
					continue
				else:
					brackets -= 1
			elif value == "LPAREN":
				parens += 1
			elif value == "RPAREN":
				if parens == 0:
					continue
				else:
					parens -= 1
			elif value == "INDENT":
				tabs += 1
				continue
			elif value == "DEDENT":
				if tabs > 0:
					tabs -= 1
				continue
			elif value == "NEWLINE":
				if tabs > 0:
					token = "\n" + "\t" * tabs
				else:
					continue

			prog_buffer.write(token)
			prog_buffer.write(" ")
			expected_buffer.write(token)
			expected_buffer.write(" ")
			expected_buffer.write(value)
			expected_buffer.write("\n")

	prog_buffer.flush()
	prog_buffer.close()
	expected_buffer.flush()
	expected_buffer.close()
	return prog_file, expected_file, lexer_file


if len(sys.argv) == 1:
	print "Usage: python", sys.argv[0], "<number_of_tokens>"
	sys.exit(-1)

if PWD.endswith("glang"):
	lexer = os.path.join(PWD, "frontend/lexer.py")
elif PWD.endswith("tests"):
	lexer = os.path.join(PWD, "../frontend/lexer.py")
else:
	print "Run from glang or glang/tests directory."
	sys.exit(-1)

prog_file, expected_file, lexer_file = generate_random_tokens(int(sys.argv[1]))
subprocess.call(["python", lexer, prog_file, lexer_file])
subprocess.call(["diff", expected_file, lexer_file])
