# ----------------------------------------------------------------------
# codegen.py
#
# Code Generator Gramola.
##
# ----------------------------------------------------------------------

#type_list = ["int", "double"]

class Node:
    def __init__(self):
        pass
    
class Lines:
    def __init__(self):
        self.lines = []

    def __str__(self):
        s = ""
        for line in self.lines:
            s += str(line)
            s += "\n"
        return s
        
    def append(self, line):
        self.lines.append(line)

class Line:
    def __init__(self):
        self.line = ""

    def append(self, s):
        self.line += str(s)
        self.line += " "

    def endline(self):
        self.line += ";"
        
    def __str__(self):
        return self.line
        
class Codegen:
    def __init__(self):
        self.lines = []

    def gen_declaration(self, node):
        code = Line()
        code.append(node.vtype)
        code.append(node.varname)
        code.endline()
        return code
    
    def gen_call_expr(self, node):
        code = Line()
        # call a constructor or a static func
        # e.g. g = Graph() 
        #      t = time()
        if node.subsubtype == "constructor":
            code.append(node.typename)
            code.append("(")
            # the types are checked in semantic analysis
            # so we assume all arguments match the right types here
            if node.args:
                first = node.args[0]
                code.append(first)
                for arg in node.args[1:]:
                    code.append(",")
                    code.append(arg)
            code.append(")")
        else:
            # other subtypes include:
            # built in function: t = time()
            # member function references: nodes = g.nodes()
            raise NotImplementedError
        return code

    def gen_arith_expr(self, node):
        code = Line()
        code.append(str(node.left))
        code.append(node.op)
        code.append(str(node.right))
        return code
    
    def gen_expr(self, node):
        generators = { "arith" : self.gen_arith_expr,
                    "call" : self.gen_call_expr}
        assert(node.type == "expr")
        generator = generators[node.subtype]
        return generator(node)
        
        
    def gen_lvalue(self, node):
        code = Line()
        if node.subtype == "declare_and_assign":
            code.append(node.vtype)
            code.append(node.vname)
        elif node.subtype == "id":
            code.append(node.id)
        else:
            raise NotImplementedError
        return code

    def gen_assignment(self, node):
        lvalue = node.lvalue # variable name
        expr = node.expr # expression
        code = Line()

        code.append(self.gen_lvalue(lvalue))
        code.append("=")
        code.append(self.gen_expr(expr))
        code.endline()
        return code

    def gen_statement(self, node):
        # dispatch according to the right statement type
        return self.gen_assignment(node)
    
    def gen_func(self, node):
        def __header__(rtype, name, params):
            code = Line()
            code.append("public ")
            code.append(rtype)
            code.append(funcname)
            code.append("(")
            if params:
                first = params[0]
                code.append(param.type)
                code.append(param.name)
                for param in params[1:]:
                    code.append(",")
                    code.append(param.type)
                    code.append(param.name)
            code.append(")")
            code.append("{")
            return code
            
        def __exit__():
            code = Line()
            code.append("}")
            return code
        
        rtype = node.rtype
        funcname = node.name
        params = node.params
        body = node.body

        funccode = Lines()
        funccode.append(__header__(rtype,funcname, params))
        for stat in body:
            funccode.append(self.gen_statement(stat))
        funccode.append(__exit__())
        return funccode
        
def test_expr(gen):
    expr = Node()
    expr.left =  3
    expr.op = "+"
    expr.right = 4
    print gen.gen_expr(expr)
    
def test_assign(gen):
    expr = Node()
    expr.left = 3
    expr.op = "+"
    expr.right = 4
    assign = Node()
    assign.lvalue =  "a"
    assign.expr = expr
    print gen.gen_assignment(assign)

def test_func(gen):
    construct_expr = Node()
    construct_expr.type = "expr"
    construct_expr.subtype = "call"
    construct_expr.subsubtype = "constructor"
    construct_expr.typename = "Graph"
    construct_expr.args = []

    declare_assign = Node()
    declare_assign.type = "statement"
    declare_assign.lvalue = Node()
    declare_assign.lvalue.subtype = "declare_and_assign"
    declare_assign.lvalue.vtype = "Graph"
    declare_assign.lvalue.vname = "g"
    declare_assign.expr = construct_expr

    expr = Node()
    expr.type = "expr"
    expr.subtype = "arith"
    expr.left = 3
    expr.op = "+"
    expr.right = 4

    assign = Node()
    assign.type = "statement"
    assign.lvalue = Node()
    assign.lvalue.subtype = "id"
    assign.lvalue.id = "a"
    assign.expr = expr

    func = Node()
    func.type = "func"
    func.rtype = "int"
    func.name = "main"
    func.params = []
    func.body = []
    func.body.append(assign)
    func.body.append(declare_assign)
    
    print gen.gen_func(func)
    
if __name__ == "__main__":
    gen = Codegen()
    #    test_expr(gen)
    test_func(gen)
    
