#!/usr/bin/python2.7

'AST node definitions for Gramola.'

# pylint: disable=R0903
# "Too few public methods"

from ply import lex


class Error(Exception):
    'Generic error class for nodes.py.'


class InvalidNodeConstructionError(Error):
    'Node constructor was passed invalid arguments.'
    def __init__(self, node_obj):
        Error.__init__(self, 'Invalid arguments to {0} constructor'.format(
                node_obj.__class__.__name__))


def prettify(obj, indent=''):
    '''Recursively builds a pretty string for printing the given object.

    Doesn't handle loops, though.
    '''
    if isinstance(obj, lex.LexToken):
        # At the moment, we don't want to print the whole LexToken
        return repr(obj.value)
    if getattr(obj, '__iter__', None):
        indent += '\t'
        if isinstance(obj, list):
            pretty_iter = [prettify(x, indent=indent) for x in obj]
            start, end = '[', ']'
        elif isinstance(obj, tuple):
            pretty_iter = [prettify(x, indent=indent) for x in obj]
            # These are usually short (e.g. namespaces)
            return '({0})'.format(', '.join(pretty_iter))
        elif isinstance(obj, dict):
            pretty_iter = ['{0}: {1}'.format(prettify(x, indent=indent),
                                             prettify(y, indent=indent))
                           for x, y in obj.iteritems()]
            start, end = '{', '}'
        else:
            return repr(obj)
        if len(obj) > 0:
            bounds_sep = '\n' + indent
            item_sep = ',' + bounds_sep
        else:
            bounds_sep = ''
            item_sep = ', '
        content = item_sep.join(pretty_iter)
        return '{start}{bounds_sep}{content}{bounds_sep}{end}'.format(
            start=start, bounds_sep=bounds_sep, content=content, end=end)
    if getattr(obj, '__dict__', None):
        return '({0}) {1}'.format(
            obj.__class__.__name__,
            prettify(obj.__dict__, indent=indent))
    return repr(obj)


class Node(object):
    'Representation of a node in an abstract syntax tree (AST).'

    def __init__(self, **kwargs):
        for kwarg in kwargs:
            # These fields can be None
            if kwarg in ('base',):
                continue
            if kwarg is None:
                raise InvalidNodeConstructionError(self)
        self.__dict__.update(kwargs)

    def __str__(self):
        return '<{0}: {1}>'.format(
            self.__class__.__name__,
            ', '.join('{0}={1!r}'.format(x, y)
                      for x, y in self.__dict__.iteritems()))

    def __repr__(self):
        return str(self)


class StartNode(Node):
    'AST node for the start symbol.'

    def __init__(self, stmt_list):
        Node.__init__(self, stmt_list=stmt_list)


class FunctionDefNode(Node):
    'AST node for a function definition.'

    def __init__(self, return_type, name, params, body):
        Node.__init__(self, return_type=return_type, name=name, params=params,
                      body=body)


class TypeNode(Node):
    'AST node for a data type, either built-in or derived.'

    def __init__(self, value, namespace):
        Node.__init__(self, value=value, namespace=namespace)


class NameNode(Node):
    'AST node for a variable or function identifier.'

    def __init__(self, value, namespace):
        Node.__init__(self, value=value, namespace=namespace)


class DeclarationNode(Node):
    'AST node for a type-name pair.'

    def __init__(self, var_type, name):
        Node.__init__(self, var_type=var_type, name=name)


class ClassDefNode(Node):
    'AST node for a class definition.'

    def __init__(self, name, body, base=None):
        Node.__init__(self, name=name, body=body, base=base)


class ExpressionStmtNode(Node):
    'AST node for an expression statement.'

    def __init__(self, expr):
        Node.__init__(self, expr=expr)


class DeclarationStmtNode(Node):
    'AST node for a name declaration.'

    def __init__(self, value):
        Node.__init__(self, value=value)


class AssignmentNode(Node):
    'AST node for an assignment statement.'

    def __init__(self, target, value):
        Node.__init__(self, target=target, value=value)


class PrintNode(Node):
    'AST node for a print statement.'

    def __init__(self, values):
        Node.__init__(self, values=values)


class BreakNode(Node):
    'AST node for a break statement.'

    def __init__(self):
        Node.__init__(self)


class ContinueNode(Node):
    'AST node for a continue statement.'

    def __init__(self):
        Node.__init__(self)


class ReturnNode(Node):
    'AST node for a return statement.'

    def __init__(self, value=None):
        Node.__init__(self, value=value)


class IfNode(Node):
    'AST node for an if statement.'

    def __init__(self, test, body, elses=None):
        Node.__init__(self, test=test, body=body, elses=elses or [])


class WhileNode(Node):
    'AST node for a while statement.'

    def __init__(self, test, body):
        Node.__init__(self, test=test, body=body)


class ForNode(Node):
    'AST node for a for statement.'

    def __init__(self, target, iterable, body):
        Node.__init__(self, target=target, iterable=iterable, body=body)


class BinaryOpNode(Node):
    'AST node for a binary operation.'

    def __init__(self, operator, left, right):
        Node.__init__(self, operator=operator, left=left, right=right)


class UnaryOpNode(Node):
    'AST node for a unary operation.'

    def __init__(self, operator, operand):
        Node.__init__(self, operator=operator, operand=operand)


class StringNode(Node):
    'AST node for a string object.'

    def __init__(self, value):
        Node.__init__(self, value=value)


class NumberNode(Node):
    'AST node for a number object.'

    def __init__(self, value):
        Node.__init__(self, value=value)


class ParenNode(Node):
    'AST node for a parenthesized expression.'

    def __init__(self, expr):
        Node.__init__(self, expr=expr)


class ListNode(Node):
    'AST node for a list of expressions.'

    def __init__(self, elts):
        Node.__init__(self, elts=elts)


class DictNode(Node):
    'AST node for a dict, stored as a list of (key, value) items.'

    def __init__(self, items):
        Node.__init__(self, items=items)


class SetNode(Node):
    'AST node for a set of expressions.'

    def __init__(self, elts):
        Node.__init__(self, elts=elts)


class AttributeRefNode(Node):
    'AST node for an attribute reference.'

    def __init__(self, value, attribute):
        Node.__init__(self, value=value, attribute=attribute)


class SubscriptNode(Node):
    'AST node for a subscription.'

    def __init__(self, value, index):
        Node.__init__(self, value=value, index=index)


class CallNode(Node):
    'AST node for a function call.'

    def __init__(self, func, args, is_constructor=False):
        Node.__init__(self, func=func, args=args or [],
                      is_constructor=is_constructor)
