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

def circumvent_tree_id(control_id: str) -> str:
    """
    Generates the circumvent tree ID based on the control ID.
    
    :param control_id: The ID of the security control.
    :return: A string representing the circumvent tree ID.
    """
    return f"CIRC_{control_id}"

class AttackTreeNode:
    def __init__(self, object_store: ObjectStore):
        self.name: str = ""
        self.type: str = ""  # AND, OR, LEAF, REF, CIRC
        self.reasoning: str = ""
        self.comment: str = ""
        self.children = []
        self.security_control_ids: list[str] = []
        # When a node is marked with CIRC, then a referenced_node_id is set to the ID of the circumvent tree
        self.referenced_node_id: str = None
        self.object_store: ObjectStore = object_store

    def add_child(self, child_node):
        self.children.append(child_node)

    def get_active_control_ids(self) -> list[str]:
        """
        Returns a list of active circumvent tree IDs associated with this node.
        This is useful for determining which circumvent trees are relevant for feasibility calculations.
        """
        return [control_id for control_id in self.security_control_ids if self.object_store.get(control_id).is_active]

    def get_feasibility(self, resolved_parent: 'AttackTreeResolvedNode'=None):
        if self.security_control_ids:
            active_control_ids = self.get_active_control_ids()
            active_circumvent_trees = [self.object_store.get(circumvent_tree_id(control_id)) for control_id in active_control_ids]
            if not all(circumvent_tree for circumvent_tree in active_circumvent_trees):
                raise ValueError("One or more referenced circumvent trees do not exist in the object store.")
            and_node = AttackTreeAndNode(self.object_store)
            and_node.name = f"Controlled {self.name}"
            # and_node.security_control_ids = active_control_ids
            and_node.add_child(self.without_controls())
            for circumvent_tree_original in active_circumvent_trees:
                # create a deep copy of the circumvent tree to avoid modifying the original,
                # because setting the type to CIRC and setting a referenced_node_id will prevent
                # that the tree is expanded in the documentation. But the original tree SHOULD be expanded.
                circumvent_tree = copy.deepcopy(circumvent_tree_original)
                circumvent_tree.root_node.type = "CIRC"
                circumvent_tree.root_node.referenced_node_id = circumvent_tree.id
                and_node.add_child(circumvent_tree.root_node)
            # feasibility = and_node.get_feasibility_without_controls(resolved_node)
            feasibility = and_node.get_feasibility(resolved_parent)
            # ToDo: are the commented lines above an alternative to the following?

            # resolved_node.children[-1] is now the AND node that combines the original node and the circumvent trees
            # after invoking get_feasibility we can set the control_ids without triggering an endless recursion
            if resolved_parent != None and len(resolved_parent.children) > 0:
                resolved_parent.children[-1].security_control_ids = active_control_ids

            return feasibility

        return self.get_feasibility_without_controls(self._get_feasibility, resolved_parent)

    def without_controls(self) -> 'AttackTreeLeafNode':
        deep_copy = copy.deepcopy(self)
        deep_copy.security_control_ids = []
        return deep_copy

    def get_feasibility_without_controls(self, get_feasibility, resolved_parent: 'AttackTreeResolvedNode'=None) -> Feasibility:
        """
        Returns the feasibility of the node without considering any controls.
        This is useful for calculating the base feasibility of the node.

        get_feasibility: A callable that retrieves the feasibility of the node.
        """
        resolved_node = AttackTreeResolvedNode() if resolved_parent is not None else None
        
        # do not expand circumvent nodes or reference nodes, so that they show up as references in the report
        # instead of being expanded in-place in every using attack tree
        feasibility = get_feasibility(None if self.type == "CIRC" or self.type == "REF" else resolved_node)
        
        if resolved_parent is not None:
            resolved_node.fill_from_node(self, feasibility)
            resolved_parent.children.append(resolved_node)

        return feasibility
    
    def _get_feasibility(self, resolved_parent: 'AttackTreeResolvedNode'=None) -> Feasibility:
        """
        This method should be implemented by subclasses to calculate the feasibility of the node.
        It is expected to return a Feasibility object.
        """
        raise NotImplementedError("Subclasses must implement this method.")

