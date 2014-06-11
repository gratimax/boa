from boa.gen import codegen
from boa.gen.scope import Scope
from os import path
import ast

f = path.abspath('fixtures/file.py')
out = path.abspath('fixtures/file.js')
contents = open(f, 'r').read()
tree = ast.parse(contents, f)

code = codegen(tree)
open(out, 'w').write(code)