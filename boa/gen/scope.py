class Binding:

    # represents a binding of a name to a value

    def __init__(self, name, val):
        # create a binding object
        self.name = name
        self.val = val


class Scope:

    # represents a scope with bindings

    def __init__(self):
        # create a scope object
        self.bindings = []

    def binding(self, name, val):
        # add a bindings
        binding = self.get_binding(name)
        if binding is not None:
            binding['val'] = val
        else:
            self.add_binding(Binding(name, val))

    def get_binding(self, name):
        # do I have this binding?
        for x in self.bindings:
            if x.name is name:
                return x
        return None

    def add_binding(self, binding):
        # add a binding
        self.bindings.append(binding)

    def declarations(self):
        # get the declarations
        return 'var ' + ', '.join(x.name for x in self.bindings) + ';' if len(self.bindings) > 0 else ''


class ModuleScope(Scope):

    # scope on the module level, or as python calls it, global level

    pass


class LocalScope(Scope):

    # scope that has a parent scope or inherited scope

    pass