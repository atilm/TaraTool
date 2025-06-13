from domain.feasibility import Feasibility

class AttackTreeNode:
    def __init__(self):
        self.name: str = ""
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def get_feasibility(self) -> Feasibility:
        """
        Returns the feasibility of the node.
        This method should be overridden in subclasses to provide specific feasibility logic.
        """
        raise NotImplementedError("This method should be overridden in subclasses.")


class AttackTreeAndNode(AttackTreeNode):
    def __init__(self):
        super().__init__()
        self.name = ""
        self.type = "AND"

class AttackTreeOrNode(AttackTreeNode):
    def __init__(self):
        super().__init__()
        self.name = ""
        self.type = "OR"

class AttackTreeLeafNode(AttackTreeNode):
    def __init__(self):
        super().__init__()
        self.name = ""
        self.type = "LEAF"

class AttackTreeReferenceNode(AttackTreeNode):
    def __init__(self):
        super().__init__()


class AttackTree:
    def __init__(self, name: str, description: str = None):
        self.name = name
        self.description = description
        self.root_node = []
