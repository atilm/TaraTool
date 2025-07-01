import unittest
from tara.domain.feasibility import Feasibility
from tara.domain.attack_tree import AttackTree, AttackTreeResolvedNode
from tara.domain.util_attack_tree_test_case import AttackTreeTestCase

class TestCase(unittest.TestCase):
    def test_the_feasibilities_of_parent_nodes_are_resolved(self):

        attack_tree_description = """# ATT-1

| Attack Tree    | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning   | Control | Comment   |
| -------------- | ---- | --- | --- | --- | --- | --- | ----------- | ------- | --------- |
| Root Threat    | AND  |     |     |     |     |     | Reasoning 0 |         | Comment 0 |
| -- Threat 1    |      | 1m  | P   | R   | U   | SP  | Reasoning 1 |         | Comment 1 |
| -- Threat 2    | OR   |     |     |     |     |     | Reasoning 2 |         | Comment 2 |
| ---- Threat 3  |      | 1w  | L   | C   | E   | B   | Reasoning 3 |         | Comment 3 |
"""

        t = AttackTreeTestCase()
        tree = t.parse_attack_tree(attack_tree_description, "ATT-1")

        # Act
        resolved_tree = tree.get_resolved_tree()

        # Assert
        self.assertEqual(resolved_tree.id, "ATT-1")
        self.assertIsInstance(resolved_tree.root_node, AttackTreeResolvedNode)
        self.assertEqual(resolved_tree.root_node.name, "Root Threat")
        self.assertEqual(resolved_tree.root_node.type, "AND")
        self.assertEqual(resolved_tree.root_node.reasoning, "Reasoning 0")
        self.assertEqual(resolved_tree.root_node.comment, "Comment 0")

        self.assertEqual(resolved_tree.root_node.feasibility, tree.get_feasibility())

        self.assertEqual(len(resolved_tree.root_node.children), 2)
        self.assertEqual(resolved_tree.root_node.children[0].name, "Threat 1")
        self.assertEqual(resolved_tree.root_node.children[0].type, "LEAF")
        self.assertEqual(resolved_tree.root_node.children[0].feasibility, tree.root_node.children[0].get_feasibility())
        self.assertEqual(resolved_tree.root_node.children[0].reasoning, "Reasoning 1")
        self.assertEqual(resolved_tree.root_node.children[0].comment, "Comment 1")
        self.assertEqual(resolved_tree.root_node.children[1].name, "Threat 2")
        self.assertEqual(resolved_tree.root_node.children[1].type, "OR")
        self.assertEqual(resolved_tree.root_node.children[1].feasibility, tree.root_node.children[1].get_feasibility())
        self.assertEqual(resolved_tree.root_node.children[1].reasoning, "Reasoning 2")
        self.assertEqual(resolved_tree.root_node.children[1].comment, "Comment 2")
        self.assertEqual(len(resolved_tree.root_node.children[1].children), 1)
        self.assertEqual(resolved_tree.root_node.children[1].children[0].name, "Threat 3")
        self.assertEqual(resolved_tree.root_node.children[1].children[0].type, "LEAF")
        self.assertEqual(resolved_tree.root_node.children[1].children[0].feasibility, tree.root_node.children[1].children[0].get_feasibility())
        self.assertEqual(resolved_tree.root_node.children[1].children[0].reasoning, "Reasoning 3")
        self.assertEqual(resolved_tree.root_node.children[1].children[0].comment, "Comment 3")
                         
