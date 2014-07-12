from boa.gen.codegen import visitorTree


# codegen method
def codegen(tree):
    return visitorTree.run(tree)