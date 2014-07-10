from boa.gen.block import Block
from boa.gen.constants import BOA_PRELUDE_CONSTANT_NAME
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
    return '\n'.join(out.generate())

@visitor(ast.Num)
def num_visitor(node, tree, scope):
    return BOA_PRELUDE_CONSTANT_NAME + '.to_py(' + str(node.n) + ')'

@visitor(ast.Expr)
def expr_visitor(node, tree, scope):
    return tree.decide(node.value, scope)

@visitor(ast.Attribute)
def attribute_visitor(node, tree, scope):
    return tree.decide(node.value, scope)  + '.' + node.attr

@visitor(ast.FunctionDef)
def function_visitor(node, tree, scope):
    local_scope = LocalScope(scope)
    out = Block(local_scope, False)
    for arg in node.args.args:
        local_scope.binding(arg.id, None)
    scope.binding(node.name, None)
    out.add(scope.refer(node.name) + ' = function (' +
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
    local_scope = LocalScope(scope)
    out = Block(local_scope, False)
    local_scope.binding(node.target.id, None)
    out.add(BOA_PRELUDE_CONSTANT_NAME + '.for_in(%s, function (%s) {'
            % (tree.decide(node.iter, local_scope), tree.decide(node.target, local_scope)))
    for_block = Block(local_scope)
    for n in node.body:
        for_block.add(tree.decide(n, local_scope))
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
    if node.s.startswith('~js'):
        out = Block(scope, False)
        rest = node.s[3:]
        if rest[0] == '\n':
            rest = rest[1:]

        spaces = ''
        for char in rest:
            if char == ' ' or char == '\t':
                spaces += char
            else:
                break

        if rest.endswith(spaces):
            rest = rest[:-len(spaces)]

        if rest[-1] == '\n':
            rest = rest[:-1]

        rest = rest.split('\n')
        for line in rest:
            if line.startswith(spaces):
                line = line[len(spaces):]
            out.add(line)

        return out
    else:
        return BOA_PRELUDE_CONSTANT_NAME + ".to_py(" + repr(node.s) + ")"

@visitor(ast.Return)
def return_visitor(node, tree, scope):
    return 'return ' + tree.decide(node.value, scope)

@visitor(ast.BinOp)
def bin_op_visitor(node, tree, scope):
    return BOA_PRELUDE_CONSTANT_NAME + '.' + tree.decide(node.op, scope) + \
           '(' + tree.decide(node.left, scope) + ', ' + \
           tree.decide(node.right, scope) + ')'

@visitor(ast.Add)
def add_visitor(node, tree, scope):
    return 'add'

@visitor(ast.Sub)
def sub_visitor(node, tree, scope):
    return 'sub'

@visitor(ast.Mult)
def mult_visitor(node, tree, scope):
    return 'mult'

@visitor(ast.Div)
def div_visitor(node, tree, scope):
    return 'div'

@visitor(ast.Name)
def name_visitor(node, tree, scope):
    return scope.refer(node.id)

@visitor(ast.Assign)
def assign_visitor(node, tree, scope):
    names = (target.id for target in node.targets)
    value = tree.decide(node.value, scope)
    out = Block(scope, False)
    for name in names:
        scope.binding(name, value)
        out.add(scope.refer(name) + ' = ' + value)
    return out