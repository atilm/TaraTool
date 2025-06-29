import unittest
from tara.domain.feasibility import Feasibility
from tara.domain.attack_tree import AttackTree, AttackTreeResolvedNode
from tara.domain.util_attack_tree_test_case import AttackTreeTestCase

class TestCase(unittest.TestCase):
    def test_the_feasibilities_of_parent_nodes_are_resolved(self):
        # self.fail("This test is not implemented yet.")

        attack_tree_description = """# ATT-1

| Attack Tree    | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning   | Control | Comment   |
| -------------- | ---- | --- | --- | --- | --- | --- | ----------- | ------- | --------- |
| Root Threat    | AND  |     |     |     |     |     | Reasoning 0 |         | Comment 0 |
| -- Threat 1    |      | 1m  | P   | R   | U   | SP  | Reasoning 1 |         | Comment 1 |
| -- Threat 2    | OR   |     |     |     |     |     | Reasoning 1 |         | Comment 1 |
| ---- Threat 3  |      | 1w  | L   | C   | E   | B   | Reasoning 1 |         | Comment 1 |
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

        self.fail("to be continued...")