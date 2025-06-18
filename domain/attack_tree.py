from domain.feasibility import Feasibility
from domain.asset import Asset
from domain.security_property import SecurityProperty

def attack_tree_id(asset: Asset, security_property: SecurityProperty) -> str:
    """
    Generates the attack tree ID based on the asset and security property.
    
    :param asset: The asset for which the attack tree ID is being generated.
    :param security_property: The security property associated with the attack tree.
    :return: A string representing the attack tree ID.
    """
    return f"AT_{asset.id}_{security_property.to_attack_id()}"

class AttackTreeNode:
    def __init__(self):
        self.name: str = ""
        self.reasoning: str = ""
        self.comment: str = ""
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
    def __init__(self, feasibility: Feasibility):
        super().__init__()
        self.name = ""
        self.type = "LEAF"
        self._feasibility = feasibility

    def get_feasibility(self):
        return self._feasibility

class AttackTreeReferenceNode(AttackTreeNode):
    def __init__(self):
        super().__init__()
        self.type = "REFERENCE"
        self.referenced_node_id: str = None

class AttackTree:
    def __init__(self, id: str):
        self.id = id
        self.description = ""
        self.root_node: AttackTreeNode = None
