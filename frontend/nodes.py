#!/usr/bin/python2.7

# pylint: disable=R0903
# "Too few public methods"
# pylint: disable=C0111
# "Missing docstring"

import pprint


class Error(Exception):
    'Generic error class for nodes.py.'


class InvalidNodeConstructionError(Error):
    'Raised when node constructor is passed invalid arguments.'
    def __init__(self, node_obj):
        Error.__init__(self, 'Invalid arguments to {0} constructor'.format(
                node_obj.__class__.__name__))


class Node(object):

    def __init__(self, **kwargs):
        for kwarg in kwargs:
            if kwarg is None:
                raise InvalidNodeConstructionError(self)
        self.__dict__.update(kwargs)

    def __str__(self):
        # TODO: find better way to print this
        return pprint.pformat(self.__dict__)

    def __repr__(self):
        return str(self)


class StartNode(Node):

    def __init__(self, stmt_list=None):
        Node.__init__(self, stmt_list=stmt_list)


class FunctionDefNode(Node):

    def __init__(self, return_type=None, name=None, params=None, body=None):
        Node.__init__(self, return_type=return_type, name=name, params=params,
                      body=body)


class TypeNode(Node):

    def __init__(self, value=None):
        Node.__init__(self, value=value)


class NameNode(Node):

    def __init__(self, value=None):
        Node.__init__(self, value=value)


class DeclarationNode(Node):

    def __init__(self, id_type=None, names=None):
        Node.__init__(self, id_type=id_type, names=names)


class AssignmentNode(Node):

    def __init__(self, target=None, value=None):
        Node.__init__(self, target=target, value=value)


class PrintNode(Node):

    def __init__(self, values=None):
        Node.__init__(self, values=values)


class BreakNode(Node):

    def __init__(self):
        Node.__init__(self)


class ContinueNode(Node):

    def __init__(self):
        Node.__init__(self)


class ReturnNode(Node):

    def __init__(self):
        Node.__init__(self)


class IfNode(Node):

    def __init__(self, test=None, body=None, elses=None):
        # elses are optional. use empty list to pass the "not None" check
        Node.__init__(self, test=test, body=body, elses=elses or [])


class WhileNode(Node):

    def __init__(self, test=None, body=None):
        Node.__init__(self, test=test, body=body)


class ForNode(Node):

    def __init__(self, target=None, iterable=None, body=None):
        Node.__init__(self, target=target, iterable=iterable, body=body)


class SuiteNode(Node):

    def __init__(self, stmts=None):
        Node.__init__(self, stmts=stmts)


class BinaryOpNode(Node):

    def __init__(self, operator=None, left=None, right=None):
        Node.__init__(self, operator=operator, left=left, right=right)


class UnaryOpNode(Node):

    def __init__(self, operator=None, operand=None):
        Node.__init__(self, operator=operator, operand=operand)


class AttributeRefNode(Node):

    def __init__(self, value=None, attribute=None):
        Node.__init__(self, value=value, attribute=attribute)


class SubscriptNode(Node):

    def __init__(self, value=None, index=None):
        Node.__init__(self, value=value, index=index)

class CallNode(Node):

    def __init__(self, func=None, args=None):
        # args are optional. use empty list to pass the "not None" check
        Node.__init__(self, func=func, args=args or [])


class ClassDefNode(Node):

    def __init__(self, name=None, base=None, body=None):
        # base is optional. use empty string to pass the "not None" check
        Node.__init__(self, name=name, base=base or '', body=body)
