from domain.tara import Tara
from domain.asset import Asset
from domain.security_property import SecurityProperty
from utilities.file_writer import FileWriter
from utilities.error_logger import IErrorLogger

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
        for asset in tara.assets:
            for security_property, damage_scenarios in asset.damage_scenarios.items():
                if not damage_scenarios:
                    continue
                for ds_id in damage_scenarios:
                    file_name = f"AT_{asset.id}_{security_property.to_attack_id()}.md"
                    file_path = f"{directory}/AttackTrees/{file_name}"
                    content = self._generate_stub_content(asset, security_property)
                    self.file_writer.write(file_path, content)

    def _generate_stub_content(self, asset: Asset, security_property: SecurityProperty) -> str:
        """
        Generates the content for the attack tree stub file.
        
        :param asset: The asset for which the attack tree is being generated.
        :param security_property: The security property associated with the attack tree.
        :return: A string containing the content for the attack tree stub file.
        """
        return (
f"""* ET: Elapsed Time
* Ex: Expertise
* Kn: Knowledge
* WoO: Window of Opportunity

| AT_{asset.id}_{security_property.to_attack_id()} | Node | ET  | Ex  | Kn  | WoO | Eq  | Reasoning | Comment | Control |
| ------------------------------------ | ---- | --- | --- | --- | --- | --- | --------- | ------- | ------- |
| {security_property.to_attack_description()} of {asset.name} |      |     |     |     |     |     |           |         |         |
"""
        )