import unittest, os
from domain.tara_parser import TaraParser
from domain.file_stubs import FileType
from utilities.file_reader import IFileReader

class MockFileReader(IFileReader):
    def __init__(self):
        self.contents = {}

    def setup_file(self, file_path: str, file_content: str):
        self.contents[file_path] = file_content

    def read_file(self, file_path: str) -> str:
        return self.contents.get(file_path, f"No mock has been set up for file path '{file_path}'")

class TaraParserTests(unittest.TestCase):
    def test_parse_valid_files(self):
        # Arrange
        directory = "mock_directory"
        mock_reader = MockFileReader()
        mock_reader.setup_file(os.path.join(directory, FileType.to_path(FileType.ASSUMPTIONS)),
"""# Assumptions

| ID    | Name | Security Claim | Comment |
| ----- | ---- | -------------- | ------- |
| Ast-1 | abc  | def            | ghi     |
| Ast-2 | jkl  | mno            | pqr     |
""")
        # mock_reader.setup_file("damage_scenarios.txt", "Scenario1\nScenario2")
        # mock_reader.setup_file("attack_trees.txt", "Tree1\nTree2")

        parser = TaraParser(mock_reader)

        # Act
        tara = parser.parse(directory)

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