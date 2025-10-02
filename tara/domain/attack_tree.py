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
        self.reasoning: str = ""
        self.comment: str = ""
        self.children = []
        self.security_control_ids: list[str] = []
        self.object_store: ObjectStore = object_store
        self.cached_feasibility: Feasibility = None

    def add_child(self, child_node):
        self.children.append(child_node)

    def get_active_control_ids(self) -> list[str]:
        """
        Returns a list of active circumvent tree IDs associated with this node.
        This is useful for determining which circumvent trees are relevant for feasibility calculations.
        """
        return [control_id for control_id in self.security_control_ids if self.object_store.get(control_id).is_active]

    def invalidate_cache(self):
        """
        Invalidates the cached feasibility of the node.
        This is useful when the node has been modified and the feasibility needs to be recalculated.
        """
        self.cached_feasibility = None
        for child in self.children:
            child.invalidate_cache()

    def get_feasibility(self, without_controls: bool = False):
        if self.cached_feasibility is not None:
            return self.cached_feasibility

        if not(without_controls) and self.security_control_ids:
            active_circumvent_trees = [self.object_store.get(circumvent_tree_id(control_id)) for control_id in self.get_active_control_ids()]
            if not all(circumvent_tree for circumvent_tree in active_circumvent_trees):
                raise ValueError("One or more referenced circumvent trees do not exist in the object store.")
            and_node = AttackTreeAndNode(self.object_store)
            and_node.add_child(self.without_controls())
            for circumvent_tree in active_circumvent_trees:
                and_node.add_child(circumvent_tree.root_node)
            
            self.cached_feasibility = and_node.get_feasibility(without_controls)
            return self.cached_feasibility

        self.cached_feasibility = self.get_feasibility_without_controls(without_controls)
        return self.cached_feasibility

    def without_controls(self) -> 'AttackTreeLeafNode':
        deep_copy = copy.deepcopy(self)
        deep_copy.security_control_ids = []
        return deep_copy

    def get_feasibility_without_controls(self, without_controls: bool = False) -> Feasibility:
        """
        Returns the feasibility of the node without considering any controls.
        This is useful for calculating the base feasibility of the node.
        """
        raise NotImplementedError("This method should be overridden in subclasses.")
    
    def get_resolved_node(self) -> 'AttackTreeResolvedNode':
        """
        Returns a resolved node representation of the attack tree node.
        This is useful for creating a resolved attack tree.
        """

        control_ids = self.get_active_control_ids()
        circumvent_trees = [self.object_store.get(circumvent_tree_id(control_id)) for control_id in control_ids]

        has_controls = len(control_ids) > 0

        resolved_node = AttackTreeResolvedNode()
        resolved_node.name = self.name
        resolved_node.type = self.type
        resolved_node.reasoning = self.reasoning
        resolved_node.comment = self.comment
        # if the original node has controls, they are split into an uncontrolled noded and the circumvent trees
        # threrefore the uncontrolled feasibility is shown when there are controls
        resolved_node.feasibility = self.get_feasibility_without_controls() if has_controls else self.get_feasibility()
        resolved_node.children = [child.get_resolved_node() for child in self.children]
        resolved_node.security_control_ids = control_ids
        # "REF" nodes have the attribute referenced_node_id set to the ID of the referenced node
        resolved_node.referenced_node_id = self.referenced_node_id if hasattr(self, 'referenced_node_id') else None

        if not has_controls:
            return resolved_node
        else:
            # insert an AND node which combines the unmitigated original node and its circumvent trees
            and_node = AttackTreeResolvedNode()
            and_node.name = f"**Controlled:** {self.name}"
            and_node.type = "AND"
            and_node.feasibility = self.get_feasibility()
            and_node.security_control_ids = control_ids

            resolved_node.security_control_ids = []
            and_node.children.append(resolved_node)

            for circumvent_tree in circumvent_trees:
                if circumvent_tree is None:
                    raise ValueError("One or more referenced circumvent trees do not exist in the object store.")
                and_node.children.append(self.circumvent_tree_to_resolved_node(circumvent_tree))

            return and_node
        
    def circumvent_tree_to_resolved_node(self, circumvent_tree: 'AttackTree') -> 'AttackTreeResolvedNode':
        """
        Converts a circumvent tree to a resolved node representation.
        This is useful for adding circumvent trees to the resolved attack tree.
        """
        resolved_node = AttackTreeResolvedNode()
        resolved_node.name = circumvent_tree.root_node.name
        resolved_node.referenced_node_id = circumvent_tree.id
        resolved_node.type = "CIRC"
        resolved_node.feasibility = circumvent_tree.get_feasibility()
        resolved_node.reasoning = circumvent_tree.root_node.reasoning
        resolved_node.comment = circumvent_tree.root_node.comment
        resolved_node.children = []
        return resolved_node

