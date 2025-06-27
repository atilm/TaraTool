from tara.domain.tara import Tara
from tara.domain.asset import Asset
from tara.domain.security_property import SecurityProperty
from tara.domain.attack_tree import attack_tree_id
from tara.utilities.file_writer import FileWriter
from tara.utilities.error_logger import IErrorLogger

class AttackTreeStubGenerator:
    """
    A class to generate starting files for attack trees for all threats,
    i.e. combinations of assets and security properties.
    """

    def __init__(self, file_writer: FileWriter, error_logger: IErrorLogger):
        """
        Initializes the AttackTreeStubGenerator with an error logger.
        
        :param error_logger: An instance of IErrorLogger to log errors.
        """
        self.file_writer = file_writer
        self.error_logger = error_logger

    def update_stubs(self, tara: Tara, directory: str) -> None:
        class TreeDefinition:
            def __init__(self, id: str, root_node_name: str):
                self.id = id
                self.root_node_name = root_node_name

        tree_definitions = []

        # Define attack trees for all assets and security properties
        for asset in tara.assets:
            for security_property, damage_scenarios in asset.damage_scenarios.items():
                # One assigned damage scenario is enough to generate a stub
                if not damage_scenarios or len(damage_scenarios) == 0:
                    continue

                tree_id = attack_tree_id(asset, security_property)
                root_node_name = f"{security_property.to_attack_description()} of {asset.name}"

                tree_definitions.append(TreeDefinition(tree_id, root_node_name))

        # Define circumvent tree stubs for all security controls
        for control in tara.security_controls:
            tree_id = f"CIRC_{control.id}"
            root_node_name = f"Circumvent {control.name}"
            tree_definitions.append(TreeDefinition(tree_id, root_node_name))

        # Write the stub files
        for tree_definition in tree_definitions:
            file_path = f"{directory}/AttackTrees/{tree_definition.id}.md"
            if self.file_writer.exists(file_path):
                continue

            content = self._generate_stub_content(tree_definition.id, tree_definition.root_node_name)
            self.file_writer.write(file_path, content)

    def _generate_stub_content(self, att_id: str, root_node_name: str) -> str:
        """
        Generates the content for the attack tree stub file.
        
        :param asset: The asset for which the attack tree is being generated.
        :param security_property: The security property associated with the attack tree.
        :return: A string containing the content for the attack tree stub file.
        """
        return (
f"""# {att_id}

* Node: (OR, AND, LEAF, REF)
* ET: Elapsed Time (1w, 1m, 6m, 3y, >3y)
* Ex: Expertise (L: Layman, P: Proficient, E: Expert, ME: multiple Experts)
* Kn: Knowledge (P: Public, R: Restricted, C: Confidential, SC: strictly Confidential)
* WoO: Window of Opportunity (U: Unlimited, E: Easy, M: Moderate, D: Difficult)
* Eq: Equipment (ST: Standard, SP: Specialized, B: Bespoke, MB: multiple Bespoke)

| Attack Tree | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning | Control | Comment |
| ------------------------------------ | ---- | --- | --- | --- | --- | --- | --------- | ------- | ------- |
| {root_node_name} |      |     |     |     |     |     |           |         |         |
"""
        )
