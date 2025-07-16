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
        resolved_trees = []
        tree.get_feasibility(resolved_trees)

        # Assert
        self.assertEqual(len(resolved_trees), 1)
        resolved_tree = resolved_trees[0]
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
                         
    def test_only_active_controls_are_copied_into_resolved_tree(self):
        attack_tree_description = """# ATT-1

| Attack Tree    | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning   | Control | Comment   |
| -------------- | ---- | --- | --- | --- | --- | --- | ----------- | ------- | --------- |
| Root Threat    |      | 1w  | L   | P   | U   | ST  | Reasoning 0 | C-1 C-2 | Comment 0 |
"""

        c1_description = """# CIRC_C-1

| Attack Tree    | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning   | Control | Comment   |
| -------------- | ---- | --- | --- | --- | --- | --- | ----------- | ------- | --------- |
| Circ. Threat   |      | 1m  | E   | R   | E   | ST  | Reasoning 0 |         | Comment 0 |
"""
        c2_description = """# CIRC_C-2

| Attack Tree    | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning   | Control | Comment   |
| -------------- | ---- | --- | --- | --- | --- | --- | ----------- | ------- | --------- |
| Circ. Threat   |      | 1m  | E   | R   | E   | ST  | Reasoning 0 |         | Comment 0 |
"""

        t = AttackTreeTestCase()
        t.register_control("C-1", False)
        t.register_control("C-2", True)
        tree = t.parse_attack_tree(attack_tree_description, "ATT-1")
        t.parse_attack_tree(c1_description, "CIRC_C-1")
        t.parse_attack_tree(c2_description, "CIRC_C-2")

        self.assertEqual(t.logger.errors, [])

        # Act
        resolved_trees = []
        tree.get_feasibility(resolved_trees)

        # Assert
        self.assertEqual(len(resolved_trees), 1)
        resolved_tree = resolved_trees[0]
        self.assertEqual(resolved_tree.root_node.security_control_ids, ["C-2"])

    def test_for_active_controls_the_circumvent_tree_is_used(self):
        attack_tree_description = """# ATT-1

| Attack Tree    | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning   | Control | Comment   |
| -------------- | ---- | --- | --- | --- | --- | --- | ----------- | ------- | --------- |
| Root Threat    |      | 1w  | L   | P   | U   | ST  | Reasoning 0 | C-1 C-2 | Comment 0 |
"""

        c1_description = """# CIRC_C-1

| Attack Tree    | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning   | Control | Comment   |
| -------------- | ---- | --- | --- | --- | --- | --- | ----------- | ------- | --------- |
| Circ. Threat 1 |      | 1m  | E   | R   | E   | ST  | Reasoning 0 |         | Comment 0 |
"""
        c2_description = """# CIRC_C-2

| Attack Tree    | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning   | Control | Comment   |
| -------------- | ---- | --- | --- | --- | --- | --- | ----------- | ------- | --------- |
| Circ. Threat 2 |      | 1m  | E   | R   | E   | ST  | Reasoning 0 |         | Comment 0 |
"""

        t = AttackTreeTestCase()
        t.register_control("C-1", True)
        t.register_control("C-2", True)
        tree = t.parse_attack_tree(attack_tree_description, "ATT-1")
        c1_tree = t.parse_attack_tree(c1_description, "CIRC_C-1")
        c2_tree = t.parse_attack_tree(c2_description, "CIRC_C-2")

        # Act
        resolved_trees = []
        tree.get_feasibility(resolved_trees)

        # Assert
        self.assertEqual(len(resolved_trees), 1)
        resolved_tree = resolved_trees[0]

        # There is an AND node inserted into the tree
        self.assertEqual(resolved_tree.root_node.type, "AND")
        self.assertEqual(resolved_tree.root_node.name, "Controlled Root Threat")
        self.assertEqual(resolved_tree.root_node.feasibility, tree.get_feasibility())
        self.assertEqual(len(resolved_tree.root_node.children), 3)
        self.assertEqual(resolved_tree.root_node.children[0].name, "Root Threat")
        self.assertEqual(resolved_tree.root_node.children[0].type, "LEAF")
        self.assertEqual(resolved_tree.root_node.children[0].feasibility, tree.root_node.get_feasibility_without_controls())
        self.assertEqual(resolved_tree.root_node.children[1].name, "Circ. Threat 1")
        self.assertEqual(resolved_tree.root_node.children[1].type, "CIRC")
        self.assertEqual(resolved_tree.root_node.children[1].feasibility, c1_tree.root_node.get_feasibility())
        self.assertEqual(resolved_tree.root_node.children[2].name, "Circ. Threat 2")
        self.assertEqual(resolved_tree.root_node.children[2].type, "CIRC")
        self.assertEqual(resolved_tree.root_node.children[2].feasibility, c2_tree.root_node.get_feasibility())

    def test_controls_on_ref_nodes_are_handled_correctly(self):
        tree = """# ATT-1

| Attack Tree                       | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning   | Control | Comment   |
| --------------------------------- | ---- | --- | --- | --- | --- | --- | ----------- | ------- | --------- |
| Root threat                       | AND  |     |     |     |     |     |             |         |           |
| -- [Technical Tree](./TAT-1.md)   | REF  |     |     |     |     |     |             | C-1     |           |
"""

        technical_tree = """# TAT-1

| Attack Tree   | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning   | Control | Comment   |
| ------------- | ---- | --- | --- | --- | --- | --- | ----------- | ------- | --------- |
| Threat 1      |      | 1m  | P   | R   | E   | SP  |             |         |           |
"""

        c1_description = """# CIRC_C-1

| Attack Tree    | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning   | Control | Comment   |
| -------------- | ---- | --- | --- | --- | --- | --- | ----------- | ------- | --------- |
| Circ. Threat 1 |      | 6m  | E   | C   | D   | ST  | Reasoning 0 |         | Comment 0 |
"""
        t = AttackTreeTestCase()
        t.register_control("C-1", True)
        tree = t.parse_attack_tree(tree, "ATT-1")
        technical_tree = t.parse_attack_tree(technical_tree, "TAT-1")
        t.parse_attack_tree(c1_description, "CIRC_C-1")

        # Act
        resolved_trees = []
        tree.get_feasibility(resolved_trees)

        self.assertEqual(len(resolved_trees), 1)
        resolved_tree = resolved_trees[0]

        self.assertEqual(t.logger.errors, [])
        self.assertEqual(t.logger.warnings, [])

        # Assert
        self.assertEqual(resolved_tree.root_node.name, "Root threat")
        self.assertEqual(resolved_tree.root_node.type, "AND")
        self.assertEqual(len(resolved_tree.root_node.children), 1)
        controlled_node = resolved_tree.root_node.children[0]
        self.assertIsInstance(controlled_node, AttackTreeResolvedNode)
        self.assertEqual(controlled_node.name, "Controlled Technical Tree")
        self.assertEqual(controlled_node.type, "AND")
        self.assertEqual(len(controlled_node.children), 2)
        ref_node = controlled_node.children[0]
        self.assertEqual(ref_node.name, "Technical Tree")
        self.assertEqual(ref_node.type, "REF")
        self.assertEqual(ref_node.referenced_node_id, "TAT-1")
        circ_node = controlled_node.children[1]
        self.assertEqual(circ_node.name, "Circ. Threat 1")
        self.assertEqual(circ_node.type, "CIRC")