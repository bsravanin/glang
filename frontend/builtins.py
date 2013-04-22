#!/usr/bin/python2.7

"Initializes a SymbolTable with Gramola's builtin types, methods and functions."

import symbols as sym


# TODO: include special functions like __len__, then replace top-level builtins
# with those calls? Also, subscriptions, operators.
# TODO: do we need a None type, i.e., an object with no value at all
# (not even bool)?

_OBJECT = sym.TypeSymbol(((), 'object'))
_VOID = sym.TypeSymbol(((), 'void'))
_BOOL = sym.TypeSymbol(((), 'bool'), base=_OBJECT.full_name)
_INT = sym.TypeSymbol(((), 'int'), base=_OBJECT.full_name)
_FLOAT = sym.TypeSymbol(((), 'float'), base=_OBJECT.full_name)
# Java: String
_STR = sym.TypeSymbol(((), 'str'), base=_OBJECT.full_name)
# Java: ArrayList<E>
_LIST = sym.TypeSymbol(((), 'list'), base=_OBJECT.full_name)
# HashSet<E>
_SET = sym.TypeSymbol(((), 'set'), base=_OBJECT.full_name)
# HashMap<K,V>
_DICT = sym.TypeSymbol(((), 'dict'), base=_OBJECT.full_name)
_GRAPH = sym.TypeSymbol(((), 'Graph'), base=_OBJECT.full_name)
_NODE = sym.TypeSymbol(((), 'Node'), base=_OBJECT.full_name)
_EDGE = sym.TypeSymbol(((), 'Edge'), base=_OBJECT.full_name)

BASIC_TYPES = (
    _OBJECT,
    _VOID,
    _BOOL,
    _INT,
    _FLOAT,
    _STR,
    _LIST,
    _SET,
    _DICT,
    _GRAPH,
    _NODE,
    _EDGE,
    )


_NODE_SET = sym.TypeSymbol(((), 'NodeSet'), base=_SET.full_name)
_EDGE_SET = sym.TypeSymbol(((), 'EdgeSet'), base=_SET.full_name)
_PATH = sym.TypeSymbol(((), 'Path'), base=_LIST.full_name)

DERIVED_TYPES = (
    _NODE_SET,
    _EDGE_SET,
    _PATH,
)


