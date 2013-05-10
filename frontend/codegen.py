#!/usr/bin/python2.7

'Code generator for Gramola.'

import analyzer
import os
import re
import symbols
import sys
import util

# pylint: disable=C0103
# "Invalid name"
# pylint: disable=C0111
# "Missing docstring"


JAVA_HEADER = os.path.join(os.path.curdir, 'header.txt')
TARGET_PROGRAM_NAME = 'Test'
JAVA_NAME_MAP = {
    'Edge.add_parents': 'addParents',
    'Edge.get_attribute': 'getVariableValue',
    'Edge.get_attribute_map': 'getVariableMap',
    'Edge.get_attributes': 'getVariables',
    'Edge.get_id': 'getId',
    'Edge.get_parents': 'getParents',
    'Edge.in_node': 'inV',
    'Edge.out_node': 'outV',
    'Edge.set_attribute': 'setVariableValue',
    'Edge.set_id': 'setId',
    'EdgeSet.filter': 'filter',
    'EdgeSet.out_nodes': 'outV',
    'Graph.add_edge': 'addEdge',
    'Graph.add_node': 'addNode',
    'Graph.edge': 'Edge',
    'Graph.get_all_edges': 'getAllEdges',
    'Graph.get_id': 'getGraphId',
    'Graph.get_node': 'getNode',
    'Graph.get_node_by_id': 'getNodeById',
    'Graph.get_all_nodes': 'getAllNodes',
    'Graph.get_nodes': 'getNodes',
    'Graph.get_paths': 'getPaths',
    'Graph.get_shortest_path': 'getShortestPath',
    'Graph.node': 'Node',
    'Node.get_attribute': 'getVariableValue',
    'Node.get_attribute_map': 'getVariableMap',
    'Node.get_attributes': 'getVariables',
    'Node.get_id': 'getId',
    'Node.in_edges': 'inE',
    'Node.in_neighbors': 'inNeighbors',
    'Node.out_edges': 'outE',
    'Node.out_neighbors': 'outNeighbors',
    'Node.set_attribute': 'setVariableValue',
    'Node.set_id': 'setId',
    'Node.set_in_edge': 'setInE',
    'Node.set_out_edge': 'setOutE',
    'Node.update': 'update',
    'NodeSet.filter': 'filter',
    'NodeSet.out_edges': 'outE',
    '__builtins.union': 'GraphUtil.union',
    '__builtins.draw': 'GraphUtil.draw',
    '__builtins.dump': 'GraphUtil.dump',
    '__builtins.len': 'GraphUtil.len',
    '__builtins.load': 'GraphUtil.load',
    '__builtins.get_fb': 'GraphUtil.getFB',
    '__builtins.get_fb_friend': 'GraphUtil.getFBFriend',
    '__builtins.get_fb_feed': 'GraphUtil.getFBFeed',
    '__builtins.get_fb_page': 'GraphUtil.getFBPage',
    'dict.copy': 'clone',
    'dict.get': 'get',
    'dict.has_key': 'containsKey',
    'dict.items': 'entrySet',
    'dict.keys': 'keySet',
    'dict.pop': 'remove',
    'dict.update': 'putAll',
    'dict.values': 'values',
    'list.append': 'add',
    'list.contains': 'contains',
    'list.copy': 'clone',
    'list.extend': 'addAll',
    'list.index': 'indexOf',
    'list.insert': 'add',
    'list.pop': 'remove',
    'list.remove': 'remove',
    # Ideally, we'd support these....
    #'list.reverse': 'Collections.reverse',
    #'list.sort': 'Collections.sort',
    'set.add': 'add',
    'set.contains': 'contains',
    'set.copy': 'clone',
    'set.difference_update': 'removeAll',
    'set.intersection_update': 'retainAll',
    'set.isempty': 'isEmpty',
    'set.issuperset': 'containsAll',
    'set.remove': 'remove',
    'set.update': 'addAll',
    'str.copy': 'clone',
    'str.endswith': 'endsWith',
    'str.find': 'indexOf',
    'str.lower': 'toLowerCase',
    'str.replace': 'replace',
    'str.rfind': 'lastIndexOf',
    'str.split': 'split',
    'str.startswith': 'startsWith',
    'str.strip': 'trim',
    'str.substring': 'substring',
    'str.upper': 'toUpperCase',
    }

