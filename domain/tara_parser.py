import os
from domain.tara import Tara
from domain.file_stubs import FileType
from domain.assumption import Assumption
from utilities.file_reader import IFileReader
from MarkdownLib.markdown_parser import MarkdownParser, MarkdownDocument, MarkdownTable

class TaraParser:
    def __init__(self, file_reader: IFileReader):
        self.file_reader = file_reader

    def parse(self, directory: str) -> Tara:
        """
        Parses the TARA documents in the specified directory and returns a Tara object.
        
        :param directory: The directory containing the TARA documents.
        :return: A Tara object populated with parsed data.
        """

        tara = Tara()
        assumptions_table = self.read_table(FileType.ASSUMPTIONS, directory)
        tara.assumptions = self.extract_assumptions(assumptions_table)

        return tara
    
    def read_table(self, file_type: FileType, directory: str) -> MarkdownTable:
        """
        Each file type is associated with a specific file name and the header
        of a markdown table expected within that file.
        The method reads the file, finds the table and parses it.
        """

        content = self.file_reader.read_file(os.path.join(directory, FileType.to_path(file_type)))
        parser = MarkdownParser()
        document: MarkdownDocument = parser.parse(content)

        for content in document.getContent():
            if isinstance(content, MarkdownTable) and content.hasHeader(FileType.get_header(file_type)):
                return content

        raise ValueError(f"{file_type} table not found in the document.")

    def extract_assumptions(self, table: MarkdownTable) -> list[Assumption]:
        """
        Extracts assumptions from a MarkdownTable.
        
        :param table: The MarkdownTable containing assumptions.
        :return: A list of Assumption objects.
        """
        assumptions = []
        for row in range(table.getRowCount()):
            assumption = Assumption()
            assumption.id = table.getCell(row, 0)
            assumption.name = table.getCell(row, 1)
            assumption.security_claim = table.getCell(row, 2)
            assumption.comment = table.getCell(row, 3)
            assumptions.append(assumption)
        return assumptions