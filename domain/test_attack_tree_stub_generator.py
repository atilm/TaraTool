import unittest
from utilities.error_logger import MemoryErrorLogger
from utilities.file_writer import MockFileWriter
from domain.tara import Tara
from domain.damage_scenario import DamageScenario
from domain.asset import Asset
from domain.security_property import SecurityProperty
from domain.attack_tree_stub_generator import AttackTreeStubGenerator

class TestCase:
    def __init__(self):
        self.error_logger = MemoryErrorLogger()
        self.file_writer = MockFileWriter()
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
            "AT_AST-CRED_EXT.md"
        ]

        for file_name in expected_files:
            self.assertIn(f"./AttackTrees/{file_name}", test_case.file_writer.written_files)

        self.assertEqual(test_case.file_writer.written_files[f"./AttackTrees/AT_AST-DB_BLOCK.md"],
"""* ET: Elapsed Time
* Ex: Expertise
* Kn: Knowledge
* WoO: Window of Opportunity

| AT_AST-DB_BLOCK | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning | Comment | Control |
| ------------------------------------ | ---- | --- | --- | --- | --- | --- | --------- | ------- | ------- |
| Blocking of Database Server |      |     |     |     |     |     |           |         |         |
""")