import unittest

from domain.feasibility import *
from domain.attack_tree_parser import AttackTreeParser
from domain.attack_tree import *
from utilities.error_logger import MemoryErrorLogger
from MarkdownLib.markdown_parser import MarkdownParser, MarkdownDocument, MarkdownTable

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

    def test_applying_AND_to_feasibilities_returns_a_feasibility_with_per_fiel_max(self):
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

        parser = MarkdownParser()
        document: MarkdownDocument = parser.parse(attack_tree_description)

        table = document.getContent()[1]
        self.assertIsInstance(table, MarkdownTable)

        logger: MemoryErrorLogger = MemoryErrorLogger()
        att_parser = AttackTreeParser(logger)
        tree = att_parser.parse_attack_tree(table, "ATT-1")

        self.assertEqual(logger.get_errors(), [])
        
        # Act
        feasibility = tree.get_feasibility()

        # Assert
        # Threat 4 wins against Threat 5 in the OR-comparison,
        # so the result contains the max values of the ratings of Threat 1 and Threat 4:
        self.assertEqual(logger.get_errors(), [])

        expected_feasibility = Feasibility()
        expected_feasibility.time = ElapsedTime.OneMonth
        expected_feasibility.expertise = Expertise.Proficient
        expected_feasibility.knowledge = Knowledge.Confidential
        expected_feasibility.window_of_opportunity = WindowOfOpportunity.Easy
        expected_feasibility.equipment = Equipment.Bespoke

        self.assertEqual(feasibility, expected_feasibility)
