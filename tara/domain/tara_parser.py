import os
from tara.domain.tara import Tara
from tara.domain.file_stubs import FileType
from tara.domain.assumption import Assumption
from tara.domain.damage_scenario import DamageScenario
from tara.domain.impacts import ImpactCategory, Impact
from tara.domain.asset import Asset
from tara.domain.security_property import SecurityProperty
from tara.domain.attack_tree_parser import AttackTreeParser
from tara.domain.feasibility import *
from tara.utilities.file_reader import IFileReader
from tara.utilities.error_logger import IErrorLogger
from tara.MarkdownLib.markdown_parser import MarkdownParser, MarkdownDocument, MarkdownTable
from tara.domain.attack_tree import AttackTree, AttackTreeNode, AttackTreeOrNode, AttackTreeAndNode, AttackTreeReferenceNode, attack_tree_id
from tara.domain.object_store import ObjectStore

class TaraParser:
    def __init__(self, file_reader: IFileReader, logger: IErrorLogger):
        self.file_reader = file_reader
        self.logger = logger
        self.object_store = ObjectStore(self.logger)

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

        # Parse security controls (security goals)
        controls_table = self.read_table(FileType.CONTROLS, directory)
        tara.security_controls = self.extract_security_controls(controls_table)

        # parse all attack trees
        attack_tree_parser = AttackTreeParser(self.logger, self.object_store)
        attack_tree_dir = os.path.join(directory, "AttackTrees")
        attack_tree_files = [f for f in self.file_reader.listdir(attack_tree_dir) if f.endswith('.md')]
        
        for file_name in attack_tree_files:
            attack_tree_table = self.read_table(FileType.ATTACK_TREE, attack_tree_dir, file_name)
            if attack_tree_table is None:
                self.logger.log_error(f"No attack tree table found in file {file_name}. Is the table header correct?")
                continue
            att_id = file_name.replace('.md', '')  # Extract the attack tree ID from the file name
            attack_tree = attack_tree_parser.parse_attack_tree(attack_tree_table, att_id)       
            tara.attack_trees.append(attack_tree)

        # register all objects by their ID
        self.add_ids(tara.assumptions)
        self.add_ids(tara.damage_scenarios)
        self.add_ids(tara.assets)
        self.add_ids(tara.attack_trees)
        self.add_ids(tara.security_controls)

        # check rules
        self.check_damage_scenario_references_in_assets(tara)
        self.check_all_attack_trees_are_present(tara)
        self.check_attack_tree_rules(tara, [
            self.check_and_or_nodes_have_children,
            self.check_referenced_trees_exist
        ])

        return tara
    def extract_security_controls(self, table: MarkdownTable) -> list:
        """
        Extracts security controls from a MarkdownTable.
        :param table: The MarkdownTable containing security controls.
        :return: A list of SecurityControl objects.
        """
        from tara.domain.security_control import SecurityControl
        controls = []
        if table is None:
            return controls

        for row in range(table.getRowCount()):
            control = SecurityControl()
            control.id = table.getCell(row, 0)
            control.name = table.getCell(row, 1)
            control.security_goal = table.getCell(row, 2)
            # Consider 'x' or 'X' as active, else inactive
            active_value = table.getCell(row, 3).strip().lower()
            control.is_active = active_value == 'x'
            controls.append(control)
        return controls

    def add_ids(self, objects: list[object]) -> None:
        """
        Adds IDs to a list of objects and registers them in the id_to_object map.
        
        :param objects: A list of objects to register by their ID.
        """
        for obj in objects:
            try:
                self.object_store.add(obj)
            except ValueError as e:
                self.logger.log_error(str(e))

    def check_damage_scenario_references_in_assets(self, tara: Tara) -> None:
        """
        Checks if all damage scenarios referenced in assets exist in the TARA.
        
        :param tara: The Tara object containing assets and damage scenarios.
        """
        for asset in tara.assets:
            for _security_property, damage_scenario_ids in asset.damage_scenarios.items():
                for ds_id in damage_scenario_ids:
                    if not self.object_store.has(ds_id):
                        self.logger.log_error(f"Damage scenario {ds_id} referenced by asset {asset.id} does not exist.")
                    else:
                        ds = self.object_store.get(ds_id)
                        if not isinstance(ds, DamageScenario):
                            self.logger.log_error(f"ID {ds_id} referenced by asset {asset.id} is not a damage scenario.")

    def check_all_attack_trees_are_present(self, tara: Tara) -> None:
        """
        Checks if all attack trees referenced in assets exist in the TARA.
        
        :param tara: The Tara object containing assets and attack trees.
        """
        from tara.domain.attack_tree import attack_tree_id

        expected_attack_tree_ids = []
        for asset in tara.assets:
            for sp in asset.security_properties():
                expected_attack_tree_ids.append(attack_tree_id(asset, sp))

        for attack_tree_id in expected_attack_tree_ids:
            if not self.object_store.has(attack_tree_id):
                self.logger.log_error(f"No attack tree found for ID {attack_tree_id}.")


    def check_attack_tree_rules(self, tara: Tara, rules: list) -> None:
        """
        Checks if all attack tree nodes of type AND and OR have at least one child.
        
        :param tara: The Tara object containing attack trees.
        :param rules: A list of lambda functions rule(node, attack_tree_id) implementing rules to check against.
        """
        def check_recursively(attack_tree_id: str, node: AttackTreeNode, logger: IErrorLogger, rules: list) -> None:
            for rule in rules:
                rule(node, attack_tree_id)

            for child in node.children:
                check_recursively(attack_tree_id, child, logger, rules)

        for tree in tara.attack_trees:
            if tree.root_node is None:
                self.logger.log_error(f"Attack tree {tree.id} has no root node.")
                continue
            
            check_recursively(tree.id, tree.root_node, self.logger, rules)

    def check_and_or_nodes_have_children(self, node: AttackTreeNode, attack_tree_id: str) -> None:
        """
        Checks if the node is an AND or OR node and has at least one child.
        
        :param node: The AttackTreeNode to check.
        :param attack_tree_id: The ID of the attack tree for logging purposes.
        """
        if isinstance(node, AttackTreeOrNode) or isinstance(node, AttackTreeAndNode):
            if len(node.children) == 0:
                self.logger.log_error(f"Node {node.name} in attack tree {attack_tree_id} has no children.")

    def check_referenced_trees_exist(self, node: AttackTreeNode, attack_tree_id: str) -> None:
        """
        Checks if the node is a reference node and the referenced tree exists.
        
        :param node: The AttackTreeNode to check.
        :param attack_tree_id: The ID of the attack tree for logging purposes.
        """
        if isinstance(node, AttackTreeReferenceNode):
            if not self.object_store.has(node.referenced_node_id):
                self.logger.log_error(f"Node {node.name} in attack tree {attack_tree_id} references non-existing tree {node.referenced_node_id}.")

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

