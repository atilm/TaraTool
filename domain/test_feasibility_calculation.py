import unittest

from domain.feasibility import *

class TestFeasibilityCalculation(unittest.TestCase):
    def test_feasibility_level_is_determined_correctly(self):
        # Arrange
        test_cases = [
            # (ElapsedTime, Expertise, Knowledge, WindowOfOpportunity, Equipment, ExpectedFeasibilityLevel, ExpectedFeasibilityScore)
            (ElapsedTime.OneWeek, Expertise.Layman, Knowledge.Public, WindowOfOpportunity.Unlimited, Equipment.Standard, FeasibilityLevel.High, 0),
            (ElapsedTime.ThreeYears, Expertise.Layman, Knowledge.Restricted, WindowOfOpportunity.Unlimited, Equipment.Standard, FeasibilityLevel.High, 13),
            (ElapsedTime.ThreeYears, Expertise.Layman, Knowledge.Restricted, WindowOfOpportunity.Easy, Equipment.Standard, FeasibilityLevel.Medium, 14),
            (ElapsedTime.MoreThanThreeYears, Expertise.Layman, Knowledge.Public, WindowOfOpportunity.Unlimited, Equipment.Standard, FeasibilityLevel.Medium, 19),
            (ElapsedTime.MoreThanThreeYears, Expertise.Layman, Knowledge.Public, WindowOfOpportunity.Easy, Equipment.Standard, FeasibilityLevel.Low, 20),
            (ElapsedTime.MoreThanThreeYears, Expertise.Layman, Knowledge.Public, WindowOfOpportunity.Easy, Equipment.Specialized, FeasibilityLevel.Low, 24),
            (ElapsedTime.ThreeYears, Expertise.Layman, Knowledge.StrictlyConfidential, WindowOfOpportunity.Moderate, Equipment.Standard, FeasibilityLevel.VeryLow, 25),
        ]

        for elapsed_time, expertise, knowledge, window_of_opportunity, equipment, expected_level, expected_score in test_cases:
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