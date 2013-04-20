#!/usr/bin/python2.7

# pylint: disable=R0903
# "Too few public methods"
# pylint: disable=C0111
# "Missing docstring"



class Error(Exception):
    'Generic error class for nodes.py.'


class InvalidNodeConstructionError(Error):
    'Node constructor was passed invalid arguments.'
    def __init__(self, node_obj):
        Error.__init__(self, 'Invalid arguments to {0} constructor'.format(
                node_obj.__class__.__name__))


def pretty_print(obj, indent=''):
    if getattr(obj, '__iter__', None):
        indent += '\t'
        if isinstance(obj, list):
            pretty_iter = [pretty_print(x, indent=indent) for x in obj]
            start, end = '[', ']'
        elif isinstance(obj, tuple):
            pretty_iter = [pretty_print(x, indent=indent) for x in obj]
            start, end = '(', ')'
        elif isinstance(obj, dict):
            pretty_iter = ['{0}: {1}'.format(pretty_print(x, indent=indent),
                                             pretty_print(y, indent=indent))
                           for x, y in obj.iteritems()]
            start, end = '{', '}'
        else:
            return str(obj)
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
        return '{{{0}: {1}}}'.format(
            obj.__class__.__name__,
            pretty_print(obj.__dict__, indent=indent), indent=indent)
    return str(obj)


class Node(object):

    def __init__(self, **kwargs):
        for kwarg in kwargs:
            if kwarg is None:
                raise InvalidNodeConstructionError(self)
        self.__dict__.update(kwargs)

    def __str__(self):
        return '<{0}: {1}>'.format(
            self.__class__.__name__,
            ', '.join('{0}={1}'.format(x, y)
                      for x, y in self.__dict__.iteritems()))

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

    def __init__(self, id_type=None, name=None):
        Node.__init__(self, id_type=id_type, name=name)


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
