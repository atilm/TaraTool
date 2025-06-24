from tara.utilities.error_logger import ErrorLogger
from tara.MarkdownLib.markdown_document import *
from tara.MarkdownLib.markdown_document_builder import *
from tara.domain.tara import Tara
from tara.domain.damage_scenario import DamageScenario
from tara.domain.attack_tree import attack_tree_id, AttackTree
from tara.domain.feasibility import Feasibility
from tara.domain.risk import RiskLevel

class TaraDocumentGenerator:
    def __init__(self, error_logger: ErrorLogger):
        self.error_logger = error_logger

    def generate(self, tara) -> MarkdownDocument:
        title_level = 0
        h1 = 1

        return MarkdownDocumentBuilder() \
            .withSection("Threat Analysis And Risk Assessment (TARA) Report", title_level) \
            .withSection("Threat Scenarios", h1) \
            .withTable(self._build_threat_scenario_table(tara)) \
            .build()

    def _build_threat_scenario_table(self, tara: Tara) -> MarkdownTable:
        builder = MarkdownTableBuilder() \
            .withHeader("ID", "Threat Scenario", "Impact", "Feasibility", "Risk")

        i = 1
        for asset in tara.assets:
            for security_property, damage_scenario_ids in asset.damage_scenarios.items():
                for ds_id in damage_scenario_ids:
                    damage_scenario: DamageScenario = self._find_by_id(tara.damage_scenarios, ds_id)
                    damage_scenario_name = damage_scenario.name if damage_scenario else "Unknown"
                    impact = damage_scenario.get_impact() if damage_scenario else None
                    impact_name = impact.name if impact else "Unknown"

                    at_id = attack_tree_id(asset, security_property)
                    attack_tree: AttackTree = self._find_by_id(tara.attack_trees, at_id)
                    feasibility = attack_tree.get_feasibility() if attack_tree else Feasibility()
                    feasibility_level = feasibility.calculate_feasibility_level()

                    risk = RiskLevel.look_up(impact, feasibility_level)

                    attack_description: str = security_property.to_attack_description().lower()

                    threat_scenario = f"{damage_scenario_name} caused by {attack_description} of {asset.name}"

                    builder.withRow(f"TS-{i}", threat_scenario, impact_name, feasibility_level.name, risk.name)
                    i += 1

        return builder.build()
    
    def _find_by_id(self, items, item_id) -> object:
        for item in items:
            if item.id == item_id:
                return item
        self.error_logger.log_error(f"Item with ID {item_id} not found.")
        return None