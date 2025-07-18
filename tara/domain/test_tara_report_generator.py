import os
import unittest
from tara.utilities.file_reader import MockFileReader
from tara.utilities.error_logger import MemoryErrorLogger
from tara.domain.file_stubs import FileType
from tara.domain.tara_parser import TaraParser
from tara.domain.tara_document_generator import TaraDocumentGenerator
from tara.MarkdownLib.markdown_document import *

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
| A-1 | Asset 1 | DS-1         | DS-2      |                 | Reasoning 1 | Description 1 |
| A-2 | Asset 2 |              | DS-2      | DS-2            | Reasoning 2 | Description 2 |
""")
        self.mock_reader.setup_file(os.path.join(self.directory, FileType.to_path(FileType.CONTROLS)),
"""# Controls

| ID  | Name      | Security Goal | Active |
| --- | --------- | ------------- | ------ |
| C-1 | Control 1 | Goal-1        | x      |
| C-2 | Control 2 | Goal-1        | x      |
""")
        
        # self.mock_reader.setup_file(os.path.join(self.directory, "AttackTrees", "k.md"),
        circ_c1 = """# CIRC_C-1

* Node: (OR, AND, LEAF, REF)
* ET: Elapsed Time (1w, 1m, 6m, 3y, >3y)
* Ex: Expertise (L: Layman, P: Proficient, E: Expert, ME: multiple Experts)
* Kn: Knowledge (P: Public, R: Restricted, C: Confidential, SC: strictly Confidential)
* WoO: Window of Opportunity (U: Unlimited, E: Easy, M: Moderate, D: Difficult)
* Eq: Equipment (ST: Standard, SP: Specialized, B: Bespoke, MB: multiple Bespoke)

| Attack Tree            | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning   | Control | Comment   |
| ---------------------- | ---- | --- | --- | --- | --- | --- | ----------- | ------- | --------- |
| Circumvent Control 1   | AND  |     |     |     |     |     |             |         |           |
| -- Circ Threat 1       |      | 1m  | E   | R   | E   | SP  |             |         |           |"""

        circ_c2 = """# CIRC_C-2

* Node: (OR, AND, LEAF, REF)
* ET: Elapsed Time (1w, 1m, 6m, 3y, >3y)
* Ex: Expertise (L: Layman, P: Proficient, E: Expert, ME: multiple Experts)
* Kn: Knowledge (P: Public, R: Restricted, C: Confidential, SC: strictly Confidential)
* WoO: Window of Opportunity (U: Unlimited, E: Easy, M: Moderate, D: Difficult)
* Eq: Equipment (ST: Standard, SP: Specialized, B: Bespoke, MB: multiple Bespoke)

| Attack Tree            | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning   | Control | Comment   |
| ---------------------- | ---- | --- | --- | --- | --- | --- | ----------- | ------- | --------- |
| Circumvent Control 2   | OR   |     |     |     |     |     |             |         |           |
| -- Circ Threat 2       |      | >3y | ME  | C   | M   |  B  |             |         |           |"""
        
        at_a_1_block = """# {0}

| Attack Tree         | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning   | Control | Comment   |
| ------------------- | ---- | --- | --- | --- | --- | --- | ----------- | ------- | --------- |
| Blocking of Asset 1 | OR   |     |     |     |     |     | Reasoning 0 |         | Comment 0 |
| -- Threat 1         | LEAF | 6m  | P   | R   | M   | ST  | Reasoning 1 | C-1     | Comment 1 |
"""

        at_a_1_man = """# {0}

| Attack Tree                   | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning   | Control | Comment   |
| ----------------------------- | ---- | --- | --- | --- | --- | --- | ----------- | ------- | --------- |
| Manipulation of Asset 1       | OR   |     |     |     |     |     | Reasoning 0 |         | Comment 0 |
| -- [Threat 1](./TAT_TREE.md)  | REF  |     |     |     |     |     | Reasoning 1 |         | Comment 1 |
"""

        technical_tree = """# {0}

| Attack Tree             | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning   | Control | Comment   |
| ----------------------- | ---- | --- | --- | --- | --- | --- | ----------- | ------- | --------- |
| Threat 1                | LEAF | 6m  | P   | R   | M   | ST  |             |         |           |
"""

        at_a_2_man = """# {0}

| Attack Tree             | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning   | Control | Comment   |
| ----------------------- | ---- | --- | --- | --- | --- | --- | ----------- | ------- | --------- |
| Manipulation of Asset 2 | OR   |     |     |     |     |     | Reasoning 0 |         | Comment 0 |
| -- Threat 1             | LEAF | 6m  | P   | R   | M   | ST  | Reasoning 1 | C-1 C-2 | Comment 1 |
"""

        at_a_2_ext = """# {0}

| Attack Tree           | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning   | Control | Comment   |
| --------------------- | ---- | --- | --- | --- | --- | --- | ----------- | ------- | --------- |
| Extraction of Asset 2 | OR   |     |     |     |     |     | Reasoning 0 |         | Comment 0 |
| -- Threat 1           | LEAF | 6m  | P   | R   | M   | ST  | Reasoning 1 |         | Comment 1 |
"""

        attack_trees = {
            "CIRC_C-1": circ_c1,
            "CIRC_C-2": circ_c2,
            "AT_A-1_BLOCK": at_a_1_block,
            "AT_A-1_MAN": at_a_1_man,
            "AT_A-2_MAN": at_a_2_man,
            "AT_A-2_EXT": at_a_2_ext,
            "TAT_TREE": technical_tree,
        }

        for at_id, tree_content in attack_trees.items():
            attack_tree_file_path = os.path.join(self.directory, "AttackTrees", f"{at_id}.md")
            attack_tree_file_content = tree_content.format(at_id)
            self.mock_reader.setup_file(attack_tree_file_path, attack_tree_file_content)

        self.parser = TaraParser(self.mock_reader, self.logger)

class TestTaraReportGenerator(unittest.TestCase):
    def test_a_report_for_a_tara_without_controls_can_be_generated(self):
        # Arrange
        t = TestCase()
        tara = t.parser.parse(t.directory)

        self.assertEqual(t.logger.errors, [])

        generator = TaraDocumentGenerator(t.logger)

        # Act
        document: MarkdownDocument = generator.generate(tara)

        # Assert
        self.assertIsInstance(document, MarkdownDocument)

        
        content = document.getContent()

        self.assertEqual(t.logger.errors, [])

        # title (1) + threat scenarios table (2) + Attack Trees Title (1) + 7 resolved attack trees (14)
        self.assertEqual(len(content), 18)

        title: MarkdownSection = content[0]
        threat_scenarios_section: MarkdownSection = content[1]
        threat_scenarios: MarkdownTable = content[2]

        self.assertIsInstance(title, MarkdownSection)
        self.assertEqual(title.level, 0)
        self.assertEqual(title.title, "Threat Analysis And Risk Assessment (TARA) Report")

        self.assertIsInstance(threat_scenarios_section, MarkdownSection)
        self.assertEqual(threat_scenarios_section.level, 1)
        self.assertEqual(threat_scenarios_section.title, "Threat Scenarios")

        self.assertIsInstance(threat_scenarios, MarkdownTable)
        self.assertTrue(threat_scenarios.hasHeader(["ID", "Threat Scenario", "Impact", "Feasibility", "Risk"]))
        self.assertEqual(threat_scenarios.getRowCount(), 4)

        self.assertEqual(threat_scenarios.getRow(0), ["TS-1", 
                                                      "Electrocuted person caused by blocking of Asset 1", 
                                                      "Severe", "[Low](#at_a-1_block)", "Medium"])
        self.assertEqual(threat_scenarios.getRow(1), ["TS-2", 
                                                      "Litigation caused by manipulation of Asset 1", 
                                                      "Major", "[Medium](#at_a-1_man)", "Medium"])
        self.assertEqual(threat_scenarios.getRow(2), ["TS-3", 
                                                      "Litigation caused by manipulation of Asset 2", 
                                                      "Major", "[VeryLow](#at_a-2_man)", "VeryLow"])
        self.assertEqual(threat_scenarios.getRow(3), ["TS-4", 
                                                      "Litigation caused by extraction of Asset 2", 
                                                      "Major", "[Medium](#at_a-2_ext)", "Medium"])
        
        # Resolved attack trees section
        
        attack_trees_section: MarkdownSection = content[3]
        self.assertEqual(attack_trees_section.level, 1)
        self.assertEqual(attack_trees_section.title, "Attack Trees")

        attack_trees_section: MarkdownSection = content[4]
        self.assertEqual(attack_trees_section.level, 2)
        self.assertEqual(attack_trees_section.title, "AT_A-1_BLOCK")

        resolved_tree_a1_block: MarkdownTable = content[5]
        self.assertIsInstance(resolved_tree_a1_block, MarkdownTable)
        self.assertEqual(resolved_tree_a1_block.getRowCount(), 4)
        self.assertTrue(resolved_tree_a1_block.hasHeader(["Attack Tree", "Node", "ET", "Ex", "Kn", "WoO", "Eq", "Feasibility", "Reasoning", "Control", "Comment"]))
        self.assertEqual(resolved_tree_a1_block.getRow(0), ["Blocking of Asset 1", "OR", "6m (4)", "E (6)", "R (3)", "M (4)", "SP (4)", "(21) Low", "Reasoning 0", "", "Comment 0"])
        self.assertEqual(resolved_tree_a1_block.getRow(1), ["-- Controlled Threat 1", "AND", "6m (4)", "E (6)", "R (3)", "M (4)", "SP (4)", "(21) Low", "", "C-1", ""])
        self.assertEqual(resolved_tree_a1_block.getRow(2), ["---- Threat 1", "LEAF", "6m (4)", "P (3)", "R (3)", "M (4)", "ST (0)", "(14) Medium", "Reasoning 1", "", "Comment 1"])
        self.assertEqual(resolved_tree_a1_block.getRow(3), ["---- [Circumvent Control 1](#circ_c-1)", "CIRC", "1m (1)", "E (6)", "R (3)", "E (1)", "SP (4)", "(15) Medium", "", "", ""])

        attack_trees_section: MarkdownSection = content[6]
        self.assertEqual(attack_trees_section.level, 2)
        self.assertEqual(attack_trees_section.title, "AT_A-1_MAN")

        resolved_tree_a1_man: MarkdownTable = content[7]
        self.assertIsInstance(resolved_tree_a1_man, MarkdownTable)
        self.assertEqual(resolved_tree_a1_man.getRowCount(), 2)
        self.assertEqual(resolved_tree_a1_man.getRow(0), ["Manipulation of Asset 1", "OR", "6m (4)", "P (3)", "R (3)", "M (4)", "ST (0)", "(14) Medium", "Reasoning 0", "", "Comment 0"])
        self.assertEqual(resolved_tree_a1_man.getRow(1), ["-- [Threat 1](#tat_tree)", "REF", "6m (4)", "P (3)", "R (3)", "M (4)", "ST (0)", "(14) Medium", "Reasoning 1", "", "Comment 1"])

        attack_trees_section: MarkdownSection = content[8]
        self.assertEqual(attack_trees_section.level, 2)
        self.assertEqual(attack_trees_section.title, "AT_A-2_MAN")
        
        resolved_tree_a2_man: MarkdownTable = content[9]
        self.assertIsInstance(resolved_tree_a2_man, MarkdownTable)
        self.assertEqual(resolved_tree_a2_man.getRowCount(), 5)