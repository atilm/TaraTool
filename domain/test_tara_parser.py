import unittest, os
from domain.tara_parser import TaraParser
from domain.file_stubs import FileType
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
        # self.assertEqual(len(tara.assets), 2)
        # self.assertEqual(len(tara.damage_scenarios), 2)
        # self.assertEqual(len(tara.attack_trees), 2)

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
