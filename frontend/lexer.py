#!/usr/bin/python2.7

'Lexical analyzer for symbols in Gramola.'

# pylint: disable=C0103
# "Invalid name...."

import sys
from ply import lex
from ply.lex import TOKEN

TAB_WIDTH = 4  # in spaces


class Error(Exception):
    'Generic error class.'


class InconsistentDedentError(Error):
    'Raised when a dedent does not match a previous indentation level.'


class UnmatchedBracketError(Error):
    'Raised when inconsistent enclosing brackets break implicit line joining.'


class Lexer(object):

    # Reserved words
    _reserved = {
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
        ) + tuple(_reserved.values())

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

    ## Helper regular expressions

    ## For number literals
    digits_re = r'(\d+)'
    # Int must be 0, or multiple digits not starting with 0
    int_re = r'(0|[1-9]{0}?)'.format(digits_re)
    # Float must have an int left of decimal point,
    # and must have at least one digit after it
    float_re = r'({0}\.{1})'.format(int_re, digits_re)
    # Note: order of disjuncts matters, because int is a prefix of float
    number_literal = r'({0}|{1})'.format(float_re, int_re)

    ## For string literals
    escape = r'(\\.)'
    # NB: the \ character does *not* do explicit line joining
    single_quote_string = r"('({0}|[^\n'])*')".format(escape)
    double_quote_string = r'("({0}|[^\n"])*")'.format(escape)
    string_literal = r'({0}|{1})'.format(single_quote_string,
                                         double_quote_string)

    newline = r'(\r?\n)'
    newline_equivalent = r'[ \t]*(\#.*)?{0}+'.format(newline)

    def t_LPAREN(self, t):
        r'\('
        self._implicit_line_joining_level += 1
        return t

    def t_RPAREN(self, t):
        r'\)'
        self._implicit_line_joining_level -= 1
        if self._implicit_line_joining_level < 0:
            raise UnmatchedBracketError(str(t))
        return t

    def t_LBRACKET(self, t):
        r'\['
        self._implicit_line_joining_level += 1
        return t

    def t_RBRACKET(self, t):
        r'\]'
        self._implicit_line_joining_level -= 1
        if self._implicit_line_joining_level < 0:
            raise UnmatchedBracketError(str(t))
        return t

    def t_LBRACE(self, t):
        r'\{'
        self._implicit_line_joining_level += 1
        return t

    def t_RBRACE(self, t):
        r'\}'
        self._implicit_line_joining_level -= 1
        if self._implicit_line_joining_level < 0:
            raise UnmatchedBracketError(str(t))
        return t

    ## Identifiers and reserved words
    # If lexeme is a reserved word, uses its appropriate token type
    def t_NAME(self, t):
        r'[A-Za-z_][A-Za-z0-9_]*'
        t.type = self._reserved.get(t.value, 'NAME')
        if (t.type in ('DEF', 'CLASS') and self._indent_stack[-1] != 0 and
            not self._find_column(t)):
            # We have line-initial content after an indented block, so dedent
            self._indent_stack.pop()
            self._lexer.lexpos -= len(t.value)
            return self._make_token('DEDENT', self._indent_stack[-1])
        return t

    @TOKEN(number_literal)
    def t_NUMBER(self, t):
        if '.' in t.value:
            t.value = float(t.value)
        else:
            t.value = int(t.value)
        return t

    @TOKEN(string_literal)
    def t_STRING(self, t):
        return t

    ## Newline equivalent
    # Optional whitespace, optional comment, then at least one newline
    # We emit a NEWLINE token only if:
    # - we're not implicitly joining logical lines, and
    # - we're not at the start of the line.
    # For all other whitespace, including line-initial, see t_WS().
    @TOKEN(newline_equivalent)
    def t_NEWLINE(self, t):
        self._lexer.lineno += t.value.count('\n')
        if not self._implicit_line_joining_level and self._find_column(t):
            # We're at the end of a statement, or just before a suite of them
            t.type = 'NEWLINE'
            return t


    ## All other whitespace
    # We only do indent/dedent calculations if:
    # - we're not implicitly joining logical lines, and
    # - we're either at the start of the line, or else we're not in the process
    #   of dedenting.
    def t_WS(self, t):
        r'[ \t]+'
        if (self._implicit_line_joining_level or
            (self._find_column(t) and not self._dedenting)):
            # Ignore this whitespace; we're either joining logical lines, or
            # we're not at the start of the line (and not dedenting)
            return None

        num_tabs = t.value.count('\t') + t.value.count(self._tab)
        if num_tabs == self._indent_stack[-1]:
            # Same indentation as previous logical line
            return None

        if num_tabs > self._indent_stack[-1]:
            self._indent_stack.append(num_tabs)
            t.type = 'INDENT'
            t.value = num_tabs
            return t

        self._indent_stack.pop()
        indent_level = self._indent_stack[-1]
        if num_tabs > indent_level:
            raise InconsistentDedentError(str(self._indent_stack))
        elif num_tabs == indent_level:
            # We're at a proper indentation level
            self._dedenting = False
        else:
            # Rewind the lexer position to just after the first "tab", so that
            # we can emit another DEDENT token
            self._rewind_lexer_for_dedenting(t)
            # Let the lexer know that we need another round of dedenting
            self._dedenting = True
        t.type = 'DEDENT'
        t.value = indent_level
        return t

    def t_error(self, t):
        print "Illegal character '{0}'".format(t.value)
        # TODO: smarter error handling
        self._lexer.skip(1)

    # Compute column index (starting from 0).
    # NB: This counts one column per character, including tabs
    def _find_column(self, token):
        last_cr = self._lexer.lexdata.rfind('\n', 0, token.lexpos)
        column = token.lexpos - (last_cr + 1)
        return column

    def _rewind_lexer_for_dedenting(self, token):
        tab = self._get_first_tab_substring(token)
        self._lexer.lexpos = token.lexpos + len(tab)

    def _get_first_tab_substring(self, token):
        if token.value.startswith('\t'):
            return '\t'
        elif token.value.startswith(self._tab):
            return self._tab

    def __init__(self, **kwargs):
        self._lexer = lex.lex(module=self, **kwargs)
        self._tab = ' ' * TAB_WIDTH
        self._indent_stack = None
        self._dedenting = None
        self._implicit_line_joining_level = None
        self._reset()

    def _reset(self):
        # Pushed when indenting, popped when dedenting
        self._indent_stack = [0]
        # Are we in the process of dedenting multiple times?
        self._dedenting = False
        self._implicit_line_joining_level = 0

    def __iter__(self):
        return self

    def next(self):
        token = self.token()
        if token is None:
            raise StopIteration
        return token

    def token(self):
        token = self._lexer.token()
        if token is not None:
            return token
        if not self._indent_stack:
            # Reset this custom lexer
            self._reset()
            return None
        level = self._indent_stack.pop()
        if not level:
            # We're at the end of the file, without any indentation
            return self._make_token('ENDMARKER', None)
        # We have some indentation to unwind before we're done
        return self._make_token('DEDENT', self._indent_stack[-1])

    def _make_token(self, tok_type, tok_value):
        token = lex.LexToken()
        token.type = tok_type
        token.value = tok_value
        token.lineno = self._lexer.lineno
        token.lexpos = self._lexer.lexpos
        return token

    def input(self, s):
        return self._lexer.input(s)


def main(args):
    # Tokenize a file containing Gramola code
    if not len(args):
        print >> sys.stderr, 'ERROR: Must provide the lexer with a filename!'
        sys.exit(1)

    filename = args[0]

    lexer = Lexer()
    with open(filename, 'r') as fd:
        lexer.input(fd.read())

	try:
		with open(args[1], "w") as ofd:
			for tok in lexer:
				print >>ofd, str(tok.value), str(tok.type)
	except IndexError:
		for tok in lexer:
			print str(tok.value), str(tok.type)


if __name__ == '__main__':
    main(sys.argv[1:])
