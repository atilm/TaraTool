import unittest

from tara.domain.feasibility import *
from tara.domain.attack_tree import *
from tara.domain.util_attack_tree_test_case import AttackTreeTestCase

class TestFeasibilityCalculation(unittest.TestCase):
    def test_feasibility_level_is_determined_correctly(self):
        # Arrange
        border_test_cases = [
            # (ElapsedTime, Expertise, Knowledge, WindowOfOpportunity, Equipment, ExpectedFeasibilityLevel, ExpectedFeasibilityScore)
            (ElapsedTime.OneWeek, Expertise.Layman, Knowledge.Public, WindowOfOpportunity.Unlimited, Equipment.Standard, FeasibilityLevel.High, 0),
            (ElapsedTime.ThreeYears, Expertise.Layman, Knowledge.Restricted, WindowOfOpportunity.Unlimited, Equipment.Standard, FeasibilityLevel.High, 13),
            (ElapsedTime.ThreeYears, Expertise.Layman, Knowledge.Restricted, WindowOfOpportunity.Easy, Equipment.Standard, FeasibilityLevel.Medium, 14),
            (ElapsedTime.MoreThanThreeYears, Expertise.Layman, Knowledge.Public, WindowOfOpportunity.Unlimited, Equipment.Standard, FeasibilityLevel.Medium, 19),
            (ElapsedTime.MoreThanThreeYears, Expertise.Layman, Knowledge.Public, WindowOfOpportunity.Easy, Equipment.Standard, FeasibilityLevel.Low, 20),
            (ElapsedTime.MoreThanThreeYears, Expertise.Layman, Knowledge.Public, WindowOfOpportunity.Easy, Equipment.Specialized, FeasibilityLevel.Low, 24),
            (ElapsedTime.ThreeYears, Expertise.Layman, Knowledge.StrictlyConfidential, WindowOfOpportunity.Moderate, Equipment.Standard, FeasibilityLevel.VeryLow, 25),
        ]

        for elapsed_time, expertise, knowledge, window_of_opportunity, equipment, expected_level, expected_score in border_test_cases:
            with self.subTest(elapsed_time=elapsed_time, expertise=expertise, knowledge=knowledge,
                              window_of_opportunity=window_of_opportunity, equipment=equipment):
                feasibility = Feasibility()
                feasibility.time = elapsed_time
                feasibility.expertise = expertise
                feasibility.knowledge = knowledge
                feasibility.window_of_opportunity = window_of_opportunity
                feasibility.equipment = equipment
                
                # Act
                score = feasibility.calculate_feasibility_score()
                level = feasibility.calculate_feasibility_level()
                
                # Assert
                self.assertEqual(score, expected_score)
                self.assertEqual(level, expected_level)

    def test_applying_OR_to_feasibilities_returns_the_feasibility_with_the_lowest_score(self):
        # Arrange
        medium_feasibility = Feasibility()
        medium_feasibility.time = ElapsedTime.SixMonths
        medium_feasibility.expertise = Expertise.Proficient
        medium_feasibility.knowledge = Knowledge.Restricted
        medium_feasibility.window_of_opportunity = WindowOfOpportunity.Moderate
        medium_feasibility.equipment = Equipment.Specialized
        
        easier_feasibility = Feasibility()
        easier_feasibility.time = ElapsedTime.SixMonths
        easier_feasibility.expertise = Expertise.Proficient
        easier_feasibility.knowledge = Knowledge.Restricted
        easier_feasibility.window_of_opportunity = WindowOfOpportunity.Easy
        easier_feasibility.equipment = Equipment.Specialized
        
        # Act
        combined_feasibility = medium_feasibility.or_feasibility(easier_feasibility)
        other_combined_feasibility = easier_feasibility.or_feasibility(medium_feasibility)
        
        # Assert
        self.assertEqual(combined_feasibility, easier_feasibility)
        self.assertEqual(other_combined_feasibility, easier_feasibility)

    def test_applying_AND_to_feasibilities_returns_a_feasibility_with_per_field_max(self):
        # Arrange
        feasibility_1 = Feasibility()
        feasibility_1.time = ElapsedTime.SixMonths
        feasibility_1.expertise = Expertise.Proficient
        feasibility_1.knowledge = Knowledge.Restricted
        feasibility_1.window_of_opportunity = WindowOfOpportunity.Moderate
        feasibility_1.equipment = Equipment.Specialized
        
        feasibility_2 = Feasibility()
        feasibility_2.time = ElapsedTime.ThreeYears
        feasibility_2.expertise = Expertise.Layman
        feasibility_2.knowledge = Knowledge.Confidential
        feasibility_2.window_of_opportunity = WindowOfOpportunity.Difficult
        feasibility_2.equipment = Equipment.Bespoke
        
        # Act
        combined_feasibility = feasibility_1.and_feasibility(feasibility_2)
        other_combined_feasibility = feasibility_2.and_feasibility(feasibility_1)
        
        # Assert
        self.assertEqual(combined_feasibility.time, ElapsedTime.ThreeYears)
        self.assertEqual(combined_feasibility.expertise, Expertise.Proficient)
        self.assertEqual(combined_feasibility.knowledge, Knowledge.Confidential)
        self.assertEqual(combined_feasibility.window_of_opportunity, WindowOfOpportunity.Difficult)
        self.assertEqual(combined_feasibility.equipment, Equipment.Bespoke)

        self.assertEqual(other_combined_feasibility, combined_feasibility)       

class TestFeasibilityForAttackTrees(unittest.TestCase):
    def test_feasibility_of_a_whole_tree_is_calculated_correctly(self):
        attack_tree_description = """# ATT-1

* Node: (OR, AND, LEAF, REF)
* ET: Elapsed Time (1w, 1m, 6m, >6m)
* Ex: Expertise (L: Layman, P: Proficient, E: Expert, ME: multiple Experts)
* Kn: Knowledge (P: Public, R: Restricted, C: Confidential, SC: strictly Confidential)
* WoO: Window of Opportunity (U: Unlimited, E: Easy, M: Moderate, D: Difficult)
* Eq: Equipment (ST: Standard, SP: Specialized, B: Bespoke, mB: multiple Bespoke)

| Attack Tree    | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning   | Control | Comment   |
| -------------- | ---- | --- | --- | --- | --- | --- | ----------- | ------- | --------- |
| Root Threat    | AND  |     |     |     |     |     | Reasoning 0 |         | Comment 0 |
| -- Threat 1    |      | 1m  | P   | R   | U   | SP  | Reasoning 1 |         | Comment 1 |
| -- Threat 2    | OR   |     |     |     |     |     | Reasoning 1 |         | Comment 1 |
| ---- Threat 4  |      | 1w  | L   | C   | E   | B   | Reasoning 1 |         | Comment 1 |
| ---- Threat 5  |      | 1w  | L   | C   | D   | B   | Reasoning 1 |         | Comment 1 |
"""

        t = AttackTreeTestCase()
        tree = t.parse_attack_tree(attack_tree_description, "ATT-1")

        self.assertEqual(t.logger.get_errors(), [])
        
        # Act
        feasibility = tree.get_feasibility()

        # Assert
        # Threat 4 wins against Threat 5 in the OR-comparison,
        # so the result contains the max values of the ratings of Threat 1 and Threat 4:
        self.assertEqual(t.logger.get_errors(), [])

        expected_feasibility = Feasibility()
        expected_feasibility.time = ElapsedTime.OneMonth
        expected_feasibility.expertise = Expertise.Proficient
        expected_feasibility.knowledge = Knowledge.Confidential
        expected_feasibility.window_of_opportunity = WindowOfOpportunity.Easy
        expected_feasibility.equipment = Equipment.Bespoke

        self.assertEqual(feasibility, expected_feasibility)

    def test_reference_nodes_are_resolved_in_feasibility_calculation(self):
        referencing_tree = """# ATT-1

| Attack Tree                     | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning   | Control | Comment   |
| ------------------------------- | ---- | --- | --- | --- | --- | --- | ----------- | ------- | --------- |
| Root Threat                     | AND  |     |     |     |     |     | Reasoning 0 |         | Comment 0 |
| -- Threat 1                     |      | 1m  | P   | R   | U   | SP  | Reasoning 1 |         | Comment 1 |
| -- [Technical Tree](./TAT-1.md) | REF  |     |     |     |     |     | Reasoning 1 |         | Comment 1 |
"""

        referenced_tree = """# TAT-1

| Attack Tree    | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning   | Control | Comment   |
| -------------- | ---- | --- | --- | --- | --- | --- | ----------- | ------- | --------- |
| Threat 2       | OR   |     |     |     |     |     | Reasoning 1 |         | Comment 1 |
| -- Threat 4    |      | 1w  | L   | C   | E   | B   | Reasoning 1 |         | Comment 1 |
| -- Threat 5    |      | 1w  | L   | C   | D   | B   | Reasoning 1 |         | Comment 1 |
"""
        t = AttackTreeTestCase()
        tree = t.parse_attack_tree(referencing_tree, "ATT-1")
        _referenced_tree_obj = t.parse_attack_tree(referenced_tree, "TAT-1")

        self.assertEqual(t.logger.get_errors(), [])

        # Act
        feasibility = tree.get_feasibility()

        # Assert
        self.assertEqual(t.logger.get_errors(), [])

        expected_feasibility = Feasibility()
        expected_feasibility.time = ElapsedTime.OneMonth
        expected_feasibility.expertise = Expertise.Proficient
        expected_feasibility.knowledge = Knowledge.Confidential
        expected_feasibility.window_of_opportunity = WindowOfOpportunity.Easy
        expected_feasibility.equipment = Equipment.Bespoke

        self.assertEqual(feasibility, expected_feasibility)

    def test_for_active_controls_circumvent_trees_are_applied(self):
        t = AttackTreeTestCase()
        
        t.register_control("C-1", True)

        tree = """# ATT-1

* Node: (OR, AND, LEAF, REF)
* ET: Elapsed Time (1w, 1m, 6m, >6m)
* Ex: Expertise (L: Layman, P: Proficient, E: Expert, ME: multiple Experts)
* Kn: Knowledge (P: Public, R: Restricted, C: Confidential, SC: strictly Confidential)
* WoO: Window of Opportunity (U: Unlimited, E: Easy, M: Moderate, D: Difficult)
* Eq: Equipment (ST: Standard, SP: Specialized, B: Bespoke, mB: multiple Bespoke)

| Attack Tree | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning   | Control | Comment   |
| ----------- | ---- | --- | --- | --- | --- | --- | ----------- | ------- | --------- |
| Threat 1    |      | 1m  | P   | R   | E   | SP  |             | C-1     |           |
"""

        circ_c1 = """# CIRC_C-1

| Attack Tree         | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning   | Control | Comment   |
| ------------------- | ---- | --- | --- | --- | --- | --- | ----------- | ------- | --------- |
| Circumvent Threat 1 |      | 1w  | E   | P   | D   | ST  |             |         |           |
"""

        tree_obj = t.parse_attack_tree(tree, "ATT-1")
        circ_c1_obj = t.parse_attack_tree(circ_c1, "CIRC_C-1")

        self.assertEqual(t.logger.get_errors(), [])

        # Act
        feasibility = tree_obj.get_feasibility()

        # Assert
        self.assertEqual(t.logger.get_errors(), [])

        # Feasibility(Threat 1 with control) should be = Feasibility(Threat 1 without control) AND Feasibility(Circumvent Control 1)
        expected_feasibility = Feasibility()
        expected_feasibility.time = ElapsedTime.OneMonth
        expected_feasibility.expertise = Expertise.Expert
        expected_feasibility.knowledge = Knowledge.Restricted
        expected_feasibility.window_of_opportunity = WindowOfOpportunity.Difficult
        expected_feasibility.equipment = Equipment.Specialized

        self.assertEqual(feasibility, expected_feasibility)

    def test_controls_can_be_deactivated_through_a_parameter(self):
        t = AttackTreeTestCase()
        
        t.register_control("C-1", True)

        tree = """# ATT-1

* Node: (OR, AND, LEAF, REF)
* ET: Elapsed Time (1w, 1m, 6m, >6m)
* Ex: Expertise (L: Layman, P: Proficient, E: Expert, ME: multiple Experts)
* Kn: Knowledge (P: Public, R: Restricted, C: Confidential, SC: strictly Confidential)
* WoO: Window of Opportunity (U: Unlimited, E: Easy, M: Moderate, D: Difficult)
* Eq: Equipment (ST: Standard, SP: Specialized, B: Bespoke, mB: multiple Bespoke)

| Attack Tree | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning   | Control | Comment   |
| ----------- | ---- | --- | --- | --- | --- | --- | ----------- | ------- | --------- |
| Threat 1    |      | 1m  | P   | R   | E   | SP  |             | C-1     |           |
"""

        circ_c1 = """# CIRC_C-1

| Attack Tree         | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning   | Control | Comment   |
| ------------------- | ---- | --- | --- | --- | --- | --- | ----------- | ------- | --------- |
| Circumvent Threat 1 |      | 1w  | E   | P   | D   | ST  |             |         |           |
"""

        tree_obj = t.parse_attack_tree(tree, "ATT-1")
        circ_c1_obj = t.parse_attack_tree(circ_c1, "CIRC_C-1")

        self.assertEqual(t.logger.get_errors(), [])

        # Act
        feasibility = tree_obj.get_feasibility(without_controls=True)

        # Assert
        self.assertEqual(t.logger.get_errors(), [])

        # Feasibility(Threat 1 with control) should be = Feasibility(Threat 1 without control) AND Feasibility(Circumvent Control 1)
        expected_feasibility = Feasibility()
        expected_feasibility.time = ElapsedTime.OneMonth
        expected_feasibility.expertise = Expertise.Proficient
        expected_feasibility.knowledge = Knowledge.Restricted
        expected_feasibility.window_of_opportunity = WindowOfOpportunity.Easy
        expected_feasibility.equipment = Equipment.Specialized

        self.assertEqual(feasibility, expected_feasibility)

    def test_multiple_controls_can_be_combinded(self):
        t = AttackTreeTestCase()
        
        t.register_control("C-1", True)
        t.register_control("C-2", True)

        tree = """# ATT-1

* Node: (OR, AND, LEAF, REF)
* ET: Elapsed Time (1w, 1m, 6m, >6m)
* Ex: Expertise (L: Layman, P: Proficient, E: Expert, ME: multiple Experts)
* Kn: Knowledge (P: Public, R: Restricted, C: Confidential, SC: strictly Confidential)
* WoO: Window of Opportunity (U: Unlimited, E: Easy, M: Moderate, D: Difficult)
* Eq: Equipment (ST: Standard, SP: Specialized, B: Bespoke, mB: multiple Bespoke)

| Attack Tree | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning   | Control | Comment   |
| ----------- | ---- | --- | --- | --- | --- | --- | ----------- | ------- | --------- |
| Threat 1    |      | 1w  | L   | P   | U   | ST  |             | C-1 C-2 |           |
"""

        circ_c1 = """# CIRC_C-1

| Attack Tree         | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning   | Control | Comment   |
| ------------------- | ---- | --- | --- | --- | --- | --- | ----------- | ------- | --------- |
| Circumvent Threat 1 |      | 6m  |     |     |     |     |             |         |           |
"""

        circ_c2 = """# CIRC_C-2

| Attack Tree         | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning   | Control | Comment   |
| ------------------- | ---- | --- | --- | --- | --- | --- | ----------- | ------- | --------- |
| Circumvent Threat 2 |      |     |     |     |     | MB  |             |         |           |
"""
        tree_obj = t.parse_attack_tree(tree, "ATT-1")
        t.parse_attack_tree(circ_c1, "CIRC_C-1")
        t.parse_attack_tree(circ_c2, "CIRC_C-2")

        self.assertEqual(t.logger.get_errors(), [])

        # Act
        feasibility = tree_obj.get_feasibility()

        # Assert
        self.assertEqual(t.logger.get_errors(), [])

        # Feasibility(Threat 1 with control) should be = Feasibility(Threat 1 without control) AND Feasibility(Circumvent Control 1) AND Feasibility(Circumvent Control 2)
        expected_feasibility = Feasibility()
        expected_feasibility.time = ElapsedTime.SixMonths
        expected_feasibility.expertise = Expertise.Layman
        expected_feasibility.knowledge = Knowledge.Public
        expected_feasibility.window_of_opportunity = WindowOfOpportunity.Unlimited
        expected_feasibility.equipment = Equipment.MultipleBespoke

        self.assertEqual(feasibility, expected_feasibility)

    def test_circumvent_trees_can_be_recursively_applied(self):
        t = AttackTreeTestCase()
        
        t.register_control("C-1", True)
        t.register_control("C-2", True)

        tree = """# ATT-1

| Attack Tree | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning   | Control | Comment   |
| ----------- | ---- | --- | --- | --- | --- | --- | ----------- | ------- | --------- |
| Threat 1    |      | 1w  | L   | P   | U   | ST  |             | C-1     |           |
"""

        circ_c1 = """# CIRC_C-1

| Attack Tree         | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning   | Control | Comment   |
| ------------------- | ---- | --- | --- | --- | --- | --- | ----------- | ------- | --------- |
| Circumvent Threat 1 |      | 6m  |     |     |     |     |             | C-2     |           |
"""

        circ_c2 = """# CIRC_C-2

| Attack Tree         | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning   | Control | Comment   |
| ------------------- | ---- | --- | --- | --- | --- | --- | ----------- | ------- | --------- |
| Circumvent Threat 2 |      |     |     |     |     | MB  |             |         |           |
"""

        tree_obj = t.parse_attack_tree(tree, "ATT-1")
        t.parse_attack_tree(circ_c1, "CIRC_C-1")
        t.parse_attack_tree(circ_c2, "CIRC_C-2")

        self.assertEqual(t.logger.get_errors(), [])

        # Act
        feasibility = tree_obj.get_feasibility()

        # Assert
        self.assertEqual(t.logger.get_errors(), [])

        # Feasibility(Threat 1 with control) should be = Feasibility(Threat 1 without control) AND Feasibility(Circumvent Control 1) AND Feasibility(Circumvent Control 2)
        expected_feasibility = Feasibility()
        expected_feasibility.time = ElapsedTime.SixMonths
        expected_feasibility.expertise = Expertise.Layman
        expected_feasibility.knowledge = Knowledge.Public
        expected_feasibility.window_of_opportunity = WindowOfOpportunity.Unlimited
        expected_feasibility.equipment = Equipment.MultipleBespoke

        self.assertEqual(feasibility, expected_feasibility)

    def test_controls_can_be_applied_to_non_leaf_nodes(self):
        t = AttackTreeTestCase()
        
        t.register_control("C-1", True)
        t.register_control("C-2", True)
        t.register_control("C-3", True)

        tree = """# ATT-1

| Attack Tree                       | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning   | Control | Comment   |
| --------------------------------- | ---- | --- | --- | --- | --- | --- | ----------- | ------- | --------- |
| Threat 1                          | AND  |     |     |     |     |     |             | C-1     |           |
| -- Threat 1                       | OR   |     |     |     |     |     |             | C-2     |           |
| ---- [Technical Tree](./TAT-1.md) | REF  |     |     |     |     |     |             | C-3     |           |
"""

        technical_tree = """# TAT-1

| Attack Tree   | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning   | Control | Comment   |
| ------------- | ---- | --- | --- | --- | --- | --- | ----------- | ------- | --------- |
| Threat 1      |      | 1m  | P   | R   | E   | SP  |             |         |           |
"""

        circ_c1 = """# CIRC_C-1

| Attack Tree         | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning   | Control | Comment   |
| ------------------- | ---- | --- | --- | --- | --- | --- | ----------- | ------- | --------- |
| Circumvent Threat 1 |      | 6m  |     |     |     |     |             |         |           |
"""

        circ_c2 = """# CIRC_C-2

| Attack Tree         | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning   | Control | Comment   |
| ------------------- | ---- | --- | --- | --- | --- | --- | ----------- | ------- | --------- |
| Circumvent Threat 2 |      |     |     |     |     | MB  |             |         |           |
"""

        circ_c3 = """# CIRC_C-3

| Attack Tree         | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning   | Control | Comment   |
| ------------------- | ---- | --- | --- | --- | --- | --- | ----------- | ------- | --------- |
| Circumvent Threat 3 |      |     |     | C   |     |     |             |         |           |
"""

        tree_obj = t.parse_attack_tree(tree, "ATT-1")
        t.parse_attack_tree(technical_tree, "TAT-1")
        t.parse_attack_tree(circ_c1, "CIRC_C-1")
        t.parse_attack_tree(circ_c2, "CIRC_C-2")
        t.parse_attack_tree(circ_c3, "CIRC_C-3")

        self.assertEqual(t.logger.get_errors(), [])

        # Act
        feasibility = tree_obj.get_feasibility()

        # Assert
        self.assertEqual(t.logger.get_errors(), [])

        # Feasibility(Threat 1 with control) should be = Feasibility(Threat 1 without control) AND Feasibility(Circumvent Control 1)
        expected_feasibility = Feasibility()
        expected_feasibility.time = ElapsedTime.SixMonths
        expected_feasibility.expertise = Expertise.Proficient
        expected_feasibility.knowledge = Knowledge.Confidential
        expected_feasibility.window_of_opportunity = WindowOfOpportunity.Easy
        expected_feasibility.equipment = Equipment.MultipleBespoke

        self.assertEqual(feasibility, expected_feasibility)

    def test_inactive_controls_are_not_applied(self):
        t = AttackTreeTestCase()
        
        # Register an inactive control
        t.register_control("C-1", False)

        tree = """# ATT-1

| Attack Tree | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning   | Control | Comment   |
| ----------- | ---- | --- | --- | --- | --- | --- | ----------- | ------- | --------- |
| Threat 1    |      | 1m  | P   | R   | E   | SP  |             | C-1     |           |
"""

        circ_c1 = """# CIRC_C-1

| Attack Tree         | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning   | Control | Comment   |
| ------------------- | ---- | --- | --- | --- | --- | --- | ----------- | ------- | --------- |
| Circumvent Threat 1 |      | 1w  | E   | P   | D   | ST  |             |         |           |
"""

        tree_obj = t.parse_attack_tree(tree, "ATT-1")
        t.parse_attack_tree(circ_c1, "CIRC_C-1")

        self.assertEqual(t.logger.get_errors(), [])

        # Act
        feasibility = tree_obj.get_feasibility()

        # Assert
        self.assertEqual(t.logger.get_errors(), [])

        # The attack feasibility should be the same as if no control was applied
        expected_feasibility = Feasibility()
        expected_feasibility.time = ElapsedTime.OneMonth
        expected_feasibility.expertise = Expertise.Proficient
        expected_feasibility.knowledge = Knowledge.Restricted
        expected_feasibility.window_of_opportunity = WindowOfOpportunity.Easy
        expected_feasibility.equipment = Equipment.Specialized

        self.assertEqual(feasibility, expected_feasibility)

    def test_a_feasibility_without_controls_can_be_calculated(self):
        t = AttackTreeTestCase()
        
        t.register_control("C-1", True)
        t.register_control("C-2", True)

        tree = """# ATT-1

| Attack Tree                     | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning   | Control | Comment   |
| ------------------------------- | ---- | --- | --- | --- | --- | --- | ----------- | ------- | --------- |
| Threat 1                        | AND  |     |     |     |     |     |             | C-1     |           |
| -- Threat 2                     | OR   |     |     |     |     |     |             | C-1     |           |
| ---- Threat 3                   |      | 1w  | L   | P   | U   | ST  |             | C-1     |           |
| -- [Technical Tree](./TAT-1.md) | REF  |     |     |     |     |     |             | C-1     |           |
"""

        technical_tree = """# TAT-1
        
| Attack Tree | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning   | Control | Comment   |
| ----------- | ---- | --- | --- | --- | --- | --- | ----------- | ------- | --------- |
| Threat 5    |      | 1w  | L   | P   | U   | ST  |             | C-1     |           |
"""

        circ_c1 = """# CIRC_C-1

| Attack Tree         | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning   | Control | Comment   |
| ------------------- | ---- | --- | --- | --- | --- | --- | ----------- | ------- | --------- |
| Circumvent Threat 1 |      |     |     |     |     |     |             | C-2     |           |
"""

        circ_c2 = """# CIRC_C-2

| Attack Tree         | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning   | Control | Comment   |
| ------------------- | ---- | --- | --- | --- | --- | --- | ----------- | ------- | --------- |
| Circumvent Threat 2 |      | 6m  | ME  | C   | D   | MB  |             |         |           |
"""

        tree_obj = t.parse_attack_tree(tree, "ATT-1")
        t.parse_attack_tree(technical_tree, "TAT-1")
        t.parse_attack_tree(circ_c1, "CIRC_C-1")
        t.parse_attack_tree(circ_c2, "CIRC_C-2")

        self.assertEqual(t.logger.get_errors(), [])

        # Act
        tree_obj.invalidate_cache()
        feasibility_with_controls = tree_obj.get_feasibility()
        tree_obj.invalidate_cache()
        feasibility_without_controls = tree_obj.get_feasibility(without_controls=True)

        # Assert
        self.assertEqual(t.logger.get_errors(), [])

        # Feasibility(Threat 1 with control) should be = Feasibility(Threat 1 without control) AND Feasibility(Circumvent Control 1)
        expected_feasibility_with_controls = Feasibility()
        expected_feasibility_with_controls.time = ElapsedTime.SixMonths
        expected_feasibility_with_controls.expertise = Expertise.MultipleExperts
        expected_feasibility_with_controls.knowledge = Knowledge.Confidential
        expected_feasibility_with_controls.window_of_opportunity = WindowOfOpportunity.Difficult
        expected_feasibility_with_controls.equipment = Equipment.MultipleBespoke

        self.assertEqual(feasibility_with_controls, expected_feasibility_with_controls)

        # Feasibility(Threat 1 without control) should be = Feasibility(Threat 1 without control) AND Feasibility(Circumvent Control 1 without control)
        expected_feasibility_without_controls = Feasibility()
        expected_feasibility_without_controls.time = ElapsedTime.OneWeek
        expected_feasibility_without_controls.expertise = Expertise.Layman
        expected_feasibility_without_controls.knowledge = Knowledge.Public
        expected_feasibility_without_controls.window_of_opportunity = WindowOfOpportunity.Unlimited
        expected_feasibility_without_controls.equipment = Equipment.Standard

        self.assertEqual(feasibility_without_controls, expected_feasibility_without_controls)