class VisitorTree:

    # class representing a tree of visitors

    def __init__(self):
        # create a new tree
        self.visitors = {}
        self.rootFn = None

    def visitor(self, *classes):
        # annotation for adding a visitor:
        # @tree.visitor(ast.Module)
        # def moduleVisitor(tree, ...):

        def with_fn(fn):
            for clss in classes:
                # overwrite in this case, as per the datastructure
                self.visitors[clss] = fn

            return fn

        return with_fn

    def root(self, fn):
        # annotation to set the root
        self.rootFn = fn
        return fn

    def decide(self, node, *args):
        # called by functions to do something with a node
        clss = node.__class__
        if clss in self.visitors:
            return self.visitors[clss](node, self, *args)
        else:
            raise ValueError(clss.__name__ + ' not found in possible visitors')

    def run(self, node):
        # run this tree at the root
        return self.rootFn(node, self)