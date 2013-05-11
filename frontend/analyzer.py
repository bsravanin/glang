#!/usr/bin/python2.7

'''Semantic analyzer for Gramola.

Important public attributes:
  analyze_file: Initializes and runs a Parser and Analyzer on the given filename

Usage:
  ast, symbol_table = analyze_file('my_file.gr', debug=False)
'''

import nodes
import os
import parser
import symbols
import sys
import util

# pylint: disable=C0103
# "Invalid name"
# pylint: disable=C0111
# "Missing docstring"
# pylint: disable=R0201
# "Method could be a function
# pylint: disable=R0903
# "Too few public methods"


class Error(Exception):
    'Generic error class.'


class InconsistentTypeError(Error):
    'Types do not match as expected.'


class InvalidNameError(Error):
    'Name is invalid in the current context.'


class InvalidTypeError(Error):
    'Type is invalid in the given context.'


class ParameterCountError(Error):
    'Incorrect number of function parameters.'


class Analyzer(object):
    '''Representation of a semantic analyzer.

    Presumes that the Parser has already been run on the given file, adding
    declared classes, functions, and variables to the symbol table.
    Resolves any unresolved symbols and runs semantic checks.
    Adds some auxiliary helper fields to the AST node instances, and may
    propagate them up the tree, e.g., 'type'.

    Important public attributes:
      analyze: Method that performs AST analysis and completes the symbol table.
    '''

    def __init__(self, tree, symbol_table):
        self._tree = tree
        self._symbol_table = symbol_table

    def analyze(self):
        self._dispatch(self._tree)

    def _dispatch(self, tree):
        tree_class = tree.__class__.__name__
        if tree_class.endswith('Node'):
            meth = getattr(self, '_' + tree.__class__.__name__[:-4])
            return meth(tree)
        if isinstance(tree, list):
            alist = []
            for t in tree:
                alist.append(self._dispatch(t))
            return alist

    def _get_ancestor_types(self, full_name):
        types = [full_name]
        parent = full_name
        while True:
            parent = self._get_parent_type(parent)
            if parent is None:
                break
            types.append(parent)
        return types

    def _get_parent_type(self, full_name):
        sym = self._symbol_table.get_by_qualified_name(full_name)
        return getattr(sym, 'base', None)

    def _resolve_attribute(self, start_type, attr):
        ancestor_types = self._get_ancestor_types(start_type)
        for atype in ancestor_types:
            namespace = symbols.flatten_full_name(atype)
            attr_sym = self._symbol_table.get_by_qualified_name(
                (namespace, attr))
            if attr_sym is not None:
                return attr_sym
        return None

    def _Start(self, t):
        self._dispatch(t.stmt_list)

    def _get_return_types(self, t):
        return_types = []
        if isinstance(t, list):
            for x in t:
                return_types.extend(self._get_return_types(x))
            return return_types

        if t.__class__.__name__ == 'ReturnNode':
            return_types.append(t.type)
            return return_types

        for x in getattr(t, '__dict__', []):
            attr = getattr(t, x)
            return_types.extend(self._get_return_types(attr))

        return return_types

    def _FunctionDef(self, t):
        self._dispatch(t.name)

        # TODO: remove this, since __init__'s now return the proper type
        # If this is a constructor, set its return type to its class name
        #if (getattr(t, 'is_method', False) and
        #    t.name.value == util.CONSTRUCTOR_NAME):
        #    class_name = t.name.namespace[-1]
        #    class_namespace = t.name.namespace[:-1]
        #    # A bit of a hack: if this is a parameterized type, we assume
        #    # the first function param will tell us the type parameter
        #    first_type_params = t.params[0].var_type.params
        #    t.return_type = nodes.TypeNode(
        #        class_name, namespace=class_namespace,
        #        params=first_type_params)
        #    t.return_type.lineno = t.lineno
        # Update the symbol table entry to match
        sym = self._symbol_table.get_by_qualified_name(
            (t.name.namespace, t.name.value))
        self._dispatch(t.return_type)
        sym.return_type = (t.return_type.namespace, t.return_type.value)

        self._dispatch(t.params)
        self._dispatch(t.body)

        # Check that the return types matches the function declaration.
        # Look for return statement(s) in 'body'.
        return_types = self._get_return_types(t.body)
        if not (return_types or sym.return_type == ((), 'void') or
                t.name.value == util.CONSTRUCTOR_NAME):
            raise InconsistentTypeError(
                '{0}: found no return type(s) for function {1}'.format(
                    t.lineno, symbols.stringify_full_name(sym.full_name)))
        for return_type in return_types:
            ancestor_types = self._get_ancestor_types(return_type)
            if sym.return_type not in ancestor_types:
                raise InconsistentTypeError(
                    '{0}: expected return type {1} in definition of '
                    'function {2}, found return type {3}'.format(
                        t.lineno,
                        symbols.stringify_full_name(sym.return_type),
                        t.name.value,
                        symbols.stringify_full_name(return_type)))

    def _Type(self, t):
        sym = self._symbol_table.get(t.value, namespace=t.namespace,
                                     symbol_type=symbols.TypeSymbol)
        # Now that we've resolved this type symbol, we can update the namespace
        # and type for it and any type parameters
        t.namespace = sym.namespace
        t.type = sym.full_name
        self._dispatch(t.params)
        expected_param_count = util.COLLECTION_BASE_TYPES.get(t.type)
        if expected_param_count and expected_param_count != len(t.params):
            raise InvalidTypeError(
                '{0}: expected {1} parameter(s) for type {2}, '
                'found {3}'.format(
                    t.lineno, expected_param_count,
                    symbols.stringify_full_name(t.type), len(t.params)))
        for param in t.params:
            param_sym = self._symbol_table.get(
                param.value, namespace=param.namespace,
                symbol_type=symbols.TypeSymbol)
            param.namespace = param_sym.namespace
            param.type = param_sym.full_name

    def _Name(self, t):
        if getattr(t, 'is_attribute', False):
            # This name is taking part in an attribute reference, and we don't
            # have the LHS of the dot here, so we check later
            return
        sym = self._symbol_table.get(t.value, namespace=t.namespace)
        if sym is None:
            raise symbols.UnknownSymbolError(
                '{0}: Could not resolve symbol name {1!r} '
                'within namespace {2!r}'.format(
                    t.lineno, t.value, symbols.stringify_tuple(t.namespace)))
        # Now that we've resolved this type symbol, we can update this node's
        # namespace
        t.namespace = sym.namespace
        # Either this variable has already been declared, in which case its
        # symbol's var_type is set, or it's about to be set in a declaration.
        # In either case, this setting is okay.
        if type(sym) == symbols.VariableSymbol:
            t.type = sym.var_type

    def _Declaration(self, t):
        # Note: this is simply a type-name pair, not the full statement
        self._dispatch(t.var_type)
        self._dispatch(t.name)
        # Make sure the AST node types are consistent
        t.type = t.name.type = t.var_type.type

    def _ClassDef(self, t):
        self._dispatch(t.name)
        if t.base:
            self._dispatch(t.base)
        self._dispatch(t.body)
        for stmt in t.body:
            if (stmt.__class__.__name__ == 'FunctionDefNode' and
                stmt.name.value == util.CONSTRUCTOR_NAME and
                stmt.return_type.type != t.name.type):
                raise InconsistentTypeError(
                    '{0}: constructor return type {1} does not match '
                    'class name {2}'.format(
                        t.lineno,
                        symbols.stringify_full_name(stmt.return_type.type),
                        symbols.stringify_full_name(t.name.type)))

    def _ExpressionStmt(self, t):
        self._dispatch(t.expr)

    def _DeclarationStmt(self, t):
        self._dispatch(t.value)

    def _Assignment(self, t):
        self._dispatch(t.target)
        self._dispatch(t.value)
        ancestor_types = self._get_ancestor_types(t.value.type)
        if t.target.type not in ancestor_types:
            raise InconsistentTypeError(
                '{2}: Target type {0} not compatible with '
                'value type {1}'.format(
                    symbols.stringify_full_name(t.target.type),
                    symbols.stringify_full_name(t.value.type), t.target.lineno))

    def _Print(self, t):
        for val in t.values:
            self._dispatch(val)

    def _Break(self, t):
        pass

    def _Continue(self, t):
        pass

    def _Return(self, t):
        if t.value:
            self._dispatch(t.value)
            t.type = t.value.type
        else:
            t.type = ((), 'void')

    def _If(self, t):
        self._dispatch(t.test)
        self._dispatch(t.body)
        for else_clause in t.elses:
            self._dispatch(else_clause)

    def _While(self, t):
        self._dispatch(t.test)
        self._dispatch(t.body)

    def _For(self, t):
        # "enhanced for" loop
        self._dispatch(t.target)
        self._dispatch(t.iterable)
        # Check that t.iterable is an instance of list or set
        if not (set(self._get_ancestor_types(t.iterable.type)) &
                set([((), 'list'), ((), 'set')])):
            raise InvalidTypeError(
                '{1}: expected an iterable (list, set), found {0}'.format(
                    symbols.stringify_full_name(t.iterable.type), t.lineno))
        # At compile time, we don't know what element types are in t.iterable,
        # unless it's a manually constructed list
        for item in getattr(t.iterable, 'elts', []):
            ancestor_types = self._get_ancestor_types(item.type)
            if t.target.type not in ancestor_types:
                raise InconsistentTypeError(
                    '{0}: expected type {1}, found type {2}'.format(
                        item.lineno, symbols.stringify_full_name(t.target.type),
                        symbols.stringify_full_name(item.type)))
        self._dispatch(t.body)

    def _BinaryOp(self, t):
        self._dispatch(t.left)
        self._dispatch(t.right)

        boolean_ops = ('or', 'and')
        comparison_ops = ('<', '>', '<=', '>=', '==', '!=', 'is')
        arithmetic_ops = ('+', '-', '*', '/', '%')
        bool_sym = self._symbol_table.get(
            'bool', symbol_type=symbols.TypeSymbol)
        bool_type = bool_sym.full_name
        int_type = self._symbol_table.get(
            'int', symbol_type=symbols.TypeSymbol).full_name
        float_sym = self._symbol_table.get(
            'float', symbol_type=symbols.TypeSymbol)
        float_type = float_sym.full_name
        str_type = self._symbol_table.get(
            'str', symbol_type=symbols.TypeSymbol).full_name
        numeric_types = set([int_type, float_type])
        op = t.operator
        if op in boolean_ops:
            t.type = bool_type
            # Coerce each side to bool if numeric or string
            bool_node = nodes.NameNode(bool_sym.name, bool_sym.namespace)
            if t.left.type in (int_type, float_type, str_type):
                new_node = nodes.CallNode(func=bool_node, args=[t.left],
                                          is_constructor=True)
                new_node.type = bool_type
                t.left = new_node
            if t.right.type in (int_type, float_type, str_type):
                new_node = nodes.CallNode(func=bool_node, args=[t.right],
                                          is_constructor=True)
                new_node.type = bool_type
                t.right = new_node
        elif op in comparison_ops:
            t.type = bool_type
            if (op not in ('==', '!=', 'is') and
                not (t.left.type in numeric_types and
                     t.right.type in numeric_types)):
                raise InvalidTypeError(
                    '{0}: either {1} or {2} types cannot take part in an '
                    'arithmetic operation'.format(
                        t.lineno,
                        symbols.stringify_full_name(t.left.type),
                        symbols.stringify_full_name(t.right.type)))
        elif op in arithmetic_ops:
            if not (t.left.type in numeric_types and
                    t.right.type in numeric_types):
                raise InvalidTypeError(
                    '{0}: either {1} or {2} types cannot take part in an '
                    'arithmetic operation'.format(
                        t.lineno,
                        symbols.stringify_full_name(t.left.type),
                        symbols.stringify_full_name(t.right.type)))
            if t.left.type != t.right.type:
                t.type = float_type
                # Coerce int to float (we only have 2 numeric types)
                float_node = nodes.NameNode(float_sym.name, float_sym.namespace)
                if t.left.type == int_type:
                    new_node = nodes.CallNode(func=float_node, args=[t.left],
                                              is_constructor=True)
                    new_node.type = float_type
                    t.left = new_node
                else:
                    new_node = nodes.CallNode(func=float_node, args=[t.right],
                                              is_constructor=True)
                    new_node.type = float_type
                    t.right = new_node
            else:
                t.type = t.left.type
        else:
            raise Error('{1}: Unknown binary operation: {0}'.format(
                    op, t.lineno))

    def _UnaryOp(self, t):
        self._dispatch(t.operand)

        boolean_ops = ('not',)
        arithmetic_ops = ('+', '-')
        bool_sym = self._symbol_table.get(
            'bool', symbol_type=symbols.TypeSymbol)
        bool_type = bool_sym.full_name
        int_type = self._symbol_table.get(
            'int', symbol_type=symbols.TypeSymbol).full_name
        float_sym = self._symbol_table.get(
            'float', symbol_type=symbols.TypeSymbol)
        float_type = float_sym.full_name
        str_type = self._symbol_table.get(
            'str', symbol_type=symbols.TypeSymbol).full_name
        numeric_types = set([int_type, float_type])
        op = t.operator
        if op in boolean_ops:
            t.type = bool_type
            # Coerce operand to bool if numeric or string
            bool_node = nodes.NameNode(bool_sym.name, bool_sym.namespace)
            if t.operand.type in (int_type, float_type, str_type):
                new_node = nodes.CallNode(func=bool_node, args=[t.operand],
                                          is_constructor=True)
                new_node.type = bool_type
                t.operand = new_node
        elif op in arithmetic_ops:
            if t.operand.type not in numeric_types:
                raise InvalidTypeError(
                    '{0}: {1} type cannot take part in an '
                    'arithmetic operation'.format(
                        t.lineno,
                        symbols.stringify_full_name(t.operand.type)))
            t.type = t.operand.type
        else:
            raise Error('{1}: Unknown unary operation: {0}'.format(
                    op, t.lineno))

    def _String(self, t):
        #t.type = ((), t.value.__class__.__name__)
        t.type = self._symbol_table.get(
            t.value.__class__.__name__,
            symbol_type=symbols.TypeSymbol).full_name

    def _Number(self, t):
        #t.type = ((), t.value.__class__.__name__)
        t.type = self._symbol_table.get(
            t.value.__class__.__name__,
            symbol_type=symbols.TypeSymbol).full_name

    def _Paren(self, t):
        self._dispatch(t.expr)
        t.type = t.expr.type

    def _List(self, t):
        self._dispatch(t.elts)
        t.type = ((), 'list')

    def _Dict(self, t):
        self._dispatch(t.items)
        t.type = ((), 'dict')

    def _Set(self, t):
        assert t.elts  # t should contain at least one element
        self._dispatch(t.elts)
        t.type = ((), 'set')

    def _AttributeRef(self, t):
        self._dispatch(t.value)
        self._dispatch(t.attribute)
        # check that t.attribute is actually an attribute of t.value
        attr_sym = self._resolve_attribute(t.value.type, t.attribute.value)
        if attr_sym is None:
            raise symbols.UnknownSymbolError(
                '{2}: {0} is not an attribute of type {1} or any of its '
                'ancestors'.format(
                    t.attribute.value,
                    symbols.stringify_full_name(t.value.type), t.lineno))

        # We skipped setting the attribute's namespace and type in _Name() so
        # that we could set it here
        t.attribute.namespace = attr_sym.namespace
        if attr_sym.__class__.__name__ == 'FunctionSymbol':
            # If the attribute isn't a VariableSymbol or TypeSymbol,
            # type means nothing
            t.attribute.type = None
        else:
            t.attribute.type = attr_sym.var_type
        t.type = t.attribute.type

    def _Subscript(self, t):
        self._dispatch(t.value)
        # Check that we can actually index into t.value
        if ((), 'list') not in self._get_ancestor_types(t.value):
            raise InvalidTypeError(
                '{1}: Type {0} is not subscriptable -- only type list'.format(
                    symbols.stringify_full_name(t.value), t.lineno))
        self._dispatch(t.index)
        # Check that the index is actually an integer
        if ((), 'int') not in self._get_ancestor_types(t.index.type):
            raise InvalidTypeError(
                '{2}: Invalid subscript type {0} for index {1}'.format(
                    symbols.stringify_full_name(t.index.type),
                    t.index, t.lineno))
        # An iterable can contain elements of any type
        t.type = ((), 'object')

    def _Call(self, t):
        self._dispatch(t.func)
        # Check that t.func is actually a name
        func_node_class = t.func.__class__.__name__
        is_attribute = False
        if func_node_class == 'AttributeRefNode':
            is_attribute = True
            name_node = t.func.attribute
        elif func_node_class in ('NameNode', 'TypeNode'):
            name_node = t.func
        else:
            raise InvalidNameError('{1}: Cannot call a {0}'.format(
                    func_node_class, t.lineno))

        # Check that this name is actually callable
        # Also, if t.func is a type, then this is a constructor call
        func_sym = self._symbol_table.get(
            name_node.value, namespace=name_node.namespace)
        func_sym_class = func_sym.__class__.__name__
        if func_sym_class == 'TypeSymbol':
            t.is_constructor = True
        elif func_sym_class != 'FunctionSymbol':
            raise InvalidNameError(
                '{1}: Cannot call an instance of {0}'.format(
                    func_sym_class, t.lineno))

        self._dispatch(t.args)

        if t.is_constructor:
            type_sym = func_sym
            # Use the class's constructor method symbol instead
            func_sym = self._resolve_attribute(
                type_sym.full_name,
                util.CONSTRUCTOR_NAME)
            t.type = type_sym.full_name
            # Replace NameNode with TypeNode for the type being constructed
            if func_node_class == 'NameNode':
                new_node = nodes.TypeNode(
                    type_sym.name, namespace=type_sym.namespace)
                new_node.type = type_sym.full_name
                new_node.lineno = t.lineno
                if is_attribute:
                    t.func.attribute = new_node
                else:
                    t.func = new_node
            if func_sym is None:
                # There's no init method to check, so we're done here
                return
        else:
            t.type = func_sym.return_type


        # Check that arg types match param_types in function symbol
        if len(func_sym.param_types) != len(t.args):
            raise ParameterCountError(
                '{0}: expected {1} argument(s) for function {2}, '
                'found {3}'.format(
                    t.lineno, len(func_sym.param_types),
                    symbols.stringify_full_name(func_sym.full_name),
                    len(t.args)))
        for i, (param_type, arg) in enumerate(
            zip(func_sym.param_types, t.args)):
            if param_type not in self._get_ancestor_types(arg.type):
                raise InconsistentTypeError(
                    '{3}: expected type {0} for function argument {1}, '
                    'found {2}'.format(
                        symbols.stringify_full_name(param_type), i + 1,
                        symbols.stringify_full_name(arg.type),
                        t.lineno))


def _analyze(ast, symbol_table):
    a = Analyzer(ast, symbol_table)
    a.analyze()


def analyze_file(filename, debug=False):
    p = parser.Parser()
    # Populate symbol table with built-ins
    builtin_ast = p.parse_file(util.BUILTINS_FILENAME, debug=debug)
    # Resolve built-in names, run checks
    _analyze(builtin_ast, p.symbol_table)

    if os.path.abspath(filename) == util.BUILTINS_FILENAME:
        return builtin_ast, p.symbol_table

    ast = p.parse_file(filename)
    # Resolve names in the given file, run checks
    _analyze(ast, p.symbol_table)
    return ast, p.symbol_table


def main(args):
    if not len(args):
        print >> sys.stderr, 'ERROR: Must provide the analyzer with a filename!'
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
    ast, symtab = analyze_file(filename, debug=debug)

    if prettify:
        print nodes.prettify(ast)
    else:
        print str(ast)

    if print_symbol_table:
        print
        print
        print '***** SYMBOL TABLE *****'
        print symtab


if __name__ == '__main__':
    main(sys.argv[1:])
