# ----------------------------------------------------------------------
# parser.py
#
# Parser for Gramola.
#
# NB: by convention, whenever the grammar calls for an optional rule,
# we create a separate method "opt_RULENAME" that matches either that
# rule, or "empty".
#
# TODO: implement symbol table
#
# ----------------------------------------------------------------------

# pylint: disable=C0103
# "Invalid name"
# pylint: disable=R0201
# "Method could be a function"

import pprint
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
        self._node_type = node_type
        self.__dict__.update(kwargs)
        # TODO: maintain "parent" pointers within Node "children"?

    @property
    def node_type(self):
        return self._node_type

    def __str__(self):
        # TODO: find better way to print this
        return '<Node {0}>'.format(pprint.pformat(self.__dict__))

    def __repr__(self):
        return str(self)


class Parser(object):

    # Set in __init__()
    tokens = None
    start = 'start'

    def __init__(self, lexer=None):
        self._lexer = lexer or Lexer()
        self.tokens = self._lexer.tokens
        self._parser = yacc.yacc(module=self)

    def parse(self, s, **kwargs):
        lexer = kwargs.pop('lexer', self._lexer)
        self._parser.parse(s, lexer=lexer, **kwargs)

    def p_empty(self, p):
        'empty :'
        pass

    def p_start(self, p):
        'start : opt_top_level_stmt_list ENDMARKER'
        p[0] = Node('start', stmt_list=p[1])

    def p_opt_top_level_stmt_list(self, p):
        '''opt_top_level_stmt_list : top_level_stmt_list
                                   | empty'''
        p[0] = p[1] or []

    def p_top_level_stmt_list(self, p):
        '''top_level_stmt_list : top_level_stmt
                               | top_level_stmt top_level_stmt_list'''
        p[0] = [p[1]]
        if len(p) == 3:
            p[0].extend(p[2])

    def p_top_level_stmt(self, p):
        '''top_level_stmt : function_def
                          | class_def'''
        p[0] = p[1]

    def p_function_def(self, p):
        'function_def : DEF type name LPAREN opt_parameter_list RPAREN COLON suite'
        # We keep "type" and "name" separate (as opposed to using type_and_name)
        # because we don't want to create a declaration Node for the function
        # name
        p[0] = Node('function_def', return_type=p[2], name=p[3], params=p[5],
                    body=p[8])

    def p_type(self, p):
        'type : NAME'
        # TODO: manage symbol table
        p[0] = Node('type', value=p[1])

    def p_name(self, p):
        'name : NAME'
        # TODO: manage symbol table
        p[0] = Node('name', value=p[1])

    def p_opt_parameter_list(self, p):
        '''opt_parameter_list : parameter_list
                              | empty'''
        p[0] = p[1] or []

    def p_parameter_list(self, p):
        '''parameter_list : type_and_name
                          | parameter_list COMMA type_and_name'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1]
            p[0].append(p[3])

    def p_type_and_name(self, p):
        'type_and_name : type name'
        # TODO: manage symbol table
        p[0] = Node('declaration', type=p[1], names=[p[2]])

    def p_stmt(self, p):
        '''stmt : simple_stmt
                | compound_stmt'''
        p[0] = p[1]

    def p_simple_stmt(self, p):
        '''simple_stmt : small_stmt NEWLINE
                       | declaration'''
        p[0] = p[1]

    def p_small_stmt(self, p):
        '''small_stmt : expr
                      | assignment_stmt
                      | print_stmt
                      | flow_stmt'''
        p[0] = p[1]

    def p_assignment_stmt(self, p):
        'assignment_stmt : target ASSIGN expr'
        p[0] = Node('assignment', target=p[1], value=p[3])

    def p_target(self, p):
        '''target : id_opt_type
                  | attribute_ref
                  | subscription'''
        p[0] = p[1]

    def p_id_opt_type(self, p):
        '''id_opt_type : type_and_name
                       | name'''
        # TODO: make sure this doesn't cause a shift/reduce conflict
        p[0] = p[1]

    def p_print_stmt(self, p):
        'print_stmt : PRINT opt_expr_list'
        p[0] = Node('print', values=p[2])

    def p_opt_expr_list(self, p):
        '''opt_expr_list : expr_list
                         | empty'''
        p[0] = p[1] or []

    def p_flow_stmt(self, p):
        '''flow_stmt : break_stmt
                     | continue_stmt
                     | return_stmt'''
        p[0] = p[1]

    def p_break_stmt(self, p):
        'break_stmt : BREAK'
        p[0] = Node('break')

    def p_continue_stmt(self, p):
        'continue_stmt : CONTINUE'
        p[0] = Node('continue')

    def p_return_stmt(self, p):
        'return_stmt : RETURN opt_expr'
        p[0] = Node('return', value=p[2])

    def p_opt_expr(self, p):
        '''opt_expr : expr
                    | empty'''
        p[0] = p[1]

    def p_declaration(self, p):
        'declaration : type name_list NEWLINE'
        p[0] = Node('declaration', type=p[1], names=p[2])

    def p_name_list(self, p):
        '''name_list : name
                     | name_list COMMA name'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1]
            p[0].append(p[3])

    def p_compound_stmt(self, p):
        '''compound_stmt : if_stmt
                         | while_stmt
                         | for_stmt'''
        p[0] = p[1]

    def p_if_stmt(self, p):
        'if_stmt : IF expr COLON suite opt_elif_clauses opt_else_clause'
        elses = p[5]  # might be a list of "if" Nodes
        if p[6]:
            elses.append(p[6])
        p[0] = Node('if', test=p[2], body=p[4], elses=elses)

    def p_opt_elif_clauses(self, p):
        '''opt_elif_clauses : elif_clauses
                            | empty'''
        p[0] = p[1] or []

    def p_opt_else_clause(self, p):
        '''opt_else_clause : else_clause
                           | empty'''
        p[0] = p[1]

    def p_elif_clauses(self, p):
        '''elif_clauses : elif_clause
                        | elif_clauses elif_clause'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1]
            p[0].append(p[2])

    def p_elif_clause(self, p):
        'elif_clause : ELIF expr COLON suite'
        p[0] = Node('if', test=p[2], body=p[4])

    def p_else_clause(self, p):
        'else_clause : ELSE COLON suite'
        p[0] = p[3]

    def p_while_stmt(self, p):
        'while_stmt : WHILE expr COLON suite'
        p[0] = Node('while', test=p[2], body=p[4])

    def p_for_stmt(self, p):
        'for_stmt : FOR id_opt_type IN primary COLON suite'
        p[0] = Node('for', target=p[2], iterable=p[4], body=p[6])

    def p_suite(self, p):
        'suite : NEWLINE INDENT stmt_list DEDENT'
        p[0] = Node('suite', stmts=p[3])

    def p_stmt_list(self, p):
        '''stmt_list : stmt
                     | stmt_list stmt'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1]
            p[0].append(p[2])

    def p_expr_list(self, p):
        '''expr_list : expr
                     | expr_list COMMA expr'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1]
            p[0].append(p[3])

    def p_expr(self, p):
        'expr : or_test'
        p[0] = p[1]

    def p_or_test(self, p):
        '''or_test : and_test
                   | or_test OR and_test'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = Node('or', left=p[1], right=p[3])

    def p_and_test(self, p):
        '''and_test : not_test
                    | and_test AND not_test'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = Node('and', left=p[1], right=p[3])

    def p_not_test(self, p):
        '''not_test : comparison
                    | NOT not_test'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = Node('not', operand=p[2])

    def p_comparison(self, p):
        '''comparison : arith_expr
                      | arith_expr comp_op arith_expr'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            left = p[1]
            op = p[2]   # this is a string, not a token
            right = p[3]
            not_loc = op.find('not')
            if not_loc < 0:
                p[0] = Node(op, left=left, right=right)
            else:
                # Strip "not" from operator
                op = op[:not_loc - 1] + op[not_loc + 3:]
                p[0] = Node('not', operand=Node(op, left=left, right=right))

    def p_comp_op(self, p):
        '''comp_op : LESS
                   | GREATER
                   | EQUAL
                   | LESSEQUAL
                   | GREATEREQUAL
                   | NOTEQUAL
                   | IN
                   | NOT IN
                   | IS
                   | IS NOT'''
        # sets p[0] to a string, not a token
        p[0] = ' '.join(x.type.lower() for x in p[1:])

    def p_arith_expr(self, p):
        '''arith_expr : mult_expr
                      | arith_expr arith_op mult_expr'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            # p[2] is a string, not a token
            p[0] = Node(p[2], left=p[1], right=p[3])

    def p_arith_op(self, p):
        '''arith_op : PLUS
                    | MINUS'''
        # sets p[0] to a string, not a token
        p[0] = p[1].type.lower()

    def p_mult_expr(self, p):
        '''mult_expr : unary_expr
                     | mult_expr mult_op unary_expr'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            # p[2] is a string, not a token
            p[0] = Node(p[2], left=p[1], right=p[3])

    def p_mult_op(self, p):
        '''mult_op : STAR
                   | SLASH
                   | PERCENT'''
        # sets p[0] to a string, not a token
        p[0] = p[1].type.lower()

    def p_unary_expr(self, p):
        '''unary_expr : power
                      | unary_op unary_expr'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            # p[2] is a string, not a token
            p[0] = Node(p[1], operand=p[2])

    def p_unary_op(self, p):
        '''unary_op : PLUS
                    | MINUS'''
        # sets p[0] to a string, not a token
        p[0] = p[1].type.lower()

    def p_power(self, p):
        '''power : primary
                 | primary DOUBLESTAR unary_expr'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = Node(p[2].type.lower(), left=p[1], right=p[3])

    def p_primary(self, p):
        '''primary : atom
                   | attribute_ref
                   | subscription
                   | call'''
        p[0] = p[1]

    def p_atom(self, p):
        '''atom : name
                | string_list
                | number
                | enclosure'''
        p[0] = p[1]

    def p_string_list(self, p):
        '''string_list : STRING
                       | string_list STRING'''
        p[0] = ''.join(p[1:])

    def p_number(self, p):
        'number : NUMBER'
        p[0] = p[1]

    def p_enclosure(self, p):
        '''enclosure : LPAREN expr RPAREN
                     | LBRACKET expr_list RBRACKET
                     | LBRACE key_datum_list RBRACE
                     | LBRACE expr_set RBRACE'''
        p[0] = p[2]

    def p_key_datum_list(self, p):
        '''key_datum_list : key_datum
                          | key_datum_list COMMA key_datum'''
        if len(p) == 2:
            p[0] = dict([p[1]])
        else:
            p[0] = p[1]
            key, value = p[3]
            p[0][key] = value

    def p_key_datum(self, p):
        'key_datum : expr COLON expr'
        p[0] = (p[1], p[3])

    def p_expr_set(self, p):
        'expr_set : expr_list'
        p[0] = set(p[1])

    def p_attribute_ref(self, p):
        'attribute_ref : primary DOT name'
        p[0] = Node('attribute', value=p[1], attr=p[3])

    def p_subscription(self, p):
        'subscription : primary LBRACKET expr RBRACKET'
        p[0] = Node('subscript', value=p[1], index=p[3])

    def p_call(self, p):
        'call : primary LPAREN opt_argument_list RPAREN'
        p[0] = Node('call', func=p[1], args=p[3])

    def p_opt_argument_list(self, p):
        '''opt_argument_list : argument_list
                             | empty'''
        p[0] = p[1] or []

    def p_argument_list(self, p):
        '''argument_list : expr
                         | argument_list COMMA expr'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1]
            p[0].append(p[3])

    def p_class_def(self, p):
        'class_def : CLASS type LPAREN opt_name RPAREN COLON class_def_suite'
        p[0] = Node('class_def', name=p[2], base=p[4], body=p[7])

    def p_opt_name(self, p):
        '''opt_name : name
                    | empty'''
        p[0] = p[1]

    def p_class_def_suite(self, p):
        'class_def_suite : NEWLINE INDENT class_stmt_list DEDENT'
        p[0] = p[3]

    def p_class_stmt_list(self, p):
        'class_stmt_list : opt_declarations opt_node_types_def function_defs'
        p[0] = p[1]
        p[0].append(p[2])
        p[0].extend(p[3])

    def p_opt_declarations(self, p):
        '''opt_declarations : declarations
                            | empty'''
        p[0] = p[1] or []

    def p_declarations(self, p):
        '''declarations : declaration
                        | declarations declaration'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1]
            p[0].append(p[2])

    def p_opt_node_types_def(self, p):
        '''opt_node_types_def : node_types_def
                              | empty'''
        p[0] = p[1] or []

    def p_node_types_def(self, p):
        'node_types_def : assignment_stmt NEWLINE'
        p[0] = p[1]

    def p_function_defs(self, p):
        '''function_defs : function_def
                         | function_defs function_def'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1]
            p[0].append(p[2])

    def p_error(self, p):
        'Handle parsing errors.'
        # TODO: more robust error handling here
        if p:
            print 'Syntax error at', str(p)
        else:
            print 'Syntax error at EOF'


def main(args):
    # Parse a file containing Gramola code and print the result
    if not len(args):
        print >> sys.stderr, 'ERROR: Must provide the parser with a filename!'
        sys.exit(1)

    filename = args[0]
    parser = Parser()
    with open(filename, 'r') as fd:
        result = parser.parse(fd.read())

    pprint.pprint(result)


if __name__ == '__main__':
    main(sys.argv[1:])

