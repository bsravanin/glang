#!/usr/bin/python2.7

'''Parser for Gramola.

NB: by convention, whenever the grammar calls for an optional rule,
we create a separate method "opt_RULENAME" that matches either that
rule, or "empty".
'''

# pylint: disable=C0103
# "Invalid name"
# pylint: disable=R0201
# "Method could be a function"
# pylint: disable=R0904
# "Too many public methods" (for Parser class)

import nodes
import symbols
import sys
from ply import yacc
from lexer import Lexer


class Error(Exception):
    'Generic error class for parser.py.'


class ParsingError(Error):
    'An error occurred during parsing.'

    def __init__(self, arg):
        Error.__init__(self, 'A syntax error occurred at: ' + arg)


class Parser(object):
    '''Representation of a parser object.

    Important public attributes:
      parse: Parses the given input, returns a nodes.Node instance representing
          the abstract syntax tree (AST) for the input.
      parse_file: Same as parse(), but on an input filename.
      reset: Resets the state of the parser, its lexer, and its symbol table.
    '''

    def __init__(self, lexer=None):
        self._lexer = lexer or Lexer()
        self._symbol_table = symbols.SymbolTable()
        self._cur_scope_name = None

        self.tokens = self._lexer.tokens
        self.start = 'start'
        self._parser = yacc.yacc(module=self)
        # We only needed these attributes to initialize Yacc, so we can delete
        # them now
        del self.tokens
        del self.start

    @property
    def _cur_namespace(self):
        'Getter for the current namespace.'
        return tuple(self._symbol_table.scope_stack)

    def _get_qualified_name(self, name):
        'Returns the given identifier, qualified by its namespace.'
        return self._symbol_table.get_qualified_name(name)

    def parse(self, s, **kwargs):
        'Parses the given string of text.'
        lexer = kwargs.pop('lexer', self._lexer)
        return self._parser.parse(s, lexer=lexer, **kwargs)

    def parse_file(self, filename, **kwargs):
        'Parses the string of text in the given named file.'
        with open(filename, 'r') as infile:
            s = infile.read()
        return self.parse(s, **kwargs)

    def reset(self):
        '''Resets the state and SymbolTable for this Parser.

        Calling parse() will indirectly reset the states of the parser and
        lexer, but this does a pre-emptive reset, and it's the only way to
        reset the symbol table.
        '''
        self._parser.restart()
        self._lexer.reset()
        self._symbol_table.reset()

    @property
    def symbol_table(self):
        "Getter for this Parser's symbol table."
        return self._symbol_table

    def _push_scope(self):
        'Pushes a new identifier onto the scope stack.'
        self._symbol_table.scope_stack.push(self._cur_scope_name)

    def _pop_scope(self):
        'Pops an identifier off the scope stack.'
        self._symbol_table.scope_stack.pop()
        namespace = self._cur_namespace
        if namespace:
            self._cur_scope_name = namespace[-1]
        else:
            self._cur_scope_name = None

    ## HELPER RULES ##
    def p_empty(self, p):
        'empty :'
        pass

    def p_new_scope(self, p):
        'new_scope :'
        p[0] = None
        self._push_scope()

    def p_error(self, p):
        'Handle parsing errors.'
        # TODO: more robust error handling here
        if p:
            raise SyntaxError(str(p))
        else:
            raise SyntaxError('EOF')

    ## TOP LEVEL ##
    def p_start(self, p):
        'start : opt_top_level_stmt_list ENDMARKER'
        p[0] = nodes.StartNode(stmt_list=p[1])

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
        '''top_level_stmt : class_stmt
                          | class_def'''
        p[0] = p[1]

    ## FUNCTION DEFINITIONS ##
    def p_function_def(self, p):
        ('function_def : DEF type new_func_name new_scope '
         'LPAREN opt_parameter_list RPAREN COLON suite')
        p[0] = nodes.FunctionDefNode(return_type=p[2], name=p[3], params=p[6],
                                     body=p[9])
        p[0].lineno = p.slice[1].lineno
        self._pop_scope()

    def p_type(self, p):
        'type : NAME'
        # We verify validity of this type in a later pass. For all we know, it
        # could be defined further on in the parsing pass.
        p[0] = nodes.TypeNode(value=p[1], namespace=self._cur_namespace)
        p[0].lineno = p.slice[1].lineno

    def p_new_func_name(self, p):
        'new_func_name : NAME'
        name_token = p.slice[1]
        name = name_token.value
        p[0] = nodes.NameNode(value=name, namespace=self._cur_namespace)
        p[0].lineno = p.slice[1].lineno
        self._cur_scope_name = name

        # Add this new function name to the symbol table, as long as it doesn't
        # already exist in the current scope
        sym = self._symbol_table.get(name)
        if sym is None:
            full_name = self._get_qualified_name(name)
            # We set/check types for this function symbol in a later pass,
            # since we may not know about its types yet.
            symbol = symbols.FunctionSymbol(full_name, token=name_token)
            self._symbol_table.set(symbol)
        elif sym.namespace == self._cur_namespace:
            raise symbols.ConflictingSymbolError(
                sym, name_token, self._cur_namespace)

    def p_opt_parameter_list(self, p):
        '''opt_parameter_list : parameter_list
                              | empty'''
        p[0] = p[1] or []

    def p_parameter_list(self, p):
        '''parameter_list : declaration
                          | parameter_list COMMA declaration'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1]
            p[0].append(p[3])

    def p_declaration(self, p):
        'declaration : type new_var_name'
        # Set the type in the names' symbols in a later pass, since we may not
        # know about this type yet.
        p[0] = nodes.DeclarationNode(var_type=p[1], name=p[2])
        p[0].lineno = p[1].lineno

    def p_new_var_name(self, p):
        'new_var_name : NAME'
        name_token = p.slice[1]
        name = name_token.value
        p[0] = nodes.NameNode(value=name, namespace=self._cur_namespace)
        p[0].lineno = p.slice[1].lineno

        sym = self._symbol_table.get(name)
        if sym is None:
            full_name = self._get_qualified_name(name)
            symbol = symbols.VariableSymbol(full_name, token=name_token)
            self._symbol_table.set(symbol)
        elif sym.namespace == self._cur_namespace:
            raise symbols.ConflictingSymbolError(
                sym, name_token, self._cur_namespace)

    def p_suite(self, p):
        'suite : NEWLINE INDENT stmt_list DEDENT'
        p[0] = p[3]

    def p_stmt_list(self, p):
        '''stmt_list : stmt
                     | stmt_list stmt'''
        if len(p) == 2:
            # If stmt is 'pass', p[1] is None
            p[0] = [p[1]] if p[1] else []
        else:
            p[0] = p[1]
            p[0].append(p[2])

    ## CLASS DEFINITIONS ##
    def p_class_def(self, p):
        ('class_def : CLASS new_type new_scope '
         'LPAREN opt_type RPAREN COLON class_def_suite')
        p[0] = nodes.ClassDefNode(name=p[2], base=p[5], body=p[8])
        p[0].lineno = p.slice[1].lineno

        # For each method in this new class, add "self" within its namespace
        class_parent_scope = self._cur_namespace[:-1]
        full_class_name = (class_parent_scope, self._cur_scope_name)
        for stmt in p[8]:
            if type(stmt) == nodes.FunctionDefNode:
                func_name = stmt.name.value
                func_namespace, func_name = self._get_qualified_name(func_name)
                sym = symbols.VariableSymbol(
                    (func_namespace + (func_name,), 'self'),
                    var_type=full_class_name)
                self._symbol_table.set(sym)
                # Also, tag it as a method
                stmt.is_method = True
        self._pop_scope()

    def p_new_type(self, p):
        'new_type : NAME'
        name_token = p.slice[1]
        name = name_token.value
        p[0] = nodes.TypeNode(value=name, namespace=self._cur_namespace)
        p[0].lineno = p.slice[1].lineno
        self._cur_scope_name = name

        # Add this type to the symbol table as long as it doesn't already exist
        # in the current scope
        sym = self._symbol_table.get(name)
        if sym is None:
            full_name = self._get_qualified_name(name)
            symbol = symbols.TypeSymbol(full_name, token=name_token)
            self._symbol_table.set(symbol)
        elif sym.namespace == self._cur_namespace:
            raise symbols.ConflictingSymbolError(
                sym, name_token, self._cur_namespace)

    def p_opt_type(self, p):
        '''opt_type : type
                    | empty'''
        p[0] = p[1]

    def p_class_def_suite(self, p):
        'class_def_suite : NEWLINE INDENT class_stmt_list DEDENT'
        p[0] = p[3]

    def p_class_stmt_list(self, p):
        '''class_stmt_list : class_stmt
                           | class_stmt_list class_stmt'''
        if len(p) == 2:
            p[0] = [p[1]] if p[1] else []
        else:
            p[0] = p[1]
            p[0].append(p[2])

    def p_class_stmt(self, p):
        '''class_stmt : declaration_stmt
                      | assignment_stmt NEWLINE
                      | function_def
                      | pass_stmt NEWLINE'''
        p[0] = p[1]

    ## STATEMENTS ##
    def p_stmt(self, p):
        '''stmt : simple_stmt
                | compound_stmt'''
        p[0] = p[1]

    ## SIMPLE STATEMENTS ##
    def p_simple_stmt(self, p):
        '''simple_stmt : small_stmt NEWLINE
                       | expr_stmt
                       | declaration_stmt'''
        p[0] = p[1]

    def p_small_stmt(self, p):
        '''small_stmt : assignment_stmt
                      | print_stmt
                      | flow_stmt
                      | pass_stmt'''
        p[0] = p[1]

    def p_expr_stmt(self, p):
        'expr_stmt : expr NEWLINE'
        p[0] = nodes.ExpressionStmtNode(expr=p[1])
        p[0].lineno = p.slice[2].lineno

    def p_declaration_stmt(self, p):
        'declaration_stmt : declaration NEWLINE'
        p[0] = nodes.DeclarationStmtNode(value=p[1])
        p[0].lineno = p[1].lineno

    def p_assignment_stmt(self, p):
        'assignment_stmt : target ASSIGN expr'
        p[0] = nodes.AssignmentNode(target=p[1], value=p[3])
        p[0].lineno = p.slice[2].lineno

    def p_target(self, p):
        '''target : var_opt_type
                  | attribute_ref
                  | subscription'''
        p[0] = p[1]

    def p_var_opt_type(self, p):
        '''var_opt_type : declaration
                        | var_name'''
        p[0] = p[1]

    def p_var_name(self, p):
        'var_name : NAME'
        name = p.slice[1].value
        p[0] = nodes.NameNode(value=name, namespace=self._cur_namespace)
        p[0].lineno = p.slice[1].lineno

        sym = self._symbol_table.get(name)
        if sym is None:
            # While function names and class names can be used in a namespace
            # before they're declared, variable names cannot
            raise symbols.UnknownSymbolError(
                'Symbol {0} is known in in namespace {1}'.format(
                    name, self._cur_namespace))

    def p_print_stmt(self, p):
        'print_stmt : PRINT opt_expr_list'
        p[0] = nodes.PrintNode(values=p[2])
        p[0].lineno = p.slice[1].lineno

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
        p[0] = nodes.BreakNode()
        p[0].lineno = p.slice[1].lineno

    def p_continue_stmt(self, p):
        'continue_stmt : CONTINUE'
        p[0] = nodes.ContinueNode()
        p[0].lineno = p.slice[1].lineno

    def p_return_stmt(self, p):
        'return_stmt : RETURN opt_expr'
        p[0] = nodes.ReturnNode(value=p[2])
        p[0].lineno = p.slice[1].lineno

    def p_opt_expr(self, p):
        '''opt_expr : expr
                    | empty'''
        p[0] = p[1]

    def p_pass_stmt(self, p):
        'pass_stmt : PASS'
        # Do nothing

    ## COMPOUND STATEMENTS ##
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
        p[0] = nodes.IfNode(test=p[2], body=p[4], elses=elses)
        p[0].lineno = p.slice[1].lineno

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
            p[0] = [p[1]] if p[1] else []
        else:
            p[0] = p[1]
            p[0].append(p[2])

    def p_elif_clause(self, p):
        'elif_clause : ELIF expr COLON suite'
        p[0] = nodes.IfNode(test=p[2], body=p[4])
        p[0].lineno = p.slice[1].lineno

    def p_else_clause(self, p):
        'else_clause : ELSE COLON suite'
        p[0] = p[3]

    def p_while_stmt(self, p):
        'while_stmt : WHILE expr COLON suite'
        p[0] = nodes.WhileNode(test=p[2], body=p[4])
        p[0].lineno = p.slice[1].lineno

    def p_for_stmt(self, p):
        'for_stmt : for new_scope var_opt_type IN for_iterable COLON suite'
        p[0] = nodes.ForNode(target=p[3], iterable=p[5], body=p[7])
        p[0].lineno = p[3].lineno
        self._pop_scope()

    def p_for(self, p):
        'for : FOR'
        p[0] = p[1]
        self._cur_scope_name = 'for_{0}'.format(p.slice[1].lineno)

    def p_for_iterable(self, p):
        '''for_iterable : name
                        | attribute_ref
                        | subscription
                        | call
                        | enclosure'''
        p[0] = p[1]

    ## EXPRESSIONS ##
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
            p[0] = nodes.BinaryOpNode(operator='or', left=p[1], right=p[3])
        p[0].lineno = p[1].lineno

    def p_and_test(self, p):
        '''and_test : not_test
                    | and_test AND not_test'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = nodes.BinaryOpNode(operator='and', left=p[1], right=p[3])
        p[0].lineno = p[1].lineno

    def p_not_test(self, p):
        '''not_test : comparison
                    | NOT not_test'''
        if len(p) == 2:
            p[0] = p[1]
            p[0].lineno = p[1].lineno
        else:
            p[0] = nodes.UnaryOpNode(operator='not', operand=p[2])
            p[0].lineno = p[2].lineno

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
                p[0] = nodes.BinaryOpNode(operator=op, left=left, right=right)
            else:
                # Strip "not" from operator
                op = op[:max(not_loc - 1, 0)] + op[not_loc + 4:]
                operand = nodes.BinaryOpNode(operator=op, left=left,
                                             right=right)
                p[0] = nodes.UnaryOpNode(operator='not', operand=operand)
        p[0].lineno = p[1].lineno

    def p_comp_op(self, p):
        '''comp_op : LESS
                   | GREATER
                   | EQUAL
                   | LESSEQUAL
                   | GREATEREQUAL
                   | NOTEQUAL
                   | IS
                   | IS NOT'''
        p[0] = '_'.join(x.value for x in p.slice[1:])

    def p_arith_expr(self, p):
        '''arith_expr : mult_expr
                      | arith_expr arith_op mult_expr'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            # p[2] is a string, not a token
            p[0] = nodes.BinaryOpNode(operator=p[2], left=p[1], right=p[3])
        p[0].lineno = p[1].lineno

    def p_arith_op(self, p):
        '''arith_op : PLUS
                    | MINUS'''
        p[0] = p[1]

    def p_mult_expr(self, p):
        '''mult_expr : unary_expr
                     | mult_expr mult_op unary_expr'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            # p[2] is a string, not a token
            p[0] = nodes.BinaryOpNode(operator=p[2], left=p[1], right=p[3])
        p[0].lineno = p[1].lineno

    def p_mult_op(self, p):
        '''mult_op : STAR
                   | SLASH
                   | PERCENT'''
        p[0] = p[1]

    def p_unary_expr(self, p):
        '''unary_expr : primary
                      | unary_op unary_expr'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            # p[2] is a string, not a token
            p[0] = nodes.UnaryOpNode(operator=p[1], operand=p[2])
        p[0].lineno = p[1].lineno

    def p_unary_op(self, p):
        '''unary_op : PLUS
                    | MINUS'''
        p[0] = p[1]

    def p_primary(self, p):
        '''primary : atom
                   | attribute_ref
                   | subscription
                   | call'''
        # a primary can be:
        # - attribute-referenced
        # - subscripted
        # - called
        # - in an arithmetic expression
        # - a for-loop iterable
        p[0] = p[1]

    def p_atom(self, p):
        '''atom : name
                | string_list
                | number
                | enclosure'''
        p[0] = p[1]

    def p_name(self, p):
        'name : NAME'
        name_token = p.slice[1]
        name = name_token.value
        p[0] = nodes.NameNode(value=name, namespace=self._cur_namespace)
        p[0].lineno = p.slice[1].lineno

        # UPDATE: Resolve this name in a later pass, once it has been declared
        # Add this name to the symbol table if it doesn't already exist in the
        # current scope
        #sym = self._symbol_table.get(name)
        #if sym is None:
        #    full_name = self._get_qualified_name(name)
        #    # Using generic Symbol class because we don't know what kind of name
        #    # this is out of context (type? variable? function?). We can update
        #    # it to a Symbol subclass later once we know what it really is.
        #    symbol = symbols.Symbol(full_name, name_token)
        #    self._symbol_table.set(symbol)

    def p_string_list(self, p):
        '''string_list : STRING
                       | string_list STRING'''
        if len(p) == 2:
            p[0] = nodes.StringNode(value=p[1])
            p[0].lineno = p.slice[1].lineno
        else:
            p[0] = nodes.StringNode(value=p[1].value + p[2])
            p[0].lineno = p[1].lineno

    def p_number(self, p):
        'number : NUMBER'
        p[0] = nodes.NumberNode(value=p[1])
        p[0].lineno = p.slice[1].lineno

    def p_enclosure(self, p):
        '''enclosure : paren_expr
                     | list_maker
                     | dict_maker
                     | set_maker'''
        p[0] = p[1]

    def p_paren_expr(self, p):
        'paren_expr : LPAREN expr RPAREN'
        p[0] = nodes.ParenNode(expr=p[2])
        p[0].lineno = p.slice[1].lineno

    def p_list_maker(self, p):
        'list_maker : LBRACKET opt_expr_list RBRACKET'
        p[0] = nodes.ListNode(elts=p[2])
        p[0].lineno = p.slice[1].lineno

    def p_dict_maker(self, p):
        'dict_maker : LBRACE opt_key_datum_list RBRACE'
        p[0] = nodes.DictNode(items=p[2])
        p[0].lineno = p.slice[1].lineno

    def p_set_maker(self, p):
        'set_maker : LBRACE expr_list RBRACE'
        # Note: expr_list is not optional. Otherwise, we'd have empty braces,
        # which create an empty dict, not a set.
        p[0] = nodes.SetNode(elts=p[2])
        p[0].lineno = p.slice[1].lineno

    def p_opt_key_datum_list(self, p):
        '''opt_key_datum_list : key_datum_list
                              | empty'''
        p[0] = p[1] or []

    def p_key_datum_list(self, p):
        '''key_datum_list : key_datum
                          | key_datum_list COMMA key_datum'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1]
            p[0].append(p[3])

    def p_key_datum(self, p):
        'key_datum : expr COLON expr'
        p[0] = (p[1], p[3])

    def p_attribute_ref(self, p):
        'attribute_ref : ref_primary DOT name'
        p[3].is_attribute = True
        p[0] = nodes.AttributeRefNode(value=p[1], attribute=p[3])
        p[0].lineno = p.slice[2].lineno

    def p_ref_primary(self, p):
        '''ref_primary : name
                       | attribute_ref
                       | subscription
                       | call'''
        p[0] = p[1]

    def p_subscription(self, p):
        'subscription : sub_primary LBRACKET expr RBRACKET'
        p[0] = nodes.SubscriptNode(value=p[1], index=p[3])
        p[0].lineno = p.slice[2].lineno

    def p_sub_primary(self, p):
        '''sub_primary : name
                       | attribute_ref
                       | subscription'''
        p[0] = p[1]

    def p_call(self, p):
        'call : call_primary LPAREN opt_argument_list RPAREN'
        p[0] = nodes.CallNode(func=p[1], args=p[3])
        p[0].lineno = p.slice[2].lineno

    def p_call_primary(self, p):
        '''call_primary : name
                        | attribute_ref'''
        p[0] = p[1]

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


def main(args):
    'Parse a file containing Gramola code and print the result.'
    if not len(args):
        print >> sys.stderr, 'ERROR: Must provide the parser with a filename!'
        sys.exit(1)

    debug = False
    prettify = False
    print_symbol_table = False
    for arg in args[:]:
        if arg == '-d':
            debug = True
        elif arg == '-p':
            prettify = True
        elif arg == '-s':
            print_symbol_table = True
        if arg.startswith('-'):
            args.remove(arg)

    filename = args[0]
    p = Parser()
    ast = p.parse_file(filename, debug=debug)

    if prettify:
        print nodes.prettify(ast)
    else:
        print str(ast)

    if print_symbol_table:
        print p.symbol_table


if __name__ == '__main__':
    main(sys.argv[1:])

