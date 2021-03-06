#!/usr/bin/python2.7

'Symbol table management for Gramola.'

import sys
import util

# For creating prettier namespace strings
NAMESPACE_SEP = '.'


class Error(Exception):
    'Generic error class for symbols.py.'


class UnknownSymbolError(Error):
    'Requested an entry for an unknown symbol.'


class ConflictingSymbolError(Error):
    'Attempted to add a symbol that already exists in the namespace.'

    def __init__(self, symbol_obj, namespace, lineno):
        Error.__init__(
            self,
            '{0}: Attempted to overwrite table entry {1} '
            'in namespace {2}'.format(lineno, symbol_obj, namespace))


def _validate_full_name(full_name):
    'Checks that the fully qualified name is well-formed.'
    if type(full_name) != tuple:
        raise TypeError('Fully qualified name must be a tuple: '
                        + repr(full_name))
    if len(full_name) != 2:
        raise ValueError('Fully qualified name must be a 2-tuple: '
                         + repr(full_name))
    _validate_namespace(full_name[0])
    _validate_name(full_name[1])


def _validate_name(name):
    'Checks that the given name is well-formed.'
    if not isinstance(name, basestring):
        raise TypeError('Name must be a basestring: '
                        + repr(name))
    if not name:
        raise ValueError('Name cannot be an empty string')


def _validate_namespace(namespace):
    'Checks that the given qualified name is well-formed.'
    if type(namespace) != tuple:
        raise TypeError('Namespace must be of type tuple: '
                        + repr(namespace))
    for name in namespace:
        _validate_name(name)


def _validate_symbol(symbol):
    'Checks that the given symbol is well-formed.'
    if not isinstance(symbol, Symbol):
        raise TypeError('SymbolTable value must be a Symbol: '
                        + repr(symbol))


def get_qualified_name(namespace, name):
    '''Returns the given name, qualified with the given namespace.

    Args:
      namespace: A tuple of identifier strings.
      name: An identifier string.

    Returns:
      A tuple of:
        tuple of names (str)
        name (str)
    '''
    if isinstance(namespace, ScopeStack) or '__iter__' in dir(namespace):
        namespace = tuple(namespace)
    _validate_namespace(namespace)
    _validate_name(name)
    return (namespace, name)


def flatten_full_name(full_name):
    'Flattens the given fully qualified name.'
    _validate_full_name(full_name)
    return full_name[0] + (full_name[1],)


def stringify_full_name(full_name):
    'Returns a stringified version of the given qualified name.'
    return stringify_tuple(flatten_full_name(full_name))


def stringify_tuple(tup):
    'Returns a stringified version of the given tuple.'
    return NAMESPACE_SEP.join(tup)


class Symbol(object):
    'Representation of a symbol table entry.'

    def __init__(self, full_name, token=None):
        '''Constructor for a Symbol instance.

        Args:
          full_name: A (namespace, name) tuple.
          token: A lex.LexToken instance, or None.
        '''
        _validate_full_name(full_name)
        namespace, name = full_name
        self._namespace = namespace
        self._name = name
        self._full_name = full_name
        self._token = token

    def __str__(self):
        attrs = dict((attr, getattr(self, attr))
                      for attr in dir(self) if not attr.startswith('_'))
        for attr in ('name', 'namespace'):
            del attrs[attr]
        fields = []
        for attr in ('full_name', 'token'):
            fields.append('{0}={1!r}'.format(attr, attrs[attr]))
            del attrs[attr]
        fields.extend('{0}={1!r}'.format(x, y) for x, y in attrs.iteritems())
        return '<{0}: {1}>'.format(self.__class__.__name__, ', '.join(fields))

    @property
    def namespace(self):
        'Getter for the symbol "namespace".'
        return self._namespace

    @property
    def name(self):
        'Getter for the unqualified symbol name.'
        return self._name

    @property
    def full_name(self):
        'Getter for the fully qualified symbol name.'
        return self._full_name

    @property
    def token(self):
        'Getter for the token that yielded this Symbol.'
        return self._token


class TypeSymbol(Symbol):
    'Simple subclass of Symbol, for primitive data types and classes.'

    def __init__(self, full_name, token=None, base=None):
        '''Constructor for TypeSymbol.

        Args:
          full_name: A (namespace, name) tuple.
          token: see Symbol.
          base: A (namespace, name) tuple representing the base class for this
              type, or None.
        '''
        Symbol.__init__(self, full_name, token=token)
        if base is not None:
            _validate_full_name(base)
        self.base = base


class VariableSymbol(Symbol):
    'Simple subclass of Symbol, for variable names.'

    def __init__(self, full_name, token=None, var_type=None,
                 var_type_params=None):
        '''Constructor for VariableSymbol.

        Args:
          full_name: A (namespace, name) tuple.
          token: see Symbol.
          var_type: A (namespace, name) tuple representing the fully qualified
              type for this variable.
          var_type_params: An iterable of (namespace, name) tuples representing
              parameters for this variable's type, or None.
        '''
        Symbol.__init__(self, full_name, token=token)
        _validate_full_name(var_type)
        self.var_type = var_type
        params = var_type_params or ()
        for param in params:
            _validate_full_name(param)
        self.var_type_params = tuple(params)