TYPE_MAP = {
    'object': 'Object',
    'void': 'void',
    'int': 'Integer',
    'bool': 'Boolean',
    'float': 'Double',
    'str': 'String',
    'list': 'ArrayList<Object>',
    'set': 'HashSet',
    'dict': 'HashMap<Object, Object>',
    'Graph': 'Graph',
    'Node': 'Node',
    'Edge': 'Edge',
    'NodeSet': 'NodeSet',
    'EdgeSet': 'EdgeSet',
    'Path': 'Path',
    }


def convert_type(name):
    return TYPE_MAP.get(name, name)


def interleave(inter, f, seq):
    'Call f on each item in seq, calling inter() in between.'
    seq = iter(seq)
    try:
        f(next(seq))
    except StopIteration:
        pass
    else:
        for x in seq:
            inter()
            f(x)


class CodeGenerator(object):
    '''Methods in this class recursively traverse an AST and output translated
    source code for the abstract syntax; original formatting is disregarded.'''

    def __init__(self, tree, output=sys.stdout):
        'Constructor for CodeGenerator.'
        self.f = output
        self._indent = 0
        self.dispatch(tree)
        self.f.write('')
        self.f.flush()

    def fill(self, text=''):
        'Indent a piece of text, according to the current indentation level'
        self.f.write('\n' + '\t' * self._indent + text)

    def write(self, text):
        'Append a piece of text to the current line.'
        self.f.write(text)

    def enter(self):
        "Start a block with ' {' and increase the indentation level."
        self.write(' {')
        self._indent += 1

    def leave(self):
        "Decrease the indentation level and close the block with '}'."
        self._indent -= 1
        self.fill(text='}')

    def end_stmt(self):
        'Print a semicolon to end the statement.'
        self.write(';')

    def dispatch(self, tree):
        'Dispatcher function, dispatching tree type T to method _T.'
        tree_class = tree.__class__.__name__
        if tree_class.endswith('Node'):
            meth = getattr(self, '_' + tree.__class__.__name__[:-4])
            meth(tree)
            return
        if isinstance(tree, list):
            for t in tree:
                self.dispatch(t)
            return


    ############### Generation methods #####################
    # There should be one method per concrete grammar type #
    # Constructors should be grouped by sum type. Ideally, #
    # this would follow the order in the grammar, but      #
    # currently doesn't.                                   #
    ########################################################

    def _Start(self, t):
        # Import header
        with open(JAVA_HEADER, 'r') as infile:
            header = infile.read()
        class_defs = []
        other_stmts = []
        for stmt in t.stmt_list:
            if stmt.__class__.__name__ == 'ClassDefNode':
                class_defs.append(stmt)
            else:
                other_stmts.append(stmt)
        for stmt in class_defs:
            # Write a new .java file
            with open(stmt.name.value + '.java', 'w') as outfile:
                outfile.write(header)
                CodeGenerator(stmt, output=outfile)

        if not other_stmts:
            return

        self.write(header)
        self.fill('public class ' + TARGET_PROGRAM_NAME)
        self.enter()
        for stmt in other_stmts:
            if stmt.__class__.__name__ == 'FunctionDefNode':
                # static attributes in the main class
                self._FunctionDef(stmt, top=True)
            else:
                self.dispatch(stmt)
        self.fill()
        self.leave()
        self.fill()

    def _FunctionDef(self, t, top=False):
        self.write('\n')
        self.fill('public ')
        if top:
            self.write('static ')
        if t.name.value == 'main':
            self.write('void main(String[] args)')
        else:
            if (t.name.value == util.CONSTRUCTOR_NAME and
                getattr(t, 'is_method', False)):
                self.write(t.return_type.value)
            else:
                self.dispatch(t.return_type)
                self.write(' ')
                self.dispatch(t.name)
            self.write('(')
            interleave(lambda: self.write(', '), self.dispatch, t.params)
            self.write(')')
        self.enter()
        self.dispatch(t.body)
        self.leave()

    def _Type(self, t):
        self.write(convert_type(t.value))

    def _Name(self, t):
        value = t.value
        if value in ('False', 'True') and not getattr(t, 'is_attribute', False):
            value = value.lower()
        elif value == 'self':
            value = 'this'
        self.write(value)

    def _Declaration(self, t, class_level=False):
        # Note: this is simply a type-name pair, not the full statement
        if class_level:
            # Class-level variables must be public
            self.write('public ')
        self.dispatch(t.var_type)
        self.write(' ')
        self.dispatch(t.name)

    def _ClassDef(self, t):
        self.write('\n')
        self.fill('class ')
        self.dispatch(t.name)
        if t.base:
            self.write(' extends ')
            self.dispatch(t.base)
        self.enter()
        self.write('\n')
        for stmt in t.body:
            if stmt.__class__.__name__ == 'DeclarationStmtNode':
                self._DeclarationStmt(stmt, class_level=True)
            else:
                self.dispatch(stmt)
        self.leave()

    def _ExpressionStmt(self, t):
        self.fill()
        self.dispatch(t.expr)
        self.end_stmt()

    def _DeclarationStmt(self, t, class_level=False):
        self.fill()
        self._Declaration(t.value, class_level=class_level)
        self.end_stmt()

    def _Assignment(self, t):
        self.fill()
        self.dispatch(t.target)
        self.write(' = ')
        self.dispatch(t.value)
        self.end_stmt()

    def _Print(self, t):
        if not t.values:
            self.fill('System.out.println()')
            self.end_stmt()
        else:
            for e in t.values:
                self.fill('System.out.println(')
                if e.__class__.__name__ == 'StringNode':
                    self.dispatch(e)
                else:
                    self.write('(')
                    self.dispatch(e)
                    self.write(').toString()')
                self.write(')')
                self.end_stmt()

    def _Break(self, _):
        self.fill('break')
        self.end_stmt()

    def _Continue(self, _):
        self.fill('continue')
        self.end_stmt()

    def _Return(self, t):
        self.fill('return')
        if t.value:
            self.write(' ')
            self.dispatch(t.value)
        self.end_stmt()

    def _If(self, t, is_else=False):
        if is_else:
            self.write(' if (')
        else:
            self.fill('if (')
        self.dispatch(t.test)
        self.write(')')
        self.enter()
        self.dispatch(t.body)
        self.leave()
        for else_clause in t.elses:
            self.write(' else')
            if else_clause.__class__.__name__ == 'IfNode':
                self._If(else_clause, is_else=True)
            else:
                self.enter()
                self.dispatch(else_clause)
                self.leave()

    def _While(self, t):
        self.fill('while (')
        self.dispatch(t.test)
        self.write(')')
        self.enter()
        self.dispatch(t.body)
        self.leave()

    def _For(self, t):
        # "enhanced for" loop
        self.fill('for (')
        self.dispatch(t.target)
        self.write(' : ')
        self.dispatch(t.iterable)
        self.write(')')
        self.enter()
        self.dispatch(t.body)
        self.leave()

    def _BinaryOp(self, t):
        op = t.operator
        if op in ('==', '!='):
            # value equality
            if op == '!=':
                self.write('!')
            self.write('(')
            self.dispatch(t.left)
            self.write(').equals(')
            self.dispatch(t.right)
            self.write(')')
            return

        if op == 'is':
            # object equality
            op = '=='
        if op == 'and':
            op = '&&'
        elif op == 'or':
            op = '||'
        self.dispatch(t.left)
        self.write(' {0} '.format(op))
        self.dispatch(t.right)

    def _UnaryOp(self, t):
        op = t.operator
        if op == 'not':
            op = '!'
        self.write(op)
        # In case of unary minus, we need to parenthesize the operand.
        self.write('(')
        self.dispatch(t.operand)
        self.write(')')

    def _String(self, t):
        # Python allows multiple quote styles for strings, but other languages
        # (e.g. Java) require one. This normalizes to double-quotes.
        self.write('"{0}"'.format(re.sub('"', '\\"', eval(t.value))))

    def _Number(self, t):
        number_type = t.type[1]
        self.write('(({0}) {1})'.format(convert_type(number_type), repr(t.value)))

    def _Paren(self, t):
        self.write('(')
        self.dispatch(t.expr)
        self.write(')')

    def _List(self, t):
        self.write('(new {0}(Arrays.asList('.format(convert_type('list')))
        interleave(lambda: self.write(', '), self.dispatch, t.elts)
        self.write(')))')

    def _Dict(self, t):
        def write_pair(item):
            self.dispatch(item[0])
            self.write(', ')
            self.dispatch(item[1])

        self.write('GraphUtil.createVarMap(')
        interleave(lambda: self.write(', '), write_pair, t.items)
        self.write(')')

    def _Set(self, t):
        self.write('(new {0}(Arrays.asList('.format(convert_type('set')))
        interleave(lambda: self.write(', '), self.dispatch, t.elts)
        self.write(')))')

    def _AttributeRef(self, t):
        self.dispatch(t.value)
        self.write('.')
        self.dispatch(t.attribute)

    def _Subscript(self, t):
        self.dispatch(t.value)
        self.write('.get(')
        self.dispatch(t.index)
        self.write(')')

    def _Call(self, t):
        # Translate qualified function name to Java name
        # - type casting: special handling
        # - builtin function: prepend GraphUtil
        # - constructor: prepend "new "
        # - attribute ref: map attr (namespace, name) to Java attr

        func_name_node = getattr(t.func, 'attribute', t.func)
        func_full_name = symbols.stringify_full_name(
            (func_name_node.namespace, func_name_node.value))
        # Special handling for casting
        if func_full_name == 'bool':
            self.write('Boolean.valueOf(')
            self.write('(')
            self.dispatch(t.args[0])
            self.write(') != 0 ? "true" : "false"')
            self.write(')')
            return
        if func_full_name == 'str':
            self.write('String.valueOf(')
            self.dispatch(t.args[0])
            self.write(')')
            return
        if func_full_name == 'int':
            self.write('Integer.valueOf(')
            self.write('(')
            self.dispatch(t.args[0])
            self.write(').toString()')
            self.write(')')
            return
        if func_full_name == 'float':
            self.write('Float.valueOf(')
            self.write('(')
            self.dispatch(t.args[0])
            self.write(').toString()')
            self.write(')')
            return

        if t.is_constructor:
            self.write('(')
            self.write('new ')
            self.dispatch(func_name_node)
            self.write('(')
            interleave(lambda: self.write(', '), self.dispatch, t.args)
            self.write(')')
            self.write(')')
            return

        java_name = JAVA_NAME_MAP.get(func_full_name, func_name_node.value)
        if func_name_node.namespace == (util.BUILTINS_CLASS_NAME,):
            # Built-in functions have special handling
            self.write(java_name)
        elif func_name_node.namespace == ():
            # Top-level functions need to be qualified with the wrapper class
            self.write('{0}.{1}'.format(TARGET_PROGRAM_NAME, java_name))
        else:
            # If called function is an object attribute, generate object first
            if getattr(t.func, 'attribute', False):
                self.dispatch(t.func.value)
                self.write('.')
            self.write(java_name)
        self.write('(')
        interleave(lambda: self.write(', '), self.dispatch, t.args)
        self.write(')')


def main(args):
    if not len(args):
        print >> sys.stderr, (
            'ERROR: Must provide code generator with a filename!')
        sys.exit(1)

    output = sys.stdout

    debug = False
    for arg in args[:]:
        if arg == '-d':
            debug = True
        if arg.startswith('-'):
            args.remove(arg)

    if len(args) > 1:
        global TARGET_PROGRAM_NAME
        TARGET_PROGRAM_NAME = args[1]
        output = open(TARGET_PROGRAM_NAME + ".java", 'w')

    ast, _ = analyzer.analyze_file(args[0], debug=debug)
    CodeGenerator(ast, output)

    if output != sys.stdout:
        output.close()


if __name__ == '__main__':
    main(sys.argv[1:])
