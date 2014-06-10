from boa.gen.visitor import VisitorTree
from boa.gen.scope import Scope

import ast

# Use a visitor tree
visitorTree = VisitorTree()
# Compacter syntax
visitor = visitorTree.visitor


# Start as python as a root
@visitorTree.root
@visitor(ast.Module)
def moduleVisitor(node, tree):
    globalScope = Scope()
    out = ''
    for expr in node.body:
        out += tree.decide(expr, globalScope) + ';\n'
    return globalScope.declarations() + '\n' + out

@visitor(ast.Num)
def numVisitor(node, tree, scope):
    return 'boa.toPy(' + str(node.n) + ')'

@visitor(ast.Expr)
def exprVisitor(node, tree, scope):
    return tree.decide(node.value, scope)

@visitor(ast.Attribute)
def attributeVisitor(node, tree, scope):
    return node.attr + '.' + tree.decide(node.value, scope)

@visitor(ast.FunctionDef)
def functionVisitor(node, tree, scope):
    localScope = Scope()
    start = 'function ' + node.name + '(' + \
            ', '.join(tree.decide(arg, localScope) for arg in node.args.args) + ') {\n'
    out = ''
    for expr in node.body:
        out += '  ' + tree.decide(expr, localScope) + ';\n'
    out += '}\n'
    for decorator in node.decorator_list:
        out += node.name + ' = ' + tree.decide(decorator, scope) + '.__getattr__(\'__call__\')(' + node.name + ');\n'
    return start + '  ' + localScope.declarations() + '\n' + out

@visitor(ast.Call)
def callVisitor(node, tree, scope):
    return tree.decide(node.func, scope) + '.__getattr__(\'__call__\')(' + \
           ', '.join(tree.decide(arg, scope) for arg in node.args) + ')'

@visitor(ast.If)
def ifVisitor(node, tree, scope):
    out = 'if (' + tree.decide(node.test, scope) + ') {\n' + \
                ';\n'.join(tree.decide(expr, scope) for expr in node.body) + '\n}\n'
    if node.orelse:
        out += 'else {\n' + ';\n'.join(tree.decide(expr, scope) for expr in node.orelse) + '\n}\n'
    return out

@visitor(ast.For)
def forVisitor(node, tree, scope):
    out = 'var $temp = %s;\n for (var $i = 0; $i < $temp.length; $i++) {\nvar %s = $temp[$i];\n;' %\
          (tree.decide(node.iter, scope), tree.decide(node.target, scope))
    for n in node.body:
        out += tree.decide(n, scope) + ';\n'
    return out + '}'

@visitor(ast.Print)
def printVisitor(node, tree, scope):
    return 'console.log(' + ', '.join(tree.decide(value, scope) for value in node.values) + ')'

@visitor(ast.Pass)
def passVisitor(node, tree, scope):
    return ''

@visitor(ast.Str)
def strVisitor(node, tree, scope):
    return "boa.toPy(" + repr(node.s) + ")"

@visitor(ast.Return)
def returnVisitor(node, tree, scope):
    return 'return ' + tree.decide(node.value, scope)

@visitor(ast.BinOp)
def binOpVisitor(node, tree, scope):
    return '(' + tree.decide(node.left, scope) + ')' + \
           tree.decide(node.op, scope) + \
           '(' + tree.decide(node.right, scope) + ')'

@visitor(ast.Add)
def addVisitor(node, tree, scope):
    return '.__add__'

@visitor(ast.Sub)
def subVisitor(node, tree, scope):
    return '.__sub__'

@visitor(ast.Mult)
def multVisitor(node, tree, scope):
    return '.__mult__'

@visitor(ast.Div)
def divVisitor(node, tree, scope):
    return '.__div__'

@visitor(ast.Name)
def nameVisitor(node, tree, scope):
    return node.id

@visitor(ast.Assign)
def assignVisitor(node, tree, scope):
    names = (target.id for target in node.targets)
    value = tree.decide(node.value, scope)
    out = ''
    for name in names:
        scope.assign(name, value)
        out += name + ' = ' + value + ';\n'
    return out[0:-2]