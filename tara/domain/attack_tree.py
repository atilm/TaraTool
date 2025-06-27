from tara.domain.feasibility import Feasibility
from tara.domain.asset import Asset
from tara.domain.security_property import SecurityProperty
from tara.domain.object_store import ObjectStore
import copy

def attack_tree_id(asset: Asset, security_property: SecurityProperty) -> str:
    """
    Generates the attack tree ID based on the asset and security property.
    
    :param asset: The asset for which the attack tree ID is being generated.
    :param security_property: The security property associated with the attack tree.
    :return: A string representing the attack tree ID.
    """
    return f"AT_{asset.id}_{security_property.to_attack_id()}"

class AttackTreeNode:
    def __init__(self, object_store: ObjectStore):
        self.name: str = ""
        self.reasoning: str = ""
        self.comment: str = ""
        self.children = []
        self.security_control_ids: list[str] = []
        self.object_store: ObjectStore = object_store

    def add_child(self, child_node):
        self.children.append(child_node)

    def get_feasibility(self):
        if self.security_control_ids:
            circumvent_trees = [self.object_store.get(f"CIRC_{control_id}") for control_id in self.security_control_ids]
            if not all(circumvent_tree for circumvent_tree in circumvent_trees):
                raise ValueError("One or more referenced circumvent trees do not exist in the object store.")
            and_node = AttackTreeAndNode(self.object_store)
            and_node.add_child(self.without_controls())
            for circumvent_tree in circumvent_trees:
                and_node.add_child(circumvent_tree.root_node)
            return and_node.get_feasibility()

        return self.get_feasibility_without_controls()

    def without_controls(self) -> 'AttackTreeLeafNode':
        deep_copy = copy.deepcopy(self)
        deep_copy.security_control_ids = []
        return deep_copy

    def get_feasibility_without_controls(self) -> Feasibility:
        """
        Returns the feasibility of the node without considering any controls.
        This is useful for calculating the base feasibility of the node.
        """
        raise NotImplementedError("This method should be overridden in subclasses.")

class AttackTreeAndNode(AttackTreeNode):
    def __init__(self, object_store: ObjectStore):
        super().__init__(object_store)
        self.name = ""
        self.type = "AND"

    def get_feasibility_without_controls(self) -> Feasibility:
        """
        Returns the feasibility of the AND node.
        The feasibility is calculated as the maximum feasibility of all child nodes.
        """
        if not self.children:
            raise ValueError("AND node has no children.")
        
        feasibility = self.children[0].get_feasibility()

        for child in self.children[1:]:
            feasibility = feasibility.and_feasibility(child.get_feasibility())
        
        return feasibility

class AttackTreeOrNode(AttackTreeNode):
    def __init__(self, object_store: ObjectStore):
        super().__init__(object_store)
        self.name = ""
        self.type = "OR"

    def get_feasibility_without_controls(self) -> Feasibility:
        """
        Returns the feasibility of the OR node.
        The feasibility is calculated as the minimum feasibility of all child nodes.
        """
        if not self.children:
            raise ValueError("OR node has no children.")
        
        feasibility = self.children[0].get_feasibility()

        for child in self.children[1:]:
            feasibility = feasibility.or_feasibility(child.get_feasibility())
        
        return feasibility

class AttackTreeLeafNode(AttackTreeNode):
    def __init__(self, feasibility: Feasibility, object_store: ObjectStore):
        super().__init__(object_store)
        self.name = ""
        self.type = "LEAF"
        self._feasibility = feasibility

    def get_feasibility_without_controls(self) -> Feasibility:
        """
        Returns the feasibility of the node without considering any controls.
        This is useful for calculating the base feasibility of the node.
        """
        return self._feasibility

class AttackTreeReferenceNode(AttackTreeNode):
    def __init__(self, object_store: ObjectStore):
        super().__init__(object_store)
        self.type = "REFERENCE"
        self.referenced_node_id: str = None

    def get_feasibility_without_controls(self) -> Feasibility:
        """
        Returns the feasibility of the referenced node.
        If the referenced node is not found, raises an error.
        """
        if self.referenced_node_id is None:
            raise ValueError("Referenced node ID is not set.")
        
        referenced_node = self.object_store.get(self.referenced_node_id)
        if referenced_node is None:
            raise ValueError(f"Referenced node with ID {self.referenced_node_id} not found.")
        
        return referenced_node.get_feasibility()

class AttackTree:
    def __init__(self, id: str):
        self.id = id
        self.description = ""
        self.root_node: AttackTreeNode = None

    def get_feasibility(self) -> Feasibility:
        """
        Returns the feasibility of the attack tree.
        This method should be overridden in subclasses to provide specific feasibility logic.
        """
        if self.root_node is None:
            raise ValueError("Attack tree has no root node.")
        
        return self.root_node.get_feasibility()