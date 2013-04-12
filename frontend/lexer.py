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
    'from': 'FROM',
    'if': 'IF',
	'import': 'IMPORT',
    'in': 'IN',
    'is': 'IS',
    'not': 'NOT',
    'or': 'OR',
    'print': 'PRINT',
    'return': 'RETURN',
    'while': 'WHILE',
	'None': 'NONE',
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

import sys
lexer_test(sys.argv[1])