class AttackTreeAndNode(AttackTreeNode):
    def __init__(self, object_store: ObjectStore):
        super().__init__(object_store)
        self.name = ""
        self.type = "AND"

    def _get_feasibility(self, resolved_parent: 'AttackTreeResolvedNode'=None) -> Feasibility:
        if not self.children:
            raise ValueError("AND node has no children.")
        
        feasibility = self.children[0].get_feasibility(resolved_parent)

        for child in self.children[1:]:
            feasibility = feasibility.and_feasibility(child.get_feasibility(resolved_parent))
        
        return feasibility
        
class AttackTreeOrNode(AttackTreeNode):
    def __init__(self, object_store: ObjectStore):
        super().__init__(object_store)
        self.name = ""
        self.type = "OR"
    
    def _get_feasibility(self, resolved_parent: 'AttackTreeResolvedNode'=None) -> Feasibility:
        if not self.children:
            raise ValueError("OR node has no children.")
        
        feasibility = self.children[0].get_feasibility(resolved_parent)

        for child in self.children[1:]:
            feasibility = feasibility.or_feasibility(child.get_feasibility(resolved_parent))
        
        return feasibility

class AttackTreeLeafNode(AttackTreeNode):
    def __init__(self, feasibility: Feasibility, object_store: ObjectStore):
        super().__init__(object_store)
        self.name = ""
        self.type = "LEAF"
        self._feasibility = feasibility
    
    def _get_feasibility(self, resolved_parent: 'AttackTreeResolvedNode'=None) -> Feasibility:
        return self._feasibility

class AttackTreeReferenceNode(AttackTreeNode):
    def __init__(self, object_store: ObjectStore):
        super().__init__(object_store)
        self.type = "REF"
    
    def _get_feasibility(self, resolved_parent: 'AttackTreeResolvedNode'=None) -> Feasibility:
        if self.referenced_node_id is None:
            raise ValueError("Referenced node ID is not set.")
        
        referenced_tree = self.object_store.get(self.referenced_node_id)
        if referenced_tree is None:
            raise ValueError(f"Referenced node with ID {self.referenced_node_id} not found.")
        
        feasibility = referenced_tree.root_node.get_feasibility(resolved_parent)
        return feasibility

class AttackTreeResolvedNode:
    def __init__(self):
        self.name: str = ""
        self.type: str = "" # AND, OR, LEAF, REF, CIRC
        self.feasibility: Feasibility = None
        self.reasoning: str = ""
        self.comment: str = ""
        self.children = []
        self.security_control_ids: list[str] = []
        # holds the referenced node ID for REF and CIRC nodes, None otherwise
        self.referenced_node_id: str = None

    def fill_from_node(self, node: AttackTreeNode, feasibility: Feasibility) -> None:
        """
        Fills the resolved node from a regular attack tree node.
        """
        self.name = node.name
        self.type = node.type
        self.reasoning = node.reasoning
        self.comment = node.comment
        self.feasibility = feasibility
        self.security_control_ids = node.get_active_control_ids()
        self.referenced_node_id = node.referenced_node_id

class ResolvedAttackTree:
    """
    Represents a resolved attack tree where each node has a resolved feasibility.
    """
    def __init__(self, id: str):
        self.id = id
        self.root_node: AttackTreeResolvedNode = None

class AttackTree:
    def __init__(self, id: str):
        self.id = id
        self.description = ""
        self.root_node: AttackTreeNode = None

    def get_feasibility(self, resolved_trees: list[ResolvedAttackTree]=None) -> Feasibility:
        """
        Returns the feasibility of the attack tree.
        Optionally accepts a resolved_trees parameter for advanced use cases.
        """
        if self.root_node is None:
            raise ValueError(f"Attack tree with id '{self.id}' has no root node.")
        
        if resolved_trees is None:
            return self.root_node.get_feasibility()
        else:
            container_node = AttackTreeResolvedNode()
            # The root node will be inserted as only child to the container node
            feasibility = self.root_node.get_feasibility(container_node)
            if not len(container_node.children) == 1:
                raise ValueError(f"Attack Tree '{self.id}': Root node did not return exactly one resolved child node.")

            resolved_tree = ResolvedAttackTree(self.id)
            resolved_tree.root_node = container_node.children[0]
            resolved_trees.append(resolved_tree)
            return feasibility