# TODO: fill in types for params, returns
BUILTIN_METHODS = (

    ## STRINGS ##
    # String.clone
    sym.FunctionSymbol((('str',), 'copy'),
                       return_type=_STR.full_name),
    # String.endsWith
    sym.FunctionSymbol((('str',), 'endswith'),
                       return_type=_BOOL.full_name,
                       param_types=(_STR.full_name,)),
    # String.indexOf
    sym.FunctionSymbol((('str',), 'find'),
                       return_type=_LIST.full_name,
                       param_types=(_INT.full_name,)),
    # String.toLowerCase
    sym.FunctionSymbol((('str',), 'lower'),
                       return_type=_STR.full_name),
    # String.replace
    sym.FunctionSymbol((('str',), 'replace'),
                       return_type=_STR.full_name,
                       param_types=(_STR.full_name, _STR.full_name)),
    # String.lastIndexOf
    sym.FunctionSymbol((('str',), 'rfind'),
                       return_type=_INT.full_name,
                       param_types=(_STR.full_name,)),
    # String.split
    sym.FunctionSymbol((('str',), 'split'),
                       return_type=_LIST.full_name,
                       param_types=(_STR.full_name,)),
    # String.startswith
    sym.FunctionSymbol((('str',), 'startswith'),
                       return_type=_BOOL.full_name,
                       param_types=(_STR.full_name,)),
    # String.trim
    sym.FunctionSymbol((('str',), 'strip'),
                       return_type=_STR.full_name),
    # String.substring
    sym.FunctionSymbol((('str',), 'substring'),
                       return_type=_STR.full_name,
                       param_types=(_INT.full_name, _INT.full_name)),
    # String.toUpperCase
    sym.FunctionSymbol((('str',), 'upper'),
                       return_type=_STR.full_name),

    ## LISTS ##
    # ArrayList<E>.add
    sym.FunctionSymbol((('list',), 'append'),
                       return_type=_BOOL.full_name,
                       param_types=(_OBJECT.full_name,)),
    # ArrayList<E>.clear
    sym.FunctionSymbol((('list',), 'clear'),
                       return_type=_VOID.full_name),
    # ArrayList<E>.clone
    sym.FunctionSymbol((('list',), 'copy'),
                       return_type=_LIST.full_name),
    # ArrayList<E>.addAll
    sym.FunctionSymbol((('list',), 'extend'),
                       return_type=_BOOL.full_name,
                       param_types=(_LIST.full_name,)),
    # ArrayList<E>.indexOf
    sym.FunctionSymbol((('list',), 'index'),
                       return_type=_INT.full_name,
                       param_types=(_OBJECT.full_name,)),
    # ArrayList<E>.add
    sym.FunctionSymbol((('list',), 'insert'),
                       return_type=_VOID.full_name,
                       param_types=(_INT.full_name, _OBJECT.full_name)),
    # ArrayList<E>.remove
    sym.FunctionSymbol((('list',), 'pop'),
                       return_type=_OBJECT.full_name,
                       param_types=(_INT.full_name,)),
    # ArrayList<E>.remove
    sym.FunctionSymbol((('list',), 'remove'),
                       return_type=_BOOL.full_name,
                       param_types=(_OBJECT.full_name,)),
    # Collections.reverse
    sym.FunctionSymbol((('list',), 'reverse'),
                       return_type=_VOID.full_name),
    # Collections.sort
    sym.FunctionSymbol((('list',), 'sort'),
                       return_type=_VOID.full_name),

    ## SETS ##
    # HashSet<E>.add
    sym.FunctionSymbol((('set',), 'add'),
                       return_type=_BOOL.full_name,
                       param_types=(_OBJECT.full_name,)),
    # HashSet<E>.clear
    sym.FunctionSymbol((('set',), 'clear'),
                       return_type=_VOID.full_name),
    # HashSet<E>.clone
    sym.FunctionSymbol((('set',), 'copy'),
                       return_type=_SET.full_name),
    # HashSet<E>.retainAll
    sym.FunctionSymbol((('set',), 'intersection_update'),
                       return_type=_BOOL.full_name,
                       param_types=(_SET.full_name,)),
    # HashSet<E>.remove
    sym.FunctionSymbol((('set',), 'remove'),
                       return_type=_BOOL.full_name,
                       param_types=(_OBJECT.full_name,)),
    # HashSet<E>.addAll
    sym.FunctionSymbol((('set',), 'update'),
                       return_type=_BOOL.full_name,
                       param_types=(_SET.full_name,)),

    ## DICTS ##
    # HashMap<K,V>.clear
    sym.FunctionSymbol((('dict',), 'clear'),
                       return_type=_BOOL.full_name),
    # HashMap<K,V>.clone
    sym.FunctionSymbol((('dict',), 'copy'),
                       return_type=_DICT.full_name),
    # HashMap<K,V>.get
    sym.FunctionSymbol((('dict',), 'get'),
                       return_type=_OBJECT.full_name,
                       param_types=(_OBJECT.full_name,)),
    # HashMap<K,V>.containsKey
    sym.FunctionSymbol((('dict',), 'has_key'),
                       return_type=_BOOL.full_name,
                       param_types=(_OBJECT.full_name,)),
    # HashMap<K,V>.entrySet
    sym.FunctionSymbol((('dict',), 'items'),
                       return_type=_SET.full_name),
    # HashMap<K,V>.keySet
    sym.FunctionSymbol((('dict',), 'keys'),
                       return_type=_SET.full_name),
    # HashMap<K,V>.remove
    sym.FunctionSymbol((('dict',), 'pop'),
                       return_type=_OBJECT.full_name,
                       param_types=(_OBJECT.full_name,)),
    # HashMap<K,V>.putAll
    sym.FunctionSymbol((('dict',), 'update'),
                       return_type=_VOID.full_name,
                       param_types=(_DICT.full_name,)),
    # HashMap<K,V>.values
    sym.FunctionSymbol((('dict',), 'values'),
                       return_type=_SET.full_name),

    ## GRAPHS ##

    ## NODES ##
    sym.FunctionSymbol((('Node',), 'in_nodes'),
                       return_type=_NODE_SET.full_name),
    sym.FunctionSymbol((('Node',), 'out_nodes'),
                       return_type=_NODE_SET.full_name),
    sym.FunctionSymbol((('Node',), 'in_edges'),
                       return_type=_EDGE_SET.full_name),
    sym.FunctionSymbol((('Node',), 'out_edges'),
                       return_type=_EDGE_SET.full_name),
    sym.FunctionSymbol((('Node',), 'shortest_path'),
                       return_type=_PATH.full_name,
                       param_types=(_NODE.full_name,)),
    sym.FunctionSymbol((('Node',), 'paths'),
                       return_type=_PATH.full_name,
                       param_types=(_NODE.full_name,)),

    ## EDGES ##
    sym.FunctionSymbol((('Edge',), 'get_attribute_set'),
                       return_type=_SET.full_name),

    ## NODE SETS ##
    sym.FunctionSymbol((('NodeSet',), 'in_edges'),
                       return_type=_EDGE_SET.full_name),
    sym.FunctionSymbol((('NodeSet',), 'out_edges'),
                       return_type=_EDGE_SET.full_name),
    sym.FunctionSymbol((('NodeSet',), 'filter'),
                       return_type=_NODE_SET.full_name,
                       param_types=(_LIST.full_name)),
    sym.FunctionSymbol((('NodeSet',), 'sort'),
                       return_type=_LIST.full_name),
    # TODO: check this
    sym.FunctionSymbol((('NodeSet',), 'group_by'),
                       return_type=_DICT.full_name,
                       param_types=_LIST.full_name),

    ## EDGE SETS ##
    sym.FunctionSymbol((('EdgeSet',), 'in_nodes'),
                       return_type=_SET.full_name),
    sym.FunctionSymbol((('EdgeSet',), 'out_nodes'),
                       return_type=_SET.full_name),
    sym.FunctionSymbol((('EdgeSet',), 'filter'),
                       return_type=_EDGE_SET.full_name,
                       param_types=(_LIST.full_name)),

    )


BUILTIN_FUNCTIONS = (

    sym.FunctionSymbol(((), 'len'),
                       return_type=_INT.full_name,
                       param_types=(_OBJECT.full_name,)),

)


SYMBOL_TABLE = sym.SymbolTable()
SYMBOL_TABLE.set_all(BASIC_TYPES)
SYMBOL_TABLE.set_all(DERIVED_TYPES)
SYMBOL_TABLE.set_all(BUILTIN_METHODS)
SYMBOL_TABLE.set_all(BUILTIN_FUNCTIONS)
