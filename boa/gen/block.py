class Block:

    # represents a block of JS code

    def __init__(self, scope, indent=True):
        # init this block
        self.fragments = []
        self.indent = indent
        if scope:
            self.scope = scope

    def add(self, fragment):
        # add a fragment
        if isinstance(fragment, Block):
            self.fragments.append(fragment)
        else:
            fragment = fragment.split('\n')
            for frag in fragment:
                self.fragments.append(frag)

    def insert(self, index, fragment):
        # insert a fragment somewhere
        self.fragments.insert(index, fragment)

    def generate(self):
        # generate a string out of this block
        frags = []

        for frag in self.fragments:
            if isinstance(frag, Block):
                # add a tab to nested blocks
                for block_fragment in frag.generate():
                    if frag.indent:
                        frags.append("  " + block_fragment)
                    else:
                        frags.append(block_fragment)
            else:
                frags.append(frag)

        return frags