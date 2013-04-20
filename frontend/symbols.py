#!/usr/bin/python

'Symbol table management for Gramola.'


class Error(Exception):
    'Generic error class for symbols.py.'


class UnknownSymbolError(Error):
    'Requested an entry for an unknown symbol.'

    def __init__(self, token, namespace):
        Error.__init__(
            self,
            'Attemped to fetch table entry for unknown symbol {0} '
            'using token {1} in namespace {2}'.format(
                token.value, token, namespace))


class PreexistingSymbolError(Error):
    'Attempted to add a symbol that already exists in the namespace.'

    def __init__(self, symbol_obj, token, namespace):
        Error.__init__(
            self,
            'Attempted to overwrite table entry {0} '
            'using token {1} in namespace {2}'.format(
                symbol_obj, token, namespace))


def _check_name_type(name):
    'Checks that the given identifier has the proper type.'
    if not isinstance(name, basestring):
        raise TypeError('Identifier must be an instance of basestring')


def _check_full_name_type(full_name):
    'Checks that the given qualified identifier has the proper type.'
    if type(full_name) != tuple:
        raise TypeError('Fully qualified identifier must be of type tuple')


def _check_symbol_type(symbol):
    'Checks that the given symbol has the proper type.'
    if not isinstance(symbol, Symbol):
        raise TypeError('SymbolTable value must be an instance of Symbol')


class Symbol(object):
    'Representation of a symbol table entry.'

    def __init__(self, full_name, token):
        '''Constructor for a Symbol instance.

        Args:
          full_name: A (namespace, identifier) tuple representing the fully
              qualified name of the symbol. 'namespace' is itself a tuple of
              scope identifiers.
          token: A lex.LexToken instance.
        '''
        self._full_name = full_name
        self._token = token

    def __str__(self):
        return '<{0}: {1}>'.format(
            self.__class__.__name__,
            ', '.join('{0}={1}'.format(x, y)
                      for x, y in self.__dict__.iteritems()))

    @property
    def name(self):
        'Getter for name field.'
        return self._full_name

    @property
    def token(self):
        'Getter for token field.'
        return self._token


class TypeSymbol(Symbol):
    'Simple subclass of Symbol, for primitive data types and classes.'

    def __init__(self, full_name, token, base=None):
        '''Constructor for TypeSymbol.

        Args:
          full_name: see Symbol.
          token: see Symbol.
          base: (str) Base class for this type.
        '''
        Symbol.__init__(self, full_name, token)
        self.base = base


class IdSymbol(Symbol):
    'Simple subclass of Symbol, for identifiers.'

    def __init__(self, full_name, token, sym_type=None):
        '''Constructor for IdSymbol.

        Args:
          full_name: see Symbol.
          token: see Symbol.
          sym_type: (str) Type for the identifier represented by this object.
        '''
        Symbol.__init__(self, full_name, token)
        self.type = sym_type


class FunctionSymbol(Symbol):
    'Simple subclass of Symbol, for function identifiers.'

    def __init__(self, full_name, token, return_type=None, param_types=None):
        '''Constructor for FunctionSymbol.

        Args:
          full_name: see Symbol.
          token: see Symbol.
          return_type: (str or None) Return type for the function represented
              by this object.
          param_types: (list of str, or None) Types for this function's
              parameters.
        '''
        Symbol.__init__(self, full_name, token)
        self.return_type = return_type
        self.param_types = param_types


def _get_qualified_name(scopes, name):
    '''Returns the given identifier, qualified with the given namespace.

    Args:
      scopes: An iterable of scope identifiers (str), i.e., a namespace.
      name: (str) An identifier to qualify.

    Returns:
      A tuple of:
        tuple of identifiers (str)
        identifier (str)
    '''
    return (tuple(scopes), name)


class SymbolTable(object):
    '''Representation of a symbol table.

    The table is keyed on (namespace, identifier), where "namespace" is a
    single-level tuple representing the top-down path through program scopes
    (i.e., a scope stack state).
    '''

    def __init__(self, scopes=None):
        self._table = {}
        self._scopes = ScopeStack(scopes=scopes)

    def __contains__(self, arg):
        return self.get(arg)

    @property
    def scope_stack(self):
        '''Getter for the table's ScopeStack.

        Note that the returned stack is still modifiable via its public methods.
        '''
        return self._scopes

    def get_qualified_name(self, name):
        '''Returns the given identifier, qualified with the current namespace.

        Args:
          name: (str) An identifier to qualify.

        Returns:
          A tuple of:
              tuple of identifiers (str)
              identifier (str)
        '''
        return _get_qualified_name(self._scopes, name)

    def get(self, identifier):
        '''Looks up an (unqualified) identifier in the symbol table.

        Args:
          identifier: (basestring)

        Returns:
          A tuple (namespace (tuple), entry (Symbol)), if an entry exists for
          the given identifier at some scoping level -- namely, the 'namespace'
          level. Otherwise, a tuple ((), None).

        Raises:
          TypeError: If 'identifier' is not of type basestring.
        '''
        _check_name_type(identifier)
        cur_scopes = list(self._scopes)
        value = None
        while cur_scopes:
            full_name = _get_qualified_name(cur_scopes, identifier)
            value = self.get_by_qualified_name(full_name)
            if value:
                break
            cur_scopes.pop()
        return cur_scopes, value

    def get_in_current_scope(self, identifier):
        '''Returns the entry in the current scope for the given identifier.

        Args:
          identifier: (str) An identifier to qualify.

        Returns:
          If an entry exists for the given qualified identifier, an instance of
          Symbol. Otherwise, None.
        '''
        full_name = self.get_qualified_name(identifier)
        return self.get_by_qualified_name(full_name)

    def get_by_qualified_name(self, full_name):
        '''Looks up a qualified identifier in the symbol table.

        Args:
          full_name: A (namespace, identifier) tuple. 'namespace' must be a
              tuple of basestring, and 'identifier' must be a basestring.

        Returns:
          If an entry exists for the given qualified identifier, an instance of
          Symbol. Otherwise, None.

        Raises:
          TypeError: If 'full_name' is not of type tuple.
        '''
        _check_full_name_type(full_name)
        return self._table.get(full_name)

    def set(self, identifier, symbol):
        '''Sets the symbol table value for the given (unqualified) identifier.

        Args:
          identifier: (basestring)
          symbol: (Symbol)

        Raises:
          TypeError: If 'identifier' is not of type basestring, or 'symbol' is
          not an instance of 'Symbol'.
        '''
        _check_name_type(identifier)
        full_name = self.get_qualified_name(identifier)
        self.set_by_qualified_name(full_name, symbol)

    def set_by_qualified_name(self, full_name, symbol):
        '''Sets the symbol table value for the given qualified identifier.

        Args:
          full_name: A (namespace, identifier) tuple. 'namespace' must be a
              tuple of basestring, and 'identifier' must be a basestring.
          symbol: An instance of Symbol.

        Raises:
          TypeError: If 'full_name' is not of type tuple, or 'symbol' is
          not an instance of 'Symbol'.
        '''
        _check_full_name_type(full_name)
        _check_symbol_type(symbol)
        self._table[full_name] = symbol


class ScopeStack(object):
    '''Representation of a stack of "scopes".

    A "scope" is simply some consistent identifier for program scope, which
    helps determine the appropriate identifier namespace.
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

    def push(self, arg):
        "Pushes 'arg' onto the stack."
        _check_name_type(arg)
        self._stack.append(arg)

    def pop(self):
        'Pops a scope identifier off the stack.'
        return self._stack.pop()
