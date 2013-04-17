# ----------------------------------------------------------------------
# parser.py
#
# Parser for Gramola.
#
# ----------------------------------------------------------------------

# pylint: disable=C0103
# "Invalid name...."

import sys
from ply import yacc
from lexer import Lexer


class Error(Exception):
    'Generic error class.'


class SymbolAlreadyPresentError(Error):
    'Raised when a declared symbol is already in the symbol table.'


class SymbolMissingError(Error):
    'Raised when a referenced symbol is not in the symbol table.'


class Node(object):

    def __init__(self, node_type, **kwargs):
        self._type = node_type
        self.__dict__.update(kwargs)

    @property
    def type(self):
        return self._type


# TODO: implement a stack of symbol tables
class Parser(object):

    # Set in __init__()
    tokens = None
    start = 'start'

    def __init_(self, lexer=None):
        self._lexer = lexer or Lexer()
        self.tokens = self._lexer.tokens
        self._parser = yacc.yacc(module=self)

    def parse(self, s, **kwargs):
        lexer = kwargs.pop('lexer', self._lexer)
        self._parser.parse(s, lexer=lexer, **kwargs)

    def p_empty(p):
        'empty :'
        pass

    def p_start(p):
	'start : opt_top_level_stmt_list ENDMARKER'
        p[0] = Node('start', stmt_list=p[1])

    def p_opt_top_level_stmt_list(p):
        'opt_top_level_stmt_list : top_level_stmt_list | empty'
        p[0] = p[1] or []

    def p_top_level_stmt_list(p):
        '''top_level_stmt_list : top_level_stmt
                               | top_level_stmt top_level_stmt_list'''
        p[0] = [p[1]]
        if len(p) == 3:
            p[0].extend(p[2])

    def p_top_level_stmt(p):
	'top_level_stmt : function_def | class_def'
        p[0] = p[1]

    def p_function_def(p):
        '''function_def : DEF typed_id LPAREN opt_parameter_list RPAREN COLON
                          suite'''
        # TODO: do symbol table lookups
        p[0] = Node('function_def', return_type=p[2], name=p[3], params=p[5],
                    body=p[8])

    def p_opt_parameter_list(p):
        'opt_parameter_list : parameter_list | empty'
        p[0] = p[1] or []

    def p_parameter_list(p):
	'parameter_list : typed_id | parameter_list COMMA typed_id'
        if len(p) == 4:
            p[0] = p[1]
            p[0].append(p[3])
        else:
            p[0] = [p[1]]

    def p_typed_id(p):
	'typed_id : NAME NAME'
        # TODO: store in symbol table, raising an error if it already exists
	p[0] = Node('id', id_type=p[1], id_name=p[2])

    def p_id_opt_type(p):
        'id_opt_type : typed_id | NAME'
        # TODO: fix this! shift/reduce conflict when RHS starts with NAME
        # TODO: do symbol table lookup here, only set target type if needed
        rhs = p[1]
        if p[1].type == 'NAME':
            # TODO: lookup type in symbol table
            rhs = Node('id', id_type=???, id_name=p[1])
        p[0] = rhs

    def p_stmt(p):
	'stmt : simple_stmt | compound_stmt'
	p[0] = p[1]

    def p_simple_stmt(p):
	'''simple_stmt : small_stmt NEWLINE
                       | declaration'''
        p[0] = p[1]

    def p_small_stmt(p):
	'''small_stmt : expr
                      | assignment_stmt
                      | print_stmt
                      | flow_stmt'''
	p[0] = p[1]

    def p_assignment_stmt(p):
	'assignment_stmt : target ASSIGN expr'
        p[0] = Node('assignment', target=p[1], value=p[3])

    def p_target(p):
	'''target : id_opt_type
                  | attribute_ref
                  | subscription'''
	p[0] = p[1]

# TODO: finish the rest of the rules
def p_target_list(p):
	'''target_list : target
        | target_list COMMA target'''
	pass


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
	if len(p) > 2:
		p[0] = p[1], p[3]
	else:
		p[0] = p[1]


def p_expr(p):
	'''expr : or_test''' 
	p[0] = p[1]


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
			   | IS NOT'''
	if len(p) > 2:
		p[0] = p[1] + " " + p[2]
	else:
		p[0] = p[1]


def p_arith_expr(p):
	'''arith_expr : mult_expr
				  | arith_expr arith_op mult_expr'''
	if len(p) > 2:
		if p[2] == "+":
			p[0] = p[1] + p[3]
		else:
			p[0] = p[1] - p[3]
	else:
		p[0] = p[1]


def p_arith_op(p):
	'''arith_op : PLUS
				| MINUS'''
	p[0] = p[1]


def p_mult_expr(p):
	'''mult_expr : unary_expr
				 | mult_expr mult_op unary_expr'''
	if len(p) > 2:
		if p[2] == "*":
			p[0] = p[1] * p[3]
		elif p[2] == "/":
			p[0] = 0.0 + p[1] / p[3]
		else:
			p[0] = p[1] % p[3]
	else:
		p[0] = p[1]


def p_mult_op(p):
	'''mult_op : STAR
			   | SLASH
			   | PERCENT'''
	p[0] = p[1]


def p_unary_expr(p):
	'''unary_expr : power
				  | unary_op unary_expr'''
	if len(p) > 2:
		if p[1] == "+":
			p[0] = p[2]
		else:
			p[0] = -p[2]
	else:
		p[0] = p[1]


def p_unary_op(p):
	'''unary_op : PLUS
				| MINUS'''
	p[0] = p[1]


def p_power(p):
	'''power : primary
			 | primary DOUBLESTAR unary_expr'''
	if len(p) > 2:
		p[0] = p[1] ** p[3]
	else:
		p[0] = p[1]


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
	p[0] = p[1]


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





def main(args):
    # Parse a file containing Gramola code and print the result
    if not len(args):
        print >> sys.stderr, 'ERROR: Must provide the parser with a filename!'
        sys.exit(1)

    filename = args[0]
    parser = Parser()
    with open(filename, 'r') as fd:
        result = parser.parse(fd.read())

    print str(result)


if __name__ == '__main__':
    main(sys.argv[1:])

