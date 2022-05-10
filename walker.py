from baum import therapyNode

class JohnnieWalker:
    def __init__(self):
        pass

    def decide(self, baum_start_node, env):
        assert not isinstance(baum_start_node, therapyNode)
        current_node = baum_start_node
        while not isinstance(current_node, therapyNode):
            current_node = current_node.return_next(env)

        return current_node


    def print_decision_tree(self, node, prefix = ""):   #das ding zeichnet nur den standard-baum
        if isinstance(node, therapyNode):
            print(prefix + "TherapyNode: " + node.name)
        else:
            print(prefix + "ForkNode: " + node.name)
            new_prefix = prefix + ".  "
            for child in node.children:
                self.print_decision_tree(child, new_prefix)
                # das ist eine rekursionsbasierte Funktion, die immer wieder sich selbst aufruft und so den Baum zeichnet


