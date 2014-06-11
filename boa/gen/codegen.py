from boa.gen.block import Block
from boa.gen.constants import BOA_BUILTINS_CONSTANT_NAME
from boa.gen.scope import ModuleScope, LocalScope
from boa.gen.visitor import VisitorTree

import ast

# Use a visitor tree
visitorTree = VisitorTree()
# Compacter syntax
visitor = visitorTree.visitor

# Start as python as a root
@visitorTree.root
@visitor(ast.Module)
def module_visitor(node, tree):
    global_scope = ModuleScope()
    out = Block(global_scope)
    for expr in node.body:
        out.add(tree.decide(expr, global_scope))
    out.insert(0, global_scope.declarations())
    return '\n'.join(out.generate())

@visitor(ast.Num)
def num_visitor(node, tree, scope):
    return BOA_BUILTINS_CONSTANT_NAME + '.to_py(' + str(node.n) + ')'

@visitor(ast.Expr)
def expr_visitor(node, tree, scope):
    return tree.decide(node.value, scope)

@visitor(ast.Attribute)
def attribute_visitor(node, tree, scope):
    return node.attr + '.' + tree.decide(node.value, scope)

@visitor(ast.FunctionDef)
def function_visitor(node, tree, scope):
    local_scope = LocalScope(scope)
    out = Block(local_scope, False)
    out.add('var ' + node.name + ' = function (' +
            ', '.join(tree.decide(arg, local_scope) for arg in node.args.args)
            + ') {')
    body_block = Block(local_scope)
    for expr in node.body:
        body_block.add(tree.decide(expr, local_scope))
    out.add(body_block)
    out.add('}')
    for decorator in node.decorator_list:
        out.add(node.name + ' = ' + tree.decide(decorator, scope) +
                '(' + node.name + ')')
    decs = local_scope.declarations()
    if decs:
        body_block.insert(0, decs)
    return out

@visitor(ast.Call)
def call_visitor(node, tree, scope):
    return tree.decide(node.func, scope) + '(' + \
           ', '.join(tree.decide(arg, scope) for arg in node.args) + ')'

@visitor(ast.If)
def if_visitor(node, tree, scope):
    out = Block(scope, False)
    out.add('if (' + tree.decide(node.test, scope) + ') {')

    if_block = Block(scope)
    for expr in node.body:
        if_block.add(tree.decide(expr, scope))
    out.add(if_block)

    if node.orelse:
        out.add('} else {')
        else_block = Block(scope)
        for expr in node.orelse:
            else_block.add(tree.decide(expr, scope))
        out.add(else_block)
        out.add('}')
    else:
        out.add('}')

    return out

@visitor(ast.For)
def for_visitor(node, tree, scope):
    out = Block(scope, False)
    out.add('builtins$.for_in(%s, function (%s) {'
            % (tree.decide(node.iter, scope), tree.decide(node.target, scope)))
    for_block = Block(scope)
    for n in node.body:
        for_block.add(tree.decide(n, scope))
    out.add(for_block)

    out.add('})')
    return out

@visitor(ast.Print)
def print_visitor(node, tree, scope):
    return 'console.log(' + ', '.join(tree.decide(value, scope) for value in node.values) + ')'

@visitor(ast.Pass)
def pass_visitor(node, tree, scope):
    return '/* pass */'

@visitor(ast.Str)
def str_visitor(node, tree, scope):
    return BOA_BUILTINS_CONSTANT_NAME + ".to_py(" + repr(node.s) + ")"

@visitor(ast.Return)
def return_visitor(node, tree, scope):
    return 'return ' + tree.decide(node.value, scope)

@visitor(ast.BinOp)
def bin_op_visitor(node, tree, scope):
    return tree.decide(node.left, scope) + tree.decide(node.op, scope) + \
           '(' + tree.decide(node.right, scope) + ')'

@visitor(ast.Add)
def add_visitor(node, tree, scope):
    return '.__add__'

@visitor(ast.Sub)
def sub_visitor(node, tree, scope):
    return '.__sub__'

@visitor(ast.Mult)
def mult_visitor(node, tree, scope):
    return '.__mult__'

@visitor(ast.Div)
def div_visitor(node, tree, scope):
    return '.__div__'

@visitor(ast.Name)
def name_visitor(node, tree, scope):
    return node.id

@visitor(ast.Assign)
def assign_visitor(node, tree, scope):
    names = (target.id for target in node.targets)
    value = tree.decide(node.value, scope)
    out = Block(scope, False)
    for name in names:
        scope.binding(name, value)
        out.add(name + ' = ' + value)
    return out