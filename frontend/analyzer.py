#!/usr/bin/python2.7

'''Semantic analyzer for Gramola.

Presumes that the Parser has already been run on the given file, adding
declared classes, functions, and variables to the symbol table.
Resolves any unresolved symbols and runs semantic checks.
'''

import nodes
import os
import parser
import symbols
import sys

# pylint: disable=C0103
# "Invalid name"
# pylint: disable=C0111
# "Missing docstring"
# pylint: disable=R0201
# "Method could be a function


BUILTINS_FILENAME = os.path.join(os.path.curdir, 'builtins.gr')
CONSTRUCTOR_NAME = '__init__'


class Error(Exception):
    'Generic error class.'


class InconsistentTypeError(Error):
    'Types do not match as expected.'


class InconsistentElementTypeError(Error):
    'A sequence contains elements of different types.'


class InvalidTypeError(Error):
    'Type is invalid for the given context.'


class InvalidNameError(Error):
    'Name is invalid in the current context.'


class Analyzer(object):

    def __init__(self, tree, symbol_table):
        self._tree = tree
        self._symbol_table = symbol_table

    def analyze(self):
        self.dispatch(self._tree)

    def dispatch(self, tree):
        tree_class = tree.__class__.__name__
        if tree_class.endswith('Node'):
            meth = getattr(self, '_' + tree.__class__.__name__[:-4])
            meth(tree)
            return
        if isinstance(tree, list):
            for t in tree:
                self.dispatch(t)
            return

    def get_ancestor_types(self, full_name):
        types = [full_name]
        parent = full_name
        while True:
            parent = self.get_parent_type(parent)
            if parent is None:
                break
            types.append(parent)
        return types

    def get_parent_type(self, full_name):
        sym = self._symbol_table.get_by_qualified_name(full_name)
        return getattr(sym, 'base', None)

    def _Start(self, t):
        self.dispatch(t.stmt_list)

    def _FunctionDef(self, t):
        self.dispatch(t.name)
        sym = self._symbol_table.get_by_qualified_name(
            (t.name.namespace, t.name.value))
        if sym is None:
            raise symbols.UnknownSymbolError(
                'Function name {0} should already have been defined '
                'in namespace {1}. You have a problem.'.format(
                    t.name.value, t.name.namespace))

        # Fill in the return type, which we couldn't resolve during parsing
        self.dispatch(t.return_type)
        if getattr(t, 'method', False) and t.name.value == CONSTRUCTOR_NAME:
            # set constructor return type to the class
            class_name = t.name.namespace[-1]
            class_namespace = t.name.namespace[:-1]
            t.return_type = nodes.TypeNode(
                class_name, namespace=class_namespace)
            t.return_type.type = (class_namespace, class_name)
        sym.return_type = (t.return_type.namespace, t.return_type.value)

        # Ensure that param types are valid
        self.dispatch(t.params)
        # Fill in the param types, which we couldn't resolve during parsing
        sym.param_types = tuple(x.type for x in t.params)
        self.dispatch(t.body)
        # TODO: check that the return type matches the function declaration?

    def _Type(self, t):
        # Make sure this type exists in the symbol table
        # If this type is defined as part of a class definition, the namespace
        # in its symbol should match the namespace in its TypeNode.
        sym = self._symbol_table.get(t.value, namespace=t.namespace,
                                     symbol_type=symbols.TypeSymbol)
        if sym is None:
            raise symbols.UnknownSymbolError(t.value, t.namespace)
        # Now that we've resolved the type name, we can update some outdated
        # fields
        t.namespace = sym.namespace
        t.type = sym.full_name

    def _Name(self, t):
        if getattr(t, 'is_attribute', False):
            # This name is taking part in an attribute reference, and we don't
            # have the LHS of the dot here, so we check later
            return
        # Make sure this name exists in the symbol table
        sym = self._symbol_table.get(t.value, namespace=t.namespace)
        if sym is None:
            raise symbols.UnknownSymbolError(
                'Name {0} is unknown in namespace {1}'.format(
                    t.value, t.namespace))
        t.namespace = sym.namespace
        # Either this variable has already been declared, in which case its
        # symbol's var_type is set, or it's about to be set in a declaration.
        # In either case, this setting is okay.
        if type(sym) == symbols.VariableSymbol:
            t.type = sym.var_type

    def _Declaration(self, t):
        # Note: this is simply a type-name pair, not the full statement
        self.dispatch(t.var_type)
        self.dispatch(t.name)
        sym = self._symbol_table.get(t.name.value, namespace=t.name.namespace)
        # Set the type in this variable's symbol, now that we know it
        sym.var_type = t.type = t.name.type = t.var_type.type

    def _ClassDef(self, t):
        self.dispatch(t.name)
        if t.base:
            self.dispatch(t.base)
            # Set the base field in this type's symbol
            sym = self._symbol_table.get_by_qualified_name(
                (t.name.namespace, t.name.value))
            sym.base = t.base.type
        self.dispatch(t.body)

    def _ExpressionStmt(self, t):
        self.dispatch(t.expr)

    def _DeclarationStmt(self, t):
        self.dispatch(t.value)

    def _Assignment(self, t):
        self.dispatch(t.target)
        self.dispatch(t.value)
        if t.target.type != t.value.type:
            raise InconsistentTypeError(
                'Target type {0} does not match value type {1}'.format(
                    t.target.type, t.value.type))

    def _Print(self, t):
        for val in t.values:
            self.dispatch(val)

    def _Break(self, t):
        pass

    def _Continue(self, t):
        pass

    def _Return(self, t):
        if t.value:
            self.dispatch(t.value)

    def _If(self, t):
        self.dispatch(t.test)
        self.dispatch(t.body)
        for else_clause in t.elses:
            self.dispatch(else_clause)

    def _While(self, t):
        self.dispatch(t.test)
        self.dispatch(t.body)

    def _For(self, t):
        # "enhanced for" loop
        self.dispatch(t.target)
        self.dispatch(t.iterable)
        # check that t.iterable is of the correct type
        # TODO: either restrict for_primary to something whose type we always
        # know, e.g. name or enclosure, or don't check the type here
        if not (set(self.get_ancestor_types(t.iterable.type)) &
                set([((), 'list'), ((), 'set')])):
            raise InvalidTypeError(
                'Expected an iterable (list, set), found {0}'.format(
                    t.iterable.type))
        # NOTE: no longer ensuring consistent element types, so this check is
        # useless
        #if t.iterable.elts:
        #    if t.target.type != t.iterable.elt_type:
        #        raise InconsistentTypeError(
        #            'Target type ({0}) does not match '
        #            'iterable element type ({1})'.format(
        #                t.target.type, t.iterable.elt_type))
        self.dispatch(t.body)

    def _BinaryOp(self, t):
        # TODO: handle 'in' operator? (collection membership)
        op = t.operator
        self.dispatch(t.left)
        self.dispatch(t.right)
        # TODO: if op is boolean, left and right must be coerced to bool
        #       if op is a comparison, left and right must have number type
        #       if op is arithmetic, left and right must have number type, and
        #           must be coerced
        #       if op is 'in', right must be something on which we can call get()
        #       otherwise, error
        new_type = t.left.type
        t.type = new_type

    def _UnaryOp(self, t):
        op = t.operator
        self.dispatch(t.operand)
        # TODO: if op is boolean, operand must be coerced to bool
        #       if op is arithmetic, operand must be a number
        #       otherwise, error
        new_type = t.operand.type
        t.type = new_type

    def _String(self, t):
        t.type = ((), t.value.__class__.__name__)

    def _Number(self, t):
        t.type = ((), t.value.__class__.__name__)

    def _Paren(self, t):
        self.dispatch(t.expr)
        t.type = t.expr.type

    def _List(self, t):
        self.dispatch(t.elts)
        t.type = ((), 'list')
        if not len(t.elts):
            #t.elt_type = None
            return
        # NOTE: no longer enforcing consistent element types
        #types = set(x.type for x in t.elts)
        #if len(types) > 1:
        #    raise InconsistentElementTypeError(
        #        'List elements have multiple types ({0}): {1}'.format(
        #            types, t.elts))
        #t.elt_type = t.elts[0].type

    def _Dict(self, t):
        self.dispatch(t.items)
        t.type = ((), 'dict')
        if not len(t.items):
            #t.key_type = None
            return
        # NOTE: no longer enforcing consistent element types
        #types = set(key.type for key, value in t.items)
        #if len(types) > 1:
        #    raise InconsistentElementTypeError(
        #        'Dict keys have multiple types ({0}): {1}'.format(
        #            types, dict(t.items)))
        #t.key_type = t.items[0][0].type

    def _Set(self, t):
        assert t.elts  # t should contain at least one element
        self.dispatch(t.elts)
        t.type = ((), 'set')
        # NOTE: no longer enforcing consistent element types
        #types = set(x.type for x in t.elts)
        #if len(types) > 1:
        #    raise InconsistentElementTypeError(
        #        'Set elements have multiple types ({0}): {1}'.format(
        #            types, t.elts))
        #t.elt_type = t.elts[0].type

    def _AttributeRef(self, t):
        self.dispatch(t.value)
        self.dispatch(t.attribute)
        # check that t.attribute is an attribute of t.value
        namespace = symbols.flatten_full_name(t.value.type)
        attr_sym = self._symbol_table.get_by_qualified_name(
            (namespace, t.attribute.value))
        if attr_sym is None:
            raise symbols.UnknownSymbolError(
                '{0} is not an attribute of type {1}'.format(
                    t.attribute.value, t.value.type))
        t.attribute.namespace = namespace
        if attr_sym.__class__.__name__ == 'FunctionSymbol':
            # if the attribute isn't a VariableSymbol or TypeSymbol,
            # type means nothing
            new_type = None
        else:
            new_type = t.attribute.type
        t.type = new_type

    def _Subscript(self, t):
        self.dispatch(t.value)
        # Can we actually index into t.value?
        if ((), 'list') not in self.get_ancestor_types(t.type):
            raise InvalidTypeError(
                'Type {0} is not subscriptable -- only type list'.format(
                    t.type))
        self.dispatch(t.index)
        # Is the index actually an integer?
        if ((), 'int') not in self.get_ancestor_types(t.index.type):
            raise InvalidTypeError(
                'Invalid subscript type {0} for index {1}'.format(
                    t.index.type, t.index))
        # An iterable can contain elements of any type
        t.type = ((), 'object')

    def _Call(self, t):
        self.dispatch(t.func)
        # Is t.func actually a name?
        func_node_type = t.func.__class__.__name__
        if func_node_type == 'AttributeRefNode':
            name_node = t.func.attribute
        elif func_node_type in 'NameNode':
            name_node = t.func
        else:
            raise InvalidNameError('Cannot call a {0}'.format(func_node_type))

        # Is this name actually callable?
        # Also, if t.func is a type, then this is a constructor call
        func_sym = self._symbol_table.get(
            name_node.value, namespace=name_node.namespace)
        func_sym_class = func_sym.__class__.__name__
        if func_sym_class == 'TypeSymbol':
            type_sym = func_sym
            t.constructor = True
        elif func_sym_class != 'FunctionSymbol':
            raise InvalidNameError('Cannot call a {0}'.format(func_sym_class))

        self.dispatch(t.args)
        # check that arg types match param_types in function symbol
        if t.constructor:
            func_sym = self._symbol_table.get_by_qualified_name(
                (symbols.flatten_full_name(func_sym.full_name),
                 CONSTRUCTOR_NAME))
            t.type = type_sym.full_name
        else:
            t.type = func_sym.return_type
        for param_type, arg in zip(func_sym.param_types, t.args):
            if param_type not in self.get_ancestor_types(arg.type):
                raise InconsistentTypeError(
                    'Expected type {0} for function argument {1}, '
                    'found {2}'.format(param_type, arg, arg.type))


def analyze(ast, symbol_table):
    a = Analyzer(ast, symbol_table)
    a.analyze()


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

    p = parser.Parser()
    # Populate symbol table with built-ins
    builtin_ast = p.parse_file(BUILTINS_FILENAME, debug=debug)
    # Resolve built-in names, run checks
    analyze(builtin_ast, p.symbol_table)
    ast = p.parse_file(filename)
    # Resolve names in the given file, run checks
    analyze(ast, p.symbol_table)

    if prettify:
        print nodes.prettify(ast)
    else:
        print str(ast)

    if print_symbol_table:
        print p.symbol_table


if __name__ == '__main__':
    main(sys.argv[1:])
