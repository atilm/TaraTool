import os
from domain.tara import Tara
from domain.file_stubs import FileType
from domain.assumption import Assumption
from domain.damage_scenario import DamageScenario
from domain.impacts import ImpactCategory, Impact
from domain.asset import Asset
from domain.security_property import SecurityProperty
from domain.attack_tree import *
from domain.feasibility import *
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

        assets_table = self.read_table(FileType.ASSETS, directory)
        tara.assets = self.extract_assets(assets_table)

        # generate all attack tree ids
        attack_tree_ids = []
        for asset in tara.assets:
            for sp in asset.security_properties():
                attack_tree_ids.append(attack_tree_id(asset, sp))

        # parse all attack trees
        for att_id in attack_tree_ids:
            file_name = f"{att_id}.md"
            att_dir = os.path.join(directory, "AttackTrees")
            attack_tree_table = self.read_table(FileType.ATTACK_TREE, att_dir, file_name) 
            attack_tree = self.extract_attack_tree(attack_tree_table, att_id)       
            tara.attack_trees.append(attack_tree)

        # register all objects by their ID
        self.add_ids(tara.assumptions)
        self.add_ids(tara.damage_scenarios)
        self.add_ids(tara.assets)
        self.add_ids(tara.attack_trees)

        # check rules
        self.check_damage_scenario_references_in_assets(tara)

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


    def check_damage_scenario_references_in_assets(self, tara: Tara) -> None:
        """
        Checks if all damage scenarios referenced in assets exist in the TARA.
        
        :param tara: The Tara object containing assets and damage scenarios.
        """
        for asset in tara.assets:
            for _security_property, damage_scenario_ids in asset.damage_scenarios.items():
                for ds_id in damage_scenario_ids:
                    if ds_id not in self.id_to_object:
                        self.logger.log_error(f"Damage scenario {ds_id} referenced by asset {asset.id} does not exist.")
                    else:
                        ds = self.id_to_object[ds_id]
                        if not isinstance(ds, DamageScenario):
                            self.logger.log_error(f"ID {ds_id} referenced by asset {asset.id} is not a damage scenario.")


    def read_table(self, file_type: FileType, directory: str, file_name: str = None) -> MarkdownTable:
        """
        Each file type is associated with a specific file name and the header
        of a markdown table expected within that file.
        The method reads the file, finds the table and parses it.
        """

        if file_name is None:
            file_name = FileType.to_path(file_type)

        content = self.file_reader.read_file(os.path.join(directory, file_name))
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

        if len(impact_str) == 0:
            impact_str = "Negligible"  # Default to Negligible if empty

        try:
            return Impact[impact_str]
        except KeyError:
            self.logger.log_error(f"Invalid impact rating found: {impact_str}")
            return Impact.Severe  # Default to Severe or handle as needed
        
    def extract_assets(self, table: MarkdownTable) -> list[Asset]:
        """
        Extracts assets from a MarkdownTable.
        
        :param table: The MarkdownTable containing assets.
        :return: A list of Asset objects.
        """
        assets = []
        if table is None:
            return assets

        for row in range(table.getRowCount()):
            asset = Asset()
            asset.id = table.getCell(row, 0)
            asset.name = table.getCell(row, 1)
            asset.reasoning = table.getCell(row, 5)
            asset.description = table.getCell(row, 6)

            asset.damage_scenarios[SecurityProperty.Availability] = self.damage_scenarios_from_column(table, row, 2)
            asset.damage_scenarios[SecurityProperty.Integrity] = self.damage_scenarios_from_column(table, row, 3)
            asset.damage_scenarios[SecurityProperty.Confidentiality] = self.damage_scenarios_from_column(table, row, 4)
            
            assets.append(asset)

        return assets
    
    def damage_scenarios_from_column(self, table: MarkdownTable, row: int, column: int) -> list[str]:
        """
        A damage scenario table contains white-space separated damage scenario ids in each security property column.
        This method extracts damage scenario ids from a specific column in the MarkdownTable.
        
        :param table: The MarkdownTable containing assets.
        :param row: The row index to extract from.
        :param column: The column index to extract from.
        :return: A list of DamageScenario ids.
        """
        damage_scenarios = []
        cell_content = table.getCell(row, column)

        if len(cell_content) == 0:
            return damage_scenarios

        # Split by whitespace and strip whitespace
        ids = [id.strip() for id in cell_content.split() if id.strip()]
        
        for id in ids:
            damage_scenarios.append(id)
        
        return damage_scenarios

    def extract_attack_tree(self, table: MarkdownTable, attack_tree_id: str) -> AttackTree:
        """
        Parses an attack tree from a markdown table.
        
        :param table: The markdown table containing the tree.
        :param attack_tree_id: The trees id corresponding to the markdown file name.
        :return: The parsed attack tree.
        """

        node: AttackTreeNode = None
        prev_node: AttackTreeNode = None
        node_stack: list[AttackTreeNode] = []
        prev_indentation: int = 0
        indentation: int = 0

        for row in range(table.getRowCount()):
            # determine indentation and node name
            name = table.getCell(row, 0)

            prev_indentation = indentation
            indentation = 0
            while name.startswith("-"):
                name = name[1:]
                indentation += 1
            name = name.strip()

            comment = table.getCell(row, 9)
            reasoning = table.getCell(row, 7)
            
            prev_node = node
            node: AttackTreeNode = None

            row_type = table.getCell(row, 1)
            if row_type == "OR":
                node = AttackTreeOrNode()
            elif row_type == "AND":
                node = AttackTreeAndNode()
            elif row_type == "LEAF" or row_type == "":
                feasibility = Feasibility()
                feasibility.time = self.parse_elapsed_time(table.getCell(row, 2), attack_tree_id)
                feasibility.expertise = self.parse_expertise(table.getCell(row, 3), attack_tree_id)
                feasibility.knowledge = self.parse_knowledge(table.getCell(row, 4), attack_tree_id)
                feasibility.window_of_opportunity = self.parse_window_of_opportunity(table.getCell(row, 5), attack_tree_id)
                feasibility.equipment = self.parse_equipment(table.getCell(row, 6), attack_tree_id)

                node = AttackTreeLeafNode(feasibility)

            node.name = name
            node.comment = comment
            node.reasoning = reasoning

            if indentation > prev_indentation:
                node_stack.append(prev_node)
            elif indentation < prev_indentation:
                node_stack.pop()
                
            if len(node_stack) != 0:
                node_stack[-1].add_child(node)    
        
        tree =  AttackTree(attack_tree_id)
        tree.root_node = node_stack[0]

        return tree

    def parse_elapsed_time(self, s: str, tree_id: str) -> ElapsedTime:
        if s == "1w":
            return ElapsedTime.OneWeek
        elif s == "1m":
            return ElapsedTime.OneMonth
        elif s == "6m":
            return ElapsedTime.SixMonths
        elif s == "3y":
            return ElapsedTime.ThreeYears
        elif s == ">3y":
            return ElapsedTime.MoreThanThreeYears
        else:
            self.logger.log_error(f"Invalid elapsed time string found in attack tree {tree_id}: '{s}'")

    def parse_expertise(self, s: str, tree_id: str) -> Expertise:
        if s == "L":
            return Expertise.Layman
        elif s == "P":
            return Expertise.Proficient
        elif s == "E":
            return Expertise.Expert
        elif s == "ME":
            return Expertise.MultipleExperts
        else:
            self.logger.log_error(f"Invalid expertise string found in attack tree {tree_id}: '{s}'")

    def parse_knowledge(self, s: str, tree_id: str) -> Knowledge:
        if s == "P":
            return Knowledge.Public
        elif s == "R":
            return Knowledge.Restricted
        elif s == "C":
            return Knowledge.Confidential
        elif s == "SC":
            return Knowledge.StrictlyConfidential
        else:
            self.logger.log_error(f"Invalid knowledge string found in attack tree {tree_id}: '{s}'")

    def parse_window_of_opportunity(self, s: str, tree_id: str) -> WindowOfOpportunity:
        if s == "U":
            return WindowOfOpportunity.Unlimited
        elif s == "E":
            return WindowOfOpportunity.Easy
        elif s == "M":
            return WindowOfOpportunity.Moderate
        elif s == "D":
            return WindowOfOpportunity.Difficult
        else:
            self.logger.log_error(f"Invalid window of opportunity string found in attack tree {tree_id}: '{s}'")

    def parse_equipment(self, s: str, tree_id: str) -> Expertise:
        if s == "ST":
            return Equipment.Standard
        elif s == "SP":
            return Equipment.Specialized
        elif s == "B":
            return Equipment.Bespoke
        elif s == "MB":
            return Equipment.MultipleBespoke
        else:
            self.logger.log_error(f"Invalid equipment string found in attack tree {tree_id}: '{s}'")
