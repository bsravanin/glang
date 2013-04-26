#!/usr/bin/python2.7

'Code generator for Gramola.'

import analyzer
import os
import re
import sys

# pylint: disable=C0103
# "Invalid name"
# pylint: disable=C0111
# "Missing docstring"


TYPE_MAP = {
    'object': 'Object',
    'void': 'void',
    'int': 'int',
    'bool': 'boolean',
    'float': 'float',
    'str': 'String',
    'list': 'ArrayList<Object>',
    'set': 'HashSet<Object>',
    'dict': 'HashMap<Object,Object>',
    'Graph': 'Graph',
    'Node': 'Node',
    'Edge': 'Edge',
    'NodeSet': 'NodeSet',
    'EdgeSet': 'EdgeSet',
    'Path': 'Path',
    }
JAVA_HEADER = os.path.join(os.path.curdir, 'header.txt')


def convert_type(name):
    # TODO: print warning if name is known?
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
        '''CodeGenerator(tree, file_obj=sys.stdout) -> None.
         Print the source for tree to file.'''
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
        self.fill('public class MainWrapper ')
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
        if (t.name.value == analyzer.CONSTRUCTOR_NAME and
            getattr(t, 'is_method', False)):
            self.write(t.return_type.value)
        else:
            self.dispatch(t.return_type)
            self.write(' ')
            self.dispatch(t.name)
        self.write('(')
        if t.name.value == 'main':
            # TODO: what if the user's 'main' definition is different?
            self.write('String[] args')
        else:
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

    def _Declaration(self, t):
        # Note: this is simply a type-name pair, not the full statement
        self.dispatch(t.var_type)
        self.write(' ')
        self.dispatch(t.name)

    def _ClassDef(self, t):
        self.write('\n')
        self.fill('class ')
        # TODO: add type param to 'name' if base is parameterized
        self.dispatch(t.name)
        if t.base:
            self.write(' extends ')
            self.dispatch(t.base)
        self.enter()
        self.dispatch(t.body)
        self.leave()

    def _ExpressionStmt(self, t):
        self.fill()
        self.dispatch(t.expr)
        self.end_stmt()

    def _DeclarationStmt(self, t):
        self.fill()
        self.dispatch(t.value)
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
                self.write('(')
                self.dispatch(e)
                self.write(').toString())')
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

    def _If(self, t):
        self.fill('if (')
        self.dispatch(t.test)
        self.write(')')
        self.enter()
        self.dispatch(t.body)
        self.leave()
        for else_clause in t.elses:
            self.write(' else')
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
        if op == '==':
            # value equality
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
        self.write(repr(t.value))

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

<<<<<<< HEAD
        self.write("GraphUtil.createVarMap(")
=======
        self.write("GraphUtil.createVariableMap(")
>>>>>>> 20b0e118b65419828207f8a4e85f366aff62b141
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
        # TODO: do function name conversion here, e.g., len(). Consider
        # dispatching as we do for Node subclasses
        # TODO: should builtin functions be named like in Java, for our
        # convenience, or like in Python, for user convenience?
        self.dispatch(t.func)
        self.write('(')
        interleave(lambda: self.write(', '), self.dispatch, t.args)
        self.write(')')


def main(args):
    if not len(args):
        print >> sys.stderr, (
            'ERROR: Must provide code generator with a filename!')
        sys.exit(1)

    debug = False
    for arg in args[:]:
        if arg == '-d':
            debug = True
        if arg.startswith('-'):
            args.remove(arg)

    ast, _ = analyzer.analyze_file(args[0], debug=debug)
    CodeGenerator(ast, output=sys.stdout)


if __name__ == '__main__':
    main(sys.argv[1:])
