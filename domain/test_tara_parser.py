import unittest, os
from domain.tara_parser import TaraParser
from domain.file_stubs import FileType
from domain.impacts import ImpactCategory, Impact
from domain.security_property import SecurityProperty
from domain.feasibility import *
from domain.attack_tree import *
from utilities.file_reader import MockFileReader
from utilities.error_logger import MemoryErrorLogger

class TestCase:
    def __init__(self):
        self.directory = "mock_directory"
        self.logger = MemoryErrorLogger()
        self.mock_reader = MockFileReader()
        self.mock_reader.setup_file(os.path.join(self.directory, FileType.to_path(FileType.ASSUMPTIONS)),
"""# Assumptions

| ID    | Name | Security Claim | Comment |
| ----- | ---- | -------------- | ------- |
| Ast-1 | abc  | def            | ghi     |
| Ast-2 | jkl  | mno            | pqr     |
""")
        self.mock_reader.setup_file(os.path.join(self.directory, FileType.to_path(FileType.DAMAGE_SCENARIOS)),
"""# Damage Scenarios

| ID   | Name                | Safety     | Operational | Financial | Privacy    | Reasoning | Comment   |
| ---- | ------------------- | ---------- | ----------- | --------- | ---------- | --------- | --------- |
| DS-1 | Electrocuted person | Severe     | Major       | Moderate  | Negligible | Reason 1  | Comment 1 |
| DS-2 | Litigation          |            |             | Major     |            | Reason 2  | Comment 2 |
""")
        self.mock_reader.setup_file(os.path.join(self.directory, FileType.to_path(FileType.ASSETS)),
"""# Assets

| ID  | Name    | Availability | Integrity | Confidentiality | Reasoning   | Description   |
| --- | ------- | ------------ | --------- | --------------- | ----------- | ------------- |
| A-1 | Asset 1 | DS-1         | DS-2      | DS-1 DS-2       | Reasoning 1 | Description 1 |
| A-2 | Asset 2 |              | DS-2 DS-1 | DS-2            | Reasoning 2 | Description 2 |
""")
        
        default_attack_tree = """# {0}

* Node: (OR, AND, LEAF, REF)
* ET: Elapsed Time (1w, 1m, 6m, >6m)
* Ex: Expertise (L: Layman, P: Proficient, E: Expert, mE: multiple Experts)
* Kn: Knowledge (P: Public, R: Restricted, C: Confidential, sC: strictly Confidential)
* WoO: Window of Opportunity (U: Unlimited, E: Easy, M: Moderate, D: Difficult)
* Eq: Equipment (St: Standard, Sp: Specialized, B: Bespoke, mB: multiple Bespoke)

| Attack Tree    | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning   | Control | Comment   |
| -------------- | ---- | --- | --- | --- | --- | --- | ----------- | ------- | --------- |
| Root Threat    | OR   |     |     |     |     |     | Reasoning 0 |         | Comment 0 |
| -- Threat 1    | LEAF | 1w  | L   | P   | U   | ST  | Reasoning 1 |         | Comment 1 |
| -- Threat 2    | LEAF | 1m  | P   | R   | E   | SP  | Reasoning 2 |         | Comment 2 |
| -- Threat 3    |      | 6m  | E   | C   | M   | B   | Reasoning 3 |         | Comment 3 |
| -- Threat 4    |      | 3y  | ME  | SC  | D   | MB  | Reasoning 4 |         | Comment 4 |
| -- Threat 5    |      | >3y | L   | P   | U   | ST  | Reasoning 5 |         | Comment 5 |"""

        attack_tree_ids = [
            "AT_A-1_BLOCK",
            "AT_A-1_MAN",
            "AT_A-1_EXT",
            "AT_A-2_MAN",
            "AT_A-2_EXT",
        ]

        for attack_tree_id in attack_tree_ids:
            attack_tree_file_path = os.path.join(self.directory, "AttackTrees", f"{attack_tree_id}.md")
            attack_tree_file_content = default_attack_tree.format(attack_tree_id)
            self.mock_reader.setup_file(attack_tree_file_path, attack_tree_file_content)

        self.parser = TaraParser(self.mock_reader, self.logger)
        


class TaraParserTests(unittest.TestCase):
    def test_parse_valid_files(self):
        # Arrange
        test_case = TestCase()
        parser = test_case.parser

        # Act
        tara = parser.parse(test_case.directory)

        # Assert
        self.assertEqual(len(tara.assumptions), 2)
        
        self.assertEqual(tara.assumptions[0].id, "Ast-1")
        self.assertEqual(tara.assumptions[0].name, "abc")
        self.assertEqual(tara.assumptions[0].security_claim, "def")
        self.assertEqual(tara.assumptions[0].comment, "ghi")

        self.assertEqual(tara.assumptions[1].id, "Ast-2")
        self.assertEqual(tara.assumptions[1].name, "jkl")
        self.assertEqual(tara.assumptions[1].security_claim, "mno")
        self.assertEqual(tara.assumptions[1].comment, "pqr")
        
        self.assertEqual(len(tara.damage_scenarios), 2)
        self.assertEqual(tara.damage_scenarios[0].id, "DS-1")
        self.assertEqual(tara.damage_scenarios[0].name, "Electrocuted person")
        self.assertEqual(tara.damage_scenarios[0].impacts[ImpactCategory.Safety], Impact.Severe)
        self.assertEqual(tara.damage_scenarios[0].impacts[ImpactCategory.Operational], Impact.Major)
        self.assertEqual(tara.damage_scenarios[0].impacts[ImpactCategory.Financial], Impact.Moderate)
        self.assertEqual(tara.damage_scenarios[0].impacts[ImpactCategory.Privacy], Impact.Negligible)
        self.assertEqual(tara.damage_scenarios[0].reasoning, "Reason 1")
        self.assertEqual(tara.damage_scenarios[0].comment, "Comment 1")

        self.assertEqual(tara.damage_scenarios[1].id, "DS-2")
        self.assertEqual(tara.damage_scenarios[1].name, "Litigation")
        self.assertEqual(tara.damage_scenarios[1].impacts[ImpactCategory.Safety], Impact.Negligible)
        self.assertEqual(tara.damage_scenarios[1].impacts[ImpactCategory.Operational], Impact.Negligible)
        self.assertEqual(tara.damage_scenarios[1].impacts[ImpactCategory.Financial], Impact.Major)
        self.assertEqual(tara.damage_scenarios[1].impacts[ImpactCategory.Privacy], Impact.Negligible)
        self.assertEqual(tara.damage_scenarios[1].reasoning, "Reason 2")
        self.assertEqual(tara.damage_scenarios[1].comment, "Comment 2")
        
        self.assertEqual(len(tara.assets), 2)
        self.assertEqual(tara.assets[0].id, "A-1")
        self.assertEqual(tara.assets[0].name, "Asset 1")
        self.assertEqual(tara.assets[0].description, "Description 1")
        self.assertEqual(tara.assets[0].reasoning, "Reasoning 1")
        self.assertEqual(tara.assets[0].damage_scenarios[SecurityProperty.Availability][0], "DS-1")
        self.assertEqual(tara.assets[0].damage_scenarios[SecurityProperty.Integrity][0], "DS-2")
        self.assertEqual(tara.assets[0].damage_scenarios[SecurityProperty.Confidentiality][0], "DS-1")
        self.assertEqual(tara.assets[0].damage_scenarios[SecurityProperty.Confidentiality][1], "DS-2")
        self.assertEqual(tara.assets[1].id, "A-2")
        self.assertEqual(tara.assets[1].name, "Asset 2")
        self.assertEqual(tara.assets[1].description, "Description 2")
        self.assertEqual(tara.assets[1].reasoning, "Reasoning 2")
        self.assertEqual(tara.assets[1].damage_scenarios[SecurityProperty.Availability], [])
        self.assertEqual(tara.assets[1].damage_scenarios[SecurityProperty.Integrity][0], "DS-2")
        self.assertEqual(tara.assets[1].damage_scenarios[SecurityProperty.Integrity][1], "DS-1")
        self.assertEqual(tara.assets[1].damage_scenarios[SecurityProperty.Confidentiality][0], "DS-2")
        
        self.assertEqual(len(tara.attack_trees), 5)
        root_node_0 = tara.attack_trees[0].root_node

        self.assertIsInstance(root_node_0, AttackTreeOrNode)
        self.assertEqual(len(root_node_0.children), 5)
        self.assert_feasibility(root_node_0.children[0],
                        ElapsedTime.OneWeek,
                        Expertise.Layman,
                        Knowledge.Public,
                        WindowOfOpportunity.Unlimited,
                        Equipment.Standard)
        self.assert_feasibility(root_node_0.children[1],
                        ElapsedTime.OneMonth,
                        Expertise.Proficient,
                        Knowledge.Restricted,
                        WindowOfOpportunity.Easy,
                        Equipment.Specialized)
        self.assert_feasibility(root_node_0.children[2],
                        ElapsedTime.SixMonths,
                        Expertise.Expert,
                        Knowledge.Confidential,
                        WindowOfOpportunity.Moderate,
                        Equipment.Bespoke)
        self.assert_feasibility(root_node_0.children[3],
                        ElapsedTime.ThreeYears,
                        Expertise.MultipleExperts,
                        Knowledge.StrictlyConfidential,
                        WindowOfOpportunity.Difficult,
                        Equipment.MultipleBespoke)
        self.assert_feasibility(root_node_0.children[4],
                        ElapsedTime.MoreThanThreeYears,
                        Expertise.Layman,
                        Knowledge.Public,
                        WindowOfOpportunity.Unlimited,
                        Equipment.Standard)


        self.assertEqual(root_node_0.reasoning, "Reasoning 0")
        self.assertEqual(root_node_0.comment, "Comment 0")
        self.assertEqual(root_node_0.children[0].reasoning, "Reasoning 1")
        self.assertEqual(root_node_0.children[0].comment, "Comment 1")


    def assert_feasibility(self, node: AttackTreeNode, time, expertise, knowledge, woOpportunity, equipement):
        expected_feasibility = Feasibility()
        expected_feasibility.time = time
        expected_feasibility.expertise = expertise
        expected_feasibility.knowledge = knowledge
        expected_feasibility.window_of_opportunity = woOpportunity
        expected_feasibility.equipment = equipement
        
        self.assertEqual(node.get_feasibility(), expected_feasibility)


    def test_error_missing_assumptions_table(self):
        # Arrange
        default_test_case = TestCase()
        directory = default_test_case.directory
        default_test_case.mock_reader.setup_file(os.path.join(directory, FileType.to_path(FileType.ASSUMPTIONS)),
"""# Assumptions

| ID    | Name |
| ----- | ---- |
| Ast-1 | abc  |
| Ast-2 | jkl  |
""")

        # Act
        tara = default_test_case.parser.parse(directory)
        
        # Assert
        self.assertEqual(len(tara.assumptions), 0)
        self.assertEqual(len(default_test_case.logger.get_errors()), 1)
        self.assertIn("ASSUMPTIONS table not found in the document.", default_test_case.logger.get_errors()[0])

    def test_error_duplicate_assumption_ids(self):
        # Arrange
        default_test_case = TestCase()
        default_test_case.mock_reader.setup_file(os.path.join(default_test_case.directory, FileType.to_path(FileType.ASSUMPTIONS)),
"""# Assumptions

| ID    | Name | Security Claim | Comment |
| ----- | ---- | -------------- | ------- |
| Ast-1 | abc  | def            | ghi     |
| Ast-1 | jkl  | mno            | pqr     |
""")

        # Act
        tara = default_test_case.parser.parse(default_test_case.directory)

        # Assert
        self.assertEqual(len(tara.assumptions), 2)
        self.assertEqual(len(default_test_case.logger.get_errors()), 1)
        self.assertIn("Duplicate ID found: Ast-1", default_test_case.logger.get_errors()[0])

    def test_only_exising_impact_values_are_accepted(self):
        # Arrange
        default_test_case = TestCase()
        default_test_case.mock_reader.setup_file(os.path.join(default_test_case.directory, FileType.to_path(FileType.DAMAGE_SCENARIOS)),
"""# Damage Scenarios

| ID   | Name                | Safety     | Operational | Financial | Privacy    | Reasoning | Comment   |
| ---- | ------------------- | ---------- | ----------- | --------- | ---------- | --------- | --------- |
| DS-1 | Electrocuted person | Sever      | major       | oderate   | NEGLIGIBLE | Reason 1  | Comment 1 |
| DS-2 | Litigation          |            |             | Major     |            | Reason 2  | Comment 2 |
""")
        # Act
        tara = default_test_case.parser.parse(default_test_case.directory)

        # Assert
        self.assertEqual(len(tara.damage_scenarios), 2)
        self.assertEqual(tara.damage_scenarios[0].impacts[ImpactCategory.Safety], Impact.Severe)
        self.assertEqual(tara.damage_scenarios[0].impacts[ImpactCategory.Operational], Impact.Severe)
        self.assertEqual(tara.damage_scenarios[0].impacts[ImpactCategory.Financial], Impact.Severe)
        self.assertEqual(tara.damage_scenarios[0].impacts[ImpactCategory.Privacy], Impact.Severe)
        self.assertEqual(len(default_test_case.logger.get_errors()), 4)
        self.assertIn("Invalid impact rating found: Sever", default_test_case.logger.get_errors()[0])
        self.assertIn("Invalid impact rating found: major", default_test_case.logger.get_errors()[1])
        self.assertIn("Invalid impact rating found: oderate", default_test_case.logger.get_errors()[2])
        self.assertIn("Invalid impact rating found: NEGLIGIBLE", default_test_case.logger.get_errors()[3])

    def test_damage_scenario_ids_are_checked_for_duplication(self):
        # Arrange
        default_test_case = TestCase()
        default_test_case.mock_reader.setup_file(os.path.join(default_test_case.directory, FileType.to_path(FileType.DAMAGE_SCENARIOS)),
"""# Damage Scenarios

| ID    | Name                | Safety     | Operational | Financial | Privacy    | Reasoning | Comment   |
| ----- | ------------------- | ---------- | ----------- | --------- | ---------- | --------- | --------- |
| Ast-1 | ID from Assumptions | Severe     | Major       | Moderate  | Negligible | Reason 1  | Comment 1 |
| DS-1  | Electrocuted person | Severe     | Major       | Moderate  | Negligible | Reason 1  | Comment 1 |
| DS-1  | Litigation          | Negligible | Negligible  | Major     | Negligible | Reason 2  | Comment 2 |
| DS-2  | Litigation          |            |             | Major     |            | Reason 2  | Comment 2 |
""")
        # Act
        tara = default_test_case.parser.parse(default_test_case.directory)

        # Assert
        self.assertEqual(len(tara.damage_scenarios), 4)
        self.assertEqual(len(default_test_case.logger.get_errors()), 2)
        self.assertIn("Duplicate ID found: Ast-1", default_test_case.logger.get_errors()[0])
        self.assertIn("Duplicate ID found: DS-1", default_test_case.logger.get_errors()[1])

    def test_asset_ids_are_checked_for_duplication(self):
        # Arrange
        default_test_case = TestCase()
        default_test_case.mock_reader.setup_file(os.path.join(default_test_case.directory, FileType.to_path(FileType.ASSETS)),
 """# Assets

| ID  | Name    | Availability | Integrity | Confidentiality | Reasoning   | Description   |
| --- | ------- | ------------ | --------- | --------------- | ----------- | ------------- |
| A-1 | Asset 1 | DS-1         | DS-2      | DS-1 DS-2       | Reasoning 1 | Description 1 |
| A-1 | Asset 2 |              | DS-2 DS-1 | DS-2            | Reasoning 2 | Description 2 |
""")       
        # Act
        tara = default_test_case.parser.parse(default_test_case.directory)

        # Assert
        self.assertEqual(len(tara.assets), 2)
        self.assertEqual(len(default_test_case.logger.get_errors()), 3)
        self.assertIn("Duplicate ID found: A-1", default_test_case.logger.get_errors()[0])
        # Duplicated attack tree IDs follow from the duplicated asset ID
        self.assertIn("Duplicate ID found: AT_A-1_MAN", default_test_case.logger.get_errors()[1])
        self.assertIn("Duplicate ID found: AT_A-1_EXT", default_test_case.logger.get_errors()[2])

    def test_assets_only_link_to_existing_damage_scenarios(self):
        # Arrange
        default_test_case = TestCase()
        default_test_case.mock_reader.setup_file(os.path.join(default_test_case.directory, FileType.to_path(FileType.ASSETS)),
 """# Assets

| ID  | Name    | Availability | Integrity | Confidentiality | Reasoning   | Description   |
| --- | ------- | ------------ | --------- | --------------- | ----------- | ------------- |
| A-1 | Asset 1 | DS-3         | DS-2      | DS-1 DS-2       | Reasoning 1 | Description 1 |
| A-2 | Asset 2 |              | DS-2 DS-4 | Ast-1           | Reasoning 2 | Description 2 |
""")       
        # Act
        tara = default_test_case.parser.parse(default_test_case.directory)

        # Assert
        self.assertEqual(len(tara.assets), 2)
        self.assertEqual(len(default_test_case.logger.get_errors()), 3)
        self.assertIn("Damage scenario DS-3 referenced by asset A-1 does not exist.", default_test_case.logger.get_errors()[0])
        self.assertIn("Damage scenario DS-4 referenced by asset A-2 does not exist.", default_test_case.logger.get_errors()[1])
        self.assertIn("ID Ast-1 referenced by asset A-2 is not a damage scenario.", default_test_case.logger.get_errors()[2])
