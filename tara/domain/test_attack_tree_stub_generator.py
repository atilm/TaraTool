import unittest
from tara.utilities.error_logger import MemoryErrorLogger
from tara.utilities.file_writer import MockFileWriter
from tara.domain.tara import Tara
from tara.domain.damage_scenario import DamageScenario
from tara.domain.asset import Asset
from tara.domain.security_property import SecurityProperty
from tara.domain.attack_tree_stub_generator import AttackTreeStubGenerator
from tara.domain.security_control import SecurityControl

class TestCase:
    def __init__(self):
        self.error_logger: MemoryErrorLogger = MemoryErrorLogger()
        self.file_writer: MockFileWriter = MockFileWriter()
        self.generator = AttackTreeStubGenerator(self.file_writer, self.error_logger)
        self.tara = Tara()

        ds = DamageScenario()
        ds.id = "DS1"
        ds.name = "Data Breach"

        self.tara.damage_scenarios = [
            ds
        ]

        db_asset = Asset()
        db_asset.id = "AST-DB"
        db_asset.name = "Database Server"
        db_asset.damage_scenarios = {
            SecurityProperty.Availability: ["DS1"],
            SecurityProperty.Integrity: ["DS1"],
            SecurityProperty.Confidentiality: ["DS1"]
        }

        cred_asset = Asset()
        cred_asset.id = "AST-CRED"
        cred_asset.name = "Credential Store"
        cred_asset.damage_scenarios = {
            SecurityProperty.Availability: [],
            SecurityProperty.Integrity: [],
            SecurityProperty.Confidentiality: ["DS1"]
        }

        self.tara.assets = [
            db_asset,
            cred_asset
        ]

        sec_control = SecurityControl()
        sec_control.id = "C-1"
        sec_control.name = "Access Control"
        sec_control.security_goal = "Goal-1"
        sec_control.is_active = False

        self.tara.security_controls = [sec_control]

class TestAttackTreeStubGenerator(unittest.TestCase):
    def test_attack_tree_file_stubs_are_generated_for_all_threats(self):
        # Arrange
        test_case = TestCase()
        generator = test_case.generator
        tara = test_case.tara

        # Act
        generator.update_stubs(tara, ".")

        # Assert
        expected_files = [
            "AT_AST-DB_BLOCK.md",
            "AT_AST-DB_MAN.md",
            "AT_AST-DB_EXT.md",
            "AT_AST-CRED_EXT.md",
            "CIRC_C-1.md"
        ]

        for file_name in expected_files:
            self.assertIn(f"./AttackTrees/{file_name}", test_case.file_writer.written_files)

        self.assertEqual(test_case.file_writer.written_files[f"./AttackTrees/AT_AST-DB_BLOCK.md"],
"""# AT_AST-DB_BLOCK

* Node: (OR, AND, LEAF, REF)
* ET: Elapsed Time (1w, 1m, 6m, 3y, >3y)
* Ex: Expertise (L: Layman, P: Proficient, E: Expert, ME: multiple Experts)
* Kn: Knowledge (P: Public, R: Restricted, C: Confidential, SC: strictly Confidential)
* WoO: Window of Opportunity (U: Unlimited, E: Easy, M: Moderate, D: Difficult)
* Eq: Equipment (ST: Standard, SP: Specialized, B: Bespoke, MB: multiple Bespoke)

| Attack Tree | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning | Control | Comment |
| ------------------------------------ | ---- | --- | --- | --- | --- | --- | --------- | ------- | ------- |
| Blocking of Database Server |      |     |     |     |     |     |           |         |         |
""")
        
        self.assertEqual(test_case.file_writer.written_files[f"./AttackTrees/CIRC_C-1.md"],
"""# CIRC_C-1

* Node: (OR, AND, LEAF, REF)
* ET: Elapsed Time (1w, 1m, 6m, 3y, >3y)
* Ex: Expertise (L: Layman, P: Proficient, E: Expert, ME: multiple Experts)
* Kn: Knowledge (P: Public, R: Restricted, C: Confidential, SC: strictly Confidential)
* WoO: Window of Opportunity (U: Unlimited, E: Easy, M: Moderate, D: Difficult)
* Eq: Equipment (ST: Standard, SP: Specialized, B: Bespoke, MB: multiple Bespoke)

| Attack Tree | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning | Control | Comment |
| ------------------------------------ | ---- | --- | --- | --- | --- | --- | --------- | ------- | ------- |
| Circumvent Access Control |      |     |     |     |     |     |           |         |         |
""")
                         
        
    def test_existing_attack_tree_files_are_not_overwritten(self):
        # Arrange
        test_case = TestCase()
        generator = test_case.generator
        tara = test_case.tara

        # Create a mock file that already exists
        test_case.file_writer.setup_exisiting_files(["./AttackTrees/AT_AST-DB_BLOCK.md", "./AttackTrees/AT_AST-CRED_EXT.md"])

        # Act
        generator.update_stubs(tara, ".")

        # Assert
        self.assertIn(f"./AttackTrees/AT_AST-DB_MAN.md", test_case.file_writer.written_files)
        self.assertIn(f"./AttackTrees/AT_AST-DB_EXT.md", test_case.file_writer.written_files)
        
        self.assertNotIn(f"./AttackTrees/AT_AST-DB_BLOCK.md", test_case.file_writer.written_files)
        self.assertNotIn(f"./AttackTrees/AT_AST-CRED_EXT.md", test_case.file_writer.written_files)
