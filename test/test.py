from boa.gen import codegen
from boa.gen.scope import Scope
from os import path
import ast
from time import time

f = path.abspath('fixtures/file.py')
out = path.abspath('fixtures/file.js')
contents = open(f, 'r').read()
s1 = time()
tree = ast.parse(contents, f)
s2 = time()
print s2 - s1


t1 = time()
code = codegen(tree)
#open(out, 'w').write(code)
t2 = time()
print t2 - t1
print t2, t1
print code