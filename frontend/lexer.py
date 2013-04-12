# ----------------------------------------------------------------------
# lexer.py
#
# Lexical analyzer for symbols in Gramola.
#
# TODO: wrap this lexer in a subclass of Lexer class, so that token()
# method can be overridden to handle ENDMARKER, remaining DEDENTS,
# and possible unmatched brackets.
#
# ----------------------------------------------------------------------

# pylint: disable=C0103
# "Invalid name...."

from ply import lex
from ply.lex import TOKEN
from ply import yacc


class Error(Exception):
    'Generic error class.'


class InconsistentDedentError(Error):
    'Raised when a dedent does not match a previous indentation level.'


class UnmatchedBracketError(Error):
    'Raised when inconsistent enclosing brackets break implicit line joining.'


# Reserved words
reserved = {
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
	# 'None': 'NONE',
}


tokens = (
    # Literals (identifier, number literal, string literal)
    'NAME', 'NUMBER', 'STRING',

    # Operators (+, -, *, **, /, %, <, <=, >, >=, ==, !=)
    'PLUS', 'MINUS', 'STAR', 'DOUBLESTAR', 'SLASH', 'PERCENT',
    'LESS', 'LESSEQUAL', 'GREATER', 'GREATEREQUAL', 'EQUAL', 'NOTEQUAL',

    # Delimiters , : . = ( ) [ ] { }
    'COMMA', 'COLON', 'DOT', 'ASSIGN',
    'LPAREN', 'RPAREN',
    'LBRACKET', 'RBRACKET',
    'LBRACE', 'RBRACE',
	'NEWLINE',

    # Indentation
    'INDENT', 'DEDENT', 'ENDMARKER',
    ) + tuple(reserved.values())


## Operators
t_PLUS             = r'\+'
t_MINUS            = r'-'
t_STAR             = r'\*'
t_DOUBLESTAR       = r'\*\*'
t_SLASH            = r'/'
t_PERCENT          = r'%'
t_LESS             = r'<'
t_LESSEQUAL        = r'<='
t_GREATER          = r'>'
t_GREATEREQUAL     = r'>='
t_EQUAL            = r'=='
t_NOTEQUAL         = r'!='


## Delimiters
t_COMMA            = r','
t_COLON            = r':'
t_DOT              = r'\.'
t_ASSIGN           = r'='


def t_LPAREN(t):
    r'\('
    t.lexer.implicit_line_joining_level += 1
    return t


def t_RPAREN(t):
    r'\)'
    t.lexer.implicit_line_joining_level -= 1
    if t.lexer.implicit_line_joining_level < 0:
        raise UnmatchedBracketError(str(t))
    return t


def t_LBRACKET(t):
    r'\['
    t.lexer.implicit_line_joining_level += 1
    return t


def t_RBRACKET(t):
    r'\]'
    t.lexer.implicit_line_joining_level -= 1
    if t.lexer.implicit_line_joining_level < 0:
        raise UnmatchedBracketError(str(t))
    return t


def t_LBRACE(t):
    r'\{'
    t.lexer.implicit_line_joining_level += 1
    return t


def t_RBRACE(t):
    r'\}'
    t.lexer.implicit_line_joining_level -= 1
    if t.lexer.implicit_line_joining_level < 0:
        raise UnmatchedBracketError(str(t))
    return t


## Identifiers and reserved words
# If lexeme is a reserved word, uses its appropriate token type
def t_NAME(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = reserved.get(t.value, 'NAME')
    return t


## Number literal
digits_re = r'(\d+)'
# Int must be 0, or multiple digits not starting with 0
int_re = r'(0|[1-9]{0}?)'.format(digits_re)
# Float must have an int left of decimal point,
# and must have at least one digit after it
float_re = r'({0}\.{1})'.format(int_re, digits_re)
number_literal = r'({0}|{1})'.format(int_re, float_re)
@TOKEN(number_literal)
def t_NUMBER(t):
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t


## String literal
# TODO: how to handle Unicode?
escape = r'(\\.)'
# TODO: make sure these quotes work, i.e., they don't need escaping
single_quote_string = r"('({0}|[^\\\n'])*')".format(escape)
double_quote_string = r'("({0}|[^\\\n"])*")'.format(escape)
string_literal = r'({0}|{1})'.format(single_quote_string, double_quote_string)
@TOKEN(string_literal)
def t_STRING(t):
    return t


## Newline equivalent
# Optional whitespace, optional comment, then at least one newline.
# We emit a NEWLINE token only if:
# - we're not implicitly joining logical lines, and
# - we're not at the start of the line.
# For all other whitespace, including line-initial, see t_WS().
newline = r'(\r?\n)'
newline_equivalent = r'[ \t]*(\#.*)?{0}+'.format(newline)
@TOKEN(newline_equivalent)
def t_NEWLINE(t):
    if not t.lexer.implicit_line_joining_level and find_column(t):
        # E.g., at the end of a statement, or just before a suite of them
        t.type = 'NEWLINE'
        return t


## All other whitespace
# We only do indent/dedent calculations if:
# - we're not implicitly joining logical lines, and
# - we're either at the start of the line, or else we're not in the process of
#   dedenting.
def t_WS(t):
    r'[ \t]+'
    if (t.lexer.implicit_line_joining_level or
        (find_column(t) and not t.lexer.dedenting)):
        # Ignore this whitespace; we're either joining logical lines, or
        # we're not at the start of the line (and not dedenting)
        return None

    num_tabs = t.value.count('\t') + t.value.count(t.lexer.tab)
    if num_tabs == t.lexer.indent_stack[-1]:
        # Same indentation as previous logical line
        return None

    if num_tabs > t.lexer.indent_stack[-1]:
        t.lexer.indent_stack.append(num_tabs)
        t.type = 'INDENT'
        t.value = get_first_tab_substring(t)
        return t

    t.lexer.indent_stack.pop()
    if num_tabs > t.lexer.indent_stack[-1]:
        raise InconsistentDedentError(str(t.lexer.indent_stack))
    elif num_tabs == t.lexer.indent_stack[-1]:
        # We're at a proper indentation level
        t.lexer.dedenting = False
    else:
        # Rewind the lexer position to just after the first "tab", so that
        # we can emit another DEDENT token
        rewind_lexer_for_dedenting(t)
        # Let the lexer know that we need another round of dedenting
        t.lexer.dedenting = True
    t.type = 'DEDENT'
    t.value = get_first_tab_substring(t)
    return t


def t_error(t):
    print "Illegal character '{0}'".format(t.value)
    t.lexer.skip(1)


# Compute column index (starting from 0).
def find_column(token):
    last_cr = token.lexer.lexdata.rfind('\n', 0, token.lexpos)
    column = token.lexpos - (last_cr + 1)
    return column


def rewind_lexer_for_dedenting(token):
    tab = get_first_tab_substring(token)
    token.lexer.lexpos = token.lexpos + len(tab)


def get_first_tab_substring(token):
    if token.value.startswith('\t'):
        return '\t'
    elif token.value.startswith(token.lexer.tab):
        return token.lexer.tab


lexer = lex.lex()
lexer.implicit_line_joining_level = 0
lexer.tab = ' ' * 4
# Pushed when indenting, popped when dedenting
lexer.indent_stack = [0]
lexer.dedenting = False


def lexer_test(filename):
	'''To parse a file containing Gramola code and print all Lexical Tokens.'''
	fd = open(filename, "r")
	lexer.input(fd.read())
	fd.close()

	for tok in lexer:
		# output = "@" + str(tok.lineno) + ":" + str(tok.lexpos) + "\t" \
					# + str(tok.value) + "\t" + tok.type
		# print output
		print tok


# ----------------------------------------------------------------------
# Parser begins now that tokenizing is done.
# ----------------------------------------------------------------------

def p_start(p):
	'''start : ENDMARKER
			 | content_list ENDMARKER'''
	pass


def p_content_list(p):
	'''content_list : content
					| content_list content'''
	pass


def p_content(p):
	'''content : NEWLINE
			   | top_level_stmt'''
	pass


def p_function_def(p):
	'''function_def : DEF NAME NAME LPAREN RPAREN COLON suite
					| DEF NAME NAME LPAREN parameter_list RPAREN COLON suite'''
	pass


def p_parameter_list(p):
	'''parameter_list : param
					  | parameter_list COMMA param'''
	pass


def p_param(p):
	'''param : NAME NAME'''
	pass


def p_top_level_stmt(p):
	'''top_level_stmt : stmt
					  | function_def
					  | class_def'''
	pass


def p_stmt(p):
	'''stmt : simple_stmt
			| compound_stmt'''
	pass


def p_simple_stmt(p):
	'''simple_stmt : small_stmt NEWLINE
				   | declaration'''
	pass


def p_small_stmt(p):
	'''small_stmt : expr
				  | assignment_stmt
				  | print_stmt
				  | flow_stmt'''
	pass


def p_assignment_stmt(p):
	'''assignment_stmt : NAME target ASSIGN expr'''
	pass


def p_target(p):
	'''target : NAME
			  | attribute_ref
			  | subscription'''
	pass



# def p_target_list(p):
	'''target_list : target
				   | target_list COMMA target'''
	# pass


def p_print_stmt(p):
	'''print_stmt : PRINT
				  | PRINT expr_list'''
	pass


def p_flow_stmt(p):
	'''flow_stmt : BREAK
				 | CONTINUE
				 | RETURN
				 | RETURN expr'''
	pass


def p_declaration(p):
	'''declaration : NAME name_list NEWLINE'''
	pass


def p_name_list(p):
	'''name_list : NAME
				 | name_list COMMA NAME'''
	pass


def p_compound_stmt(p):
	'''compound_stmt : if_stmt
					 | while_stmt
					 | for_stmt'''
	pass


def p_if_stmt(p):
	'''if_stmt : IF expr COLON suite
			   | IF expr COLON suite else_clause
			   | IF expr COLON suite elif_clauses else_clause'''
	pass


def p_elif_clauses(p):
	'''elif_clauses : elif_clause
					| elif_clauses elif_clause'''
	pass


def p_elif_clause(p):
	'''elif_clause : ELIF expr COLON suite'''
	pass


def p_else_clause(p):
	'''else_clause : ELSE expr COLON suite'''
	pass


def p_while_stmt(p):
	'''while_stmt : WHILE expr COLON suite'''
	pass


def p_for_stmt(p):
	'''for_stmt : FOR NAME NAME IN primary COLON suite'''
	pass


def p_suite(p):
	'''suite : simple_stmt
			 | NEWLINE INDENT stmt_list DEDENT'''
	pass


def p_stmt_list(p):
	'''stmt_list : stmt
				 | stmt_list stmt'''
	pass


def p_expr_list(p):
	'''expr_list : expr
				 | expr_list COMMA expr'''
	pass


def p_expr(p):
	'''expr : or_test''' 
	pass


def p_or_test(p):
	'''or_test : and_test
			   | or_test OR and_test'''
	pass


def p_and_test(p):
	'''and_test : not_test
				| and_test AND not_test'''
	pass


def p_not_test(p):
	'''not_test : comparison
				| NOT not_test'''
	pass


def p_comparison(p):
	'''comparison : arith_expr
				  | comparison comp_op arith_expr'''
	pass


def p_comp_op(p):
	'''comp_op : LESS
			   | LESSEQUAL
			   | GREATER
			   | GREATEREQUAL
			   | EQUAL
			   | NOTEQUAL
			   | IN
			   | NOT IN
			   | IS
			   | NOT IS'''
	pass


def p_arith_expr(p):
	'''arith_expr : mult_expr
				  | arith_expr arith_op mult_expr'''
	pass


def p_arith_op(p):
	'''arith_op : PLUS
				| MINUS'''
	pass


def p_mult_expr(p):
	'''mult_expr : unary_expr
				 | mult_expr mult_op unary_expr'''
	pass


def p_mult_op(p):
	'''mult_op : STAR
			   | SLASH
			   | PERCENT'''
	pass


def p_unary_expr(p):
	'''unary_expr : power
				  | unary_op unary_expr'''
	pass


def p_unary_op(p):
	'''unary_op : PLUS
				| MINUS'''
	pass


def p_power(p):
	'''power : primary
			 | primary DOUBLESTAR unary_expr'''
	pass


def p_primary(p):
	'''primary : atom
			   | attribute_ref
			   | subscription
			   | call'''
	pass


def p_atom(p):
	'''atom : NAME
			| literal
			| enclosure'''
	pass


def p_literal(p):
	'''literal : string_list
			   | NUMBER'''
	pass


def p_string_list(p):
	'''string_list : STRING
				   | string_list STRING'''
	pass


def p_enclosure(p):
	'''enclosure : LPAREN expr RPAREN
				 | LBRACKET expr_list RBRACKET
				 | LBRACE key_datum_list RBRACE
				 | LBRACE expr_list RBRACE'''
	pass


def p_key_datum_list(p):
	'''key_datum_list : key_datum
					  | key_datum_list COMMA key_datum'''
	pass


def p_key_datum(p):
	'''key_datum : expr COLON expr'''
	pass


def p_attribute_ref(p):
	'''attribute_ref : primary DOT NAME'''
	pass


def p_subscription(p):
	'''subscription : primary LBRACKET expr RBRACKET'''
	pass


# TODO
def p_call(p):
	'''call : primary LPAREN argument_list RPAREN'''
	pass


def p_argument_list(p):
	'''argument_list : expr
					 | argument_list COMMA expr'''
	pass


def p_class_def(p):
	'''class_def : CLASS NAME LPAREN RPAREN COLON class_def_suite
				 | CLASS NAME LPAREN NAME RPAREN COLON class_def_suite'''
	pass


def p_class_def_suite(p):
	'''class_def_suite : NEWLINE INDENT class_stmt_list DEDENT'''
	pass


def p_class_stmt_list(p):
	'''class_stmt_list : function_defs
					   | declarations function_defs
					   | node_types_def function_defs
					   | declarations node_types_def function_defs'''
	pass


def p_declarations(p):
	'''declarations : declaration
					| declarations declaration'''
	pass


def p_node_types_def(p):
	'''node_types_def : assignment_stmt NEWLINE'''
	pass


def p_function_defs(p):
	'''function_defs : function_def
					 | function_defs function_def'''
	pass


def p_error(p):
	print "Syntax error in", p


parser = yacc.yacc()


'''
import sys
lexer_test(sys.argv[1])
'''
