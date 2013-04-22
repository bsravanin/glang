#!/usr/bin/python2.7

"Initializes a SymbolTable with Gramola's builtin types, methods and functions."

import symbols as sym


# TODO: include special functions like __len__, then replace top-level builtins
# with those calls? Also, subscriptions, operators.

SYMBOL_TABLE = sym.SymbolTable()

BASIC_TYPES = (

    sym.TypeSymbol(((), 'bool')),
    sym.TypeSymbol(((), 'int')),
    sym.TypeSymbol(((), 'float')),
    # String
    sym.TypeSymbol(((), 'str')),
    # ArrayList<E>
    sym.TypeSymbol(((), 'list')),
    # HashSet<E>
    sym.TypeSymbol(((), 'set')),
    # HashMap<K,V>
    sym.TypeSymbol(((), 'dict')),
    sym.TypeSymbol(((), 'Graph')),
    sym.TypeSymbol(((), 'Node')),
    sym.TypeSymbol(((), 'Edge')),

    )

SYMBOL_TABLE.set_all(BASIC_TYPES)

SET_TYPE = SYMBOL_TABLE.get('set')
assert SET_TYPE is not None

DERIVED_TYPES = (

    sym.TypeSymbol(((), 'NodeSet'), base=SET_TYPE),
    sym.TypeSymbol(((), 'EdgeSet'), base=SET_TYPE),

)

SYMBOL_TABLE.set_all(DERIVED_TYPES)

# TODO: fill in types for params, returns
BUILTIN_METHODS = (

    ## STRINGS ##
    # String.clone
    sym.FunctionSymbol((('str',), 'copy')),
    # String.endsWith
    sym.FunctionSymbol((('str',), 'endswith')),
    # String.indexOf
    sym.FunctionSymbol((('str',), 'find')),
    # String.toLowerCase
    sym.FunctionSymbol((('str',), 'lower')),
    # String.replace
    sym.FunctionSymbol((('str',), 'replace')),
    # String.lastIndexOf
    sym.FunctionSymbol((('str',), 'rfind')),
    # String.split
    sym.FunctionSymbol((('str',), 'split')),
    # String.startswith
    sym.FunctionSymbol((('str',), 'startswith')),
    # String.trim
    sym.FunctionSymbol((('str',), 'strip')),
    # String.substring
    sym.FunctionSymbol((('str',), 'substring')),
    # String.toUpperCase
    sym.FunctionSymbol((('str',), 'upper')),

    ## LISTS ##
    # ArrayList<E>.add
    sym.FunctionSymbol((('list',), 'append')),
    # ArrayList<E>.clear
    sym.FunctionSymbol((('list',), 'clear')),
    # ArrayList<E>.clone
    sym.FunctionSymbol((('list',), 'copy')),
    # ArrayList<E>.addAll
    sym.FunctionSymbol((('list',), 'extend')),
    # ArrayList<E>.indexOf
    sym.FunctionSymbol((('list',), 'index')),
    # ArrayList<E>.add
    sym.FunctionSymbol((('list',), 'insert')),
    # ArrayList<E>.remove
    sym.FunctionSymbol((('list',), 'pop')),
    # ArrayList<E>.remove
    sym.FunctionSymbol((('list',), 'remove')),
    # Collections.reverse
    sym.FunctionSymbol((('list',), 'reverse')),
    # Collections.sort
    sym.FunctionSymbol((('list',), 'sort')),

    ## SETS ##
    # HashSet<E>.add
    sym.FunctionSymbol((('set',), 'add')),
    # HashSet<E>.clear
    sym.FunctionSymbol((('set',), 'clear')),
    # HashSet<E>.clone
    sym.FunctionSymbol((('set',), 'copy')),
    # HashSet<E>.retainAll
    sym.FunctionSymbol((('set',), 'intersection_update')),
    # HashSet<E>.remove
    sym.FunctionSymbol((('set',), 'remove')),
    # HashSet<E>.addAll
    sym.FunctionSymbol((('set',), 'update')),

    ## DICTS ##
    # HashMap<K,V>.clear
    sym.FunctionSymbol((('dict',), 'clear')),
    # HashMap<K,V>.clone
    sym.FunctionSymbol((('dict',), 'copy')),
    # HashMap<K,V>.get
    sym.FunctionSymbol((('dict',), 'get')),
    # HashMap<K,V>.containsKey
    sym.FunctionSymbol((('dict',), 'has_key')),
    # HashMap<K,V>.entrySet
    sym.FunctionSymbol((('dict',), 'items')),
    # HashMap<K,V>.keySet
    sym.FunctionSymbol((('dict',), 'keys')),
    # HashMap<K,V>.remove
    sym.FunctionSymbol((('dict',), 'pop')),
    # HashMap<K,V>.putAll
    sym.FunctionSymbol((('dict',), 'update')),
    # HashMap<K,V>.values
    sym.FunctionSymbol((('dict',), 'values')),

    ## GRAPHS ##

    ## NODES ##
    sym.FunctionSymbol((('Node',), 'in_nodes')),
    sym.FunctionSymbol((('Node',), 'out_nodes')),
    sym.FunctionSymbol((('Node',), 'in_edges')),
    sym.FunctionSymbol((('Node',), 'out_edges')),
    sym.FunctionSymbol((('Node',), 'shortest_path')),
    sym.FunctionSymbol((('Node',), 'paths')),

    ## EDGES ##
    sym.FunctionSymbol((('Edge',), 'get_attribute_set')),

    ## NODE SETS ##
    sym.FunctionSymbol((('NodeSet',), 'in_edges')),
    sym.FunctionSymbol((('NodeSet',), 'out_edges')),
    sym.FunctionSymbol((('NodeSet',), 'filter')),
    sym.FunctionSymbol((('NodeSet',), 'sort')),
    sym.FunctionSymbol((('NodeSet',), 'group_by')),

    ## EDGE SETS ##
    sym.FunctionSymbol((('EdgeSet',), 'in_nodes')),
    sym.FunctionSymbol((('EdgeSet',), 'out_nodes')),
    sym.FunctionSymbol((('EdgeSet',), 'filter')),

    )

SYMBOL_TABLE.set_all(BUILTIN_METHODS)


BUILTIN_FUNCTIONS = (

    ## BUILT-IN FUNCTIONS ##
    sym.FunctionSymbol(((), 'len')),

)

SYMBOL_TABLE.set_all(BUILTIN_FUNCTIONS)