class FunctionSymbol(Symbol):
    'Simple subclass of Symbol, for function names.'

    def __init__(self, full_name, token=None, return_type=None,
                 param_types=None):
        '''Constructor for FunctionSymbol.

        Args:
          full_name: A (namespace, name) tuple.
          token: see Symbol.
          return_type: A (namespace, name) tuple representing the return type
              of this function, or None.
          param_types: An iterable of (namespace, name) tuples representing the
              parameter types of this function, or None.
        '''
        Symbol.__init__(self, full_name, token=token)
        if return_type is not None:
            _validate_full_name(return_type)
        self.return_type = return_type
        if param_types is None:
            param_types = []
        for param_type in param_types:
            _validate_full_name(param_type)
        self.param_types = tuple(param_types)


class SymbolTable(object):
    '''Representation of a symbol table.

    The table is keyed on (namespace, name), where "namespace" is a
    single-level tuple representing the top-down path through program scopes
    (i.e., a scope stack state).
    '''

    def __init__(self, table=None, scopes=None):
        self._table = {}
        if table is not None:
            self.update(table)
        self._scopes = ScopeStack(scopes=scopes)

    def __contains__(self, arg):
        return self.get(arg)

    def __str__(self):
        items = [(stringify_full_name(x), y) for x, y in self._table.items()]
        items.sort()
        vals = []
        for name, sym in items:
            vals.append('({0!r}, {1})'.format(name, sym))
        return '\n'.join(vals)

    def as_dict(self):
        'Return the dict that backs this SymbolTable.'
        return self._table

    def reset(self, table=None, scopes=None):
        'Resets this SymbolTable.'
        self.__init__(table=table, scopes=scopes)

    def update(self, table):
        'Updates this SymbolTable with the given SymbolTable.'
        if isinstance(table, SymbolTable):
            table = table.as_dict()
        if not isinstance(table, dict):
            raise TypeError("Parameter 'table' must be a SymbolTable or dict")
        self._table.update(table)

    @property
    def scope_stack(self):
        '''Getter for the table's ScopeStack.

        Note that the returned stack is still modifiable via its public methods.
        '''
        return self._scopes

    def get_qualified_name(self, name):
        '''Returns the given name, qualified with the current namespace.

        Args:
          name: (str) An name to qualify.

        Returns:
          A tuple of:
              tuple of names (str)
              name (str)
        '''
        return get_qualified_name(self._scopes, name)

    def get(self, name, namespace=None, symbol_type=Symbol):
        '''Looks up an (unqualified) name in the symbol table.

        Args:
          name: (basestring)
          namespace: A tuple of scope identifiers (str), or None. If present,
              the symbol search begins in that namespace and works its way up.
              If None, we start at the current namespace stored in this table.
          symbol_type: A Symbol (sub)class type to filter the search.

        Returns:
          A Symbol, if an entry exists for the given name at some scoping level.
          Otherwise, None.

        Raises:
          TypeError: If 'name' is not of type basestring.
        '''
        _validate_name(name)
        namespace = namespace or self._scopes
        cur_scopes = list(namespace)
        value = None
        while cur_scopes:
            full_name = get_qualified_name(cur_scopes, name)
            value = self.get_by_qualified_name(full_name)
            if value and isinstance(value, symbol_type):
                break
            cur_scopes.pop()
        else:
            full_name = get_qualified_name(cur_scopes, name)
            value = self.get_by_qualified_name(full_name)
        if value is None:
            full_name = get_qualified_name((util.BUILTINS_CLASS_NAME,), name)
            value = self.get_by_qualified_name(full_name)
        return value

    def get_in_current_scope(self, name):
        '''Returns the entry in the current scope for the given name.

        Args:
          name: (str) An name to qualify.

        Returns:
          If an entry exists for the given qualified name, an instance of
          Symbol. Otherwise, None.
        '''
        full_name = self.get_qualified_name(name)
        return self.get_by_qualified_name(full_name)

    def get_by_qualified_name(self, full_name):
        '''Looks up a qualified name in the symbol table.

        Args:
          full_name: A (namespace, name) tuple.

        Returns:
          If an entry exists for the given qualified name, an instance of
          Symbol. Otherwise, None.

        Raises:
          TypeError: If 'full_name' is not of type tuple.
        '''
        _validate_full_name(full_name)
        return self._table.get(full_name)

    def set(self, symbol):
        '''Sets and entry for the given symbol.

        The key for the given symbol consists of its namespace and name, which
        have already been validated.

        Args:
          symbol: (Symbol)

        Raises:
          TypeError: If 'symbol' is not a valid symbol.
        '''
        _validate_symbol(symbol)
        self._table[symbol.full_name] = symbol

    def set_all(self, symbols):
        'Set symbol table entries for all of the given symbols.'
        errors = []
        for sym in symbols:
            try:
                self.set(sym)
            except TypeError, e:
                errors.append(sym)
                print >> sys.stderr, 'TypeError: {0}. Skipping.'.format(e)
                continue
        return errors


class ScopeStack(object):
    '''Representation of a stack of "scopes".

    A "scope" is simply some consistent name for program scope, which
    helps determine the appropriate namespace.
    '''

    def __init__(self, scopes=None):
        if scopes is None:
            scopes = []
        self._stack = list(scopes)

    def __iter__(self):
        return iter(self._stack)

    def __str__(self):
        return str(self._stack)

    def __repr__(self):
        return 'ScopeStack(stack={!r})'.format(self._stack)

    def push(self, name):
        "Pushes 'name' onto the stack."
        _validate_name(name)
        self._stack.append(name)

    def pop(self):
        'Pops a scope name off the stack.'
        return self._stack.pop()
