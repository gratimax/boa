from boa.gen.constants import BOA_MODULE_CONSTANT_NAME


class Binding(object):

    # represents a binding of a name to a value

    def __init__(self, name, val):
        # create a binding object
        self.name = name
        self.val = val


class Scope(object):

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

    def refer(self, name):
        # get what a binding should be to referred as
        binding = self.get_binding(name)

        if binding:
            return binding.name

    def declarations(self):
        # get the declarations
        return 'var ' + ', '.join(x.name for x in self.bindings) if len(self.bindings) > 0 else ''


class ModuleScope(Scope):

    # scope on the module level, or as python calls it, global level

    def refer(self, name):
        # a binding is referred to by the 'module' object
        binding = self.get_binding(name)

        if binding:
            return BOA_MODULE_CONSTANT_NAME + '.' + binding.name


class LocalScope(Scope):

    # scope that has a parent scope or inherited scope

    def __init__(self, parent):
        # initialize with the parent scope
        super(LocalScope, self).__init__()
        self.parent = parent

    def get_binding(self, name):
        # do I have this binding?
        for x in self.bindings:
            if x.name is name:
                return x
        # check the parent's binding
        return self.parent.get_binding(name)