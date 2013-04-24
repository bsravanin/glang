#!/usr/bin/python2.7

'Code generator for Gramola.'

import parser
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
        # TODO: add imports, etc. here
        self.write('GENERATE IMPORTS, ETC. HERE')
        self.dispatch(t.stmt_list)
        self.fill()

    def _FunctionDef(self, t):
        # TODO: find way to generate wrapper class around top-level Gramola
        # statements, possible with AST ops in the semantic analysis phase
        self.write('\n')
        self.fill('public ')
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
        if value in ('False', 'True'):
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
        else:
            for e in t.values:
                self.fill('System.out.println(')
                self.dispatch(e)
                self.write(')')
        self.end_stmt()

    def _Break(self, t):
        self.fill('break')
        self.end_stmt()

    def _Continue(self, t):
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
        # TODO: handle 'in' operator (collection membership)
        op = t.operator
        if op == 'and':
            op = '&&'
        elif op == 'or':
            op = '||'
        elif op == 'is':
            # TODO: make sure this does object identity
            op = '=='
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
        self.write(t.value)

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
        self.write('(new {0}('.format(convert_type('dict')))
        # TODO: find way to init HashMap without breaking up the statement,
        # maybe use an anonymous class?
        self.write('GENERATE MAP CONTENT HERE')
        #interleave(lambda: self.write(', '), write_pair, t.items)
        self.write('))')

    def _Set(self, t):
        assert t.elts  # t should contain at least one element
        self.write('(new {0}(Arrays.asList('.format(convert_type('set')))
        interleave(lambda: self.write(', '), self.dispatch, t.elts)
        self.write(')))')

    def _AttributeRef(self, t):
        self.dispatch(t.value)
        self.write('.')
        self.dispatch(t.attribute)

    def _Subscript(self, t):
        self.dispatch(t.value)
        # TODO: depending on t.value_type, use a different indexing method
        self.write('.get(')
        self.dispatch(t.index)
        self.write(')')

    def _Call(self, t):
        self.dispatch(t.func)
        self.write('(')
        interleave(lambda: self.write(', '), self.dispatch, t.args)
        self.write(')')


def main(args):
    p = parser.Parser()
    for filename in args:
        tree = p.parse_file(filename)
        CodeGenerator(tree, output=sys.stdout)


if __name__ == '__main__':
    main(sys.argv[1:])
