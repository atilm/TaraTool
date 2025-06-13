import os
from domain.tara import Tara
from domain.file_stubs import FileType
from domain.assumption import Assumption
from domain.damage_scenario import DamageScenario
from domain.impacts import ImpactCategory, Impact
from utilities.file_reader import IFileReader
from utilities.error_logger import IErrorLogger
from MarkdownLib.markdown_parser import MarkdownParser, MarkdownDocument, MarkdownTable

class TaraParser:
    def __init__(self, file_reader: IFileReader, logger: IErrorLogger):
        self.file_reader = file_reader
        self.logger = logger
        # map of all objects which are identified by an ID
        self.id_to_object: dict[str, object] = {}

    def parse(self, directory: str) -> Tara:
        """
        Parses the TARA documents in the specified directory and returns a Tara object.
        
        :param directory: The directory containing the TARA documents.
        :return: A Tara object populated with parsed data.
        """

        tara = Tara()
        assumptions_table = self.read_table(FileType.ASSUMPTIONS, directory)
        tara.assumptions = self.extract_assumptions(assumptions_table)

        damage_scenarios_table = self.read_table(FileType.DAMAGE_SCENARIOS, directory)
        tara.damage_scenarios = self.extract_damage_scenarios(damage_scenarios_table)

        # register all objects by their ID
        self.add_ids(tara.assumptions)
        self.add_ids(tara.damage_scenarios)

        return tara
    
    def add_ids(self, objects: list[object]) -> None:
        """
        Adds IDs to a list of objects and registers them in the id_to_object map.
        
        :param objects: A list of objects to register by their ID.
        """
        for obj in objects:
            if hasattr(obj, 'id') and obj.id:
                if obj.id in self.id_to_object:
                    self.logger.log_error(f"Duplicate ID found: {obj.id}")
                else:
                    self.id_to_object[obj.id] = obj
            else:
                raise ValueError("Object does not have a valid ID.") from None

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

        self.logger.log_error(f"{file_type} table not found in the document.")
        return None

    def extract_assumptions(self, table: MarkdownTable) -> list[Assumption]:
        """
        Extracts assumptions from a MarkdownTable.
        
        :param table: The MarkdownTable containing assumptions.
        :return: A list of Assumption objects.
        """
        assumptions = []
        if table is None:
            return assumptions

        for row in range(table.getRowCount()):
            assumption = Assumption()
            assumption.id = table.getCell(row, 0)
            assumption.name = table.getCell(row, 1)
            assumption.security_claim = table.getCell(row, 2)
            assumption.comment = table.getCell(row, 3)
            assumptions.append(assumption)

        return assumptions
    
    def extract_damage_scenarios(self, table: MarkdownTable) -> list:
        """
        Extracts damage scenarios from a MarkdownTable.
        
        :param table: The MarkdownTable containing damage scenarios.
        :return: A list of DamageScenario objects.
        """
        damage_scenarios = []
        if table is None:
            return damage_scenarios

        for row in range(table.getRowCount()):
            scenario = DamageScenario()
            scenario.id = table.getCell(row, 0)
            scenario.name = table.getCell(row, 1)
            scenario.reasoning = table.getCell(row, 6)
            scenario.comment = table.getCell(row, 7)

            # Assuming impacts are stored in a specific format in the table
            scenario.impacts = {
                ImpactCategory.Safety: self.str_to_impact(table.getCell(row, 2)),
                ImpactCategory.Operational: self.str_to_impact(table.getCell(row, 3)),
                ImpactCategory.Financial: self.str_to_impact(table.getCell(row, 4)),
                ImpactCategory.Privacy: self.str_to_impact(table.getCell(row, 5))
            }

            damage_scenarios.append(scenario)

        return damage_scenarios
    
    def str_to_impact(self, impact_str: str) -> Impact:
        """
        Converts a string representation of an impact to an Impact enum.
        
        :param impact_str: The string representation of the impact.
        :return: The corresponding Impact enum.
        """
        impact_str = impact_str.strip()

        try:
            return Impact[impact_str]
        except KeyError:
            self.logger.log_error(f"Invalid impact rating found: {impact_str}")
            return Impact.Severe  # Default to Severe or handle as needed