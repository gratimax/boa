from boa.gen import codegen
from boa.gen.scope import Scope
from os import path
import ast

f = path.abspath('fixtures/file.py')
contents = open(f, 'r').read()
tree = ast.parse(contents, f)

print codegen(tree)