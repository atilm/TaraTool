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

        assumption_content = self.file_reader.read_file(os.path.join(directory, FileType.to_path(FileType.ASSUMPTIONS)))
        parser = MarkdownParser()
        assumptions_doc: MarkdownDocument = parser.parse(assumption_content)

        table = assumptions_doc.getContent()[1]  # Assuming the second content is the table

        tara = Tara()

        if not isinstance(table, MarkdownTable):
            raise ValueError("The second content in the assumptions document is not a table.")
        
        for row in range(table.getRowCount()):
            assumption = Assumption()
            assumption.id = table.getCell(row, 0)
            assumption.name = table.getCell(row, 1)
            assumption.security_claim = table.getCell(row, 2)
            assumption.comment = table.getCell(row, 3)
            tara.assumptions.append(assumption)

        return tara