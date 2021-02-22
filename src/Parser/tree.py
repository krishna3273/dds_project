
class Node():
    def __init__(self, type, param=None):
        self.type = type
        self.param = param
        self.children = []

    def add_child(self, node):
        self.children.append(node)


class Tree():
    def __init__(self, tokens, query):
        self.query = query
        self.tokens = tokens

    def build_tree(self):
        self.relations = None