class AttackTreeAndNode(AttackTreeNode):
    def __init__(self, object_store: ObjectStore):
        super().__init__(object_store)
        self.name = ""
        self.type = "AND"

    def get_feasibility_without_controls(self, without_controls: bool = False) -> Feasibility:
        """
        Returns the feasibility of the AND node.
        The feasibility is calculated as the maximum feasibility of all child nodes.
        """
        if not self.children:
            raise ValueError("AND node has no children.")
        
        feasibility = self.children[0].get_feasibility(without_controls)

        for child in self.children[1:]:
            feasibility = feasibility.and_feasibility(child.get_feasibility(without_controls))
        
        return feasibility

class AttackTreeOrNode(AttackTreeNode):
    def __init__(self, object_store: ObjectStore):
        super().__init__(object_store)
        self.name = ""
        self.type = "OR"

    def get_feasibility_without_controls(self, without_controls: bool = False) -> Feasibility:
        """
        Returns the feasibility of the OR node.
        The feasibility is calculated as the minimum feasibility of all child nodes.
        """
        if not self.children:
            raise ValueError("OR node has no children.")
        
        feasibility = self.children[0].get_feasibility(without_controls)

        for child in self.children[1:]:
            feasibility = feasibility.or_feasibility(child.get_feasibility(without_controls))
        
        return feasibility

class AttackTreeLeafNode(AttackTreeNode):
    def __init__(self, feasibility: Feasibility, object_store: ObjectStore):
        super().__init__(object_store)
        self.name = ""
        self.type = "LEAF"
        self._feasibility = feasibility

    def get_feasibility_without_controls(self, without_controls: bool = False) -> Feasibility:
        """
        Returns the feasibility of the node without considering any controls.
        This is useful for calculating the base feasibility of the node.
        """
        return self._feasibility

class AttackTreeReferenceNode(AttackTreeNode):
    def __init__(self, object_store: ObjectStore):
        super().__init__(object_store)
        self.type = "REF"
        self.referenced_node_id: str = None

    def get_feasibility_without_controls(self, without_controls: bool = False) -> Feasibility:
        """
        Returns the feasibility of the referenced node.
        If the referenced node is not found, raises an error.
        """
        if self.referenced_node_id is None:
            raise ValueError("Referenced node ID is not set.")
        
        referenced_node = self.object_store.get(self.referenced_node_id)
        if referenced_node is None:
            raise ValueError(f"Referenced node with ID {self.referenced_node_id} not found.")
        
        return referenced_node.get_feasibility(without_controls)

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

    def invalidate_cache(self):
        """
        Invalidates the cached feasibility of the attack tree.
        This is useful when the tree has been modified and the feasibility needs to be recalculated.
        """
        if self.root_node:
            self.root_node.invalidate_cache()
        else:
            raise ValueError(f"Attack tree with id '{self.id}' has no root node.")

    def get_feasibility(self, without_controls: bool = False) -> Feasibility:
        """
        Returns the feasibility of the attack tree.
        This method should be overridden in subclasses to provide specific feasibility logic.
        """
        if self.root_node is None:
            raise ValueError(f"Attack tree with id '{self.id}' has no root node.")

        return self.root_node.get_feasibility(without_controls)

    def get_resolved_tree(self) -> ResolvedAttackTree:
        """
        Returns a new attack tree where each node has a resolved feasibility.
        Evaluated circumvent trees are added.
        References are updated to work within a single report document.
        """

        resolved_tree = ResolvedAttackTree(self.id)

        resolved_tree.root_node = self.root_node.get_resolved_node()
        return resolved_tree