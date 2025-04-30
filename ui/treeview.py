
class TreeItem:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = []

    def child_count(self):
        return len(self.children)

    def child(self, row):
        return self.children[row]

    def row(self):
        if self.parent:
            return self.parent.children.index(self)
        return 0

    def add_child(self, item):
        self.children.append(item)
