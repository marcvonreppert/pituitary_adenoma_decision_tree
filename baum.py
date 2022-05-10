
class therapyNode:
    def __init__(self, parent=None):
        self.parent = parent
        self.name = ""

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

class forkNode:
    def __init__(self):
        self.parent = None
        self.children = None
        self.decisionfunc = None
        self.d_2_c_map = None
        self.name = ""

    def set_name(self, name):
        self.name = name

    def add_children(self, children):
        self.children = children

    def add_parent(self, parent):
        self.parent = parent

    def add_d_2_c_map(self, d_2_c_map):
        self.d_2_c_map = d_2_c_map

    def add_decisionfunc(self, decisionfunc):
        self.decisionfunc = decisionfunc
    
    def return_next(self, env):
        # apply decision func
        print("calling node " + self.name)

        decision = self.decisionfunc(env)
        next_child_idx = self.d_2_c_map[decision]
        #decision ist entweder 0 oder 1 (siehe tree_gen)

        return self.children[next_child_idx]
        #gibt das passende child zurück (siehe tree_gen)


