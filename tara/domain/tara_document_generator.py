from tara.utilities.error_logger import ErrorLogger
from tara.MarkdownLib.markdown_document import *
from tara.MarkdownLib.markdown_document_builder import *
from tara.domain.tara import Tara
from tara.domain.damage_scenario import DamageScenario
from tara.domain.attack_tree import attack_tree_id, AttackTree, AttackTreeResolvedNode
from tara.domain.feasibility import Feasibility
from tara.domain.risk import RiskLevel
from tara.domain.feasibility_conversion import *

class TaraDocumentGenerator:
    def __init__(self, error_logger: ErrorLogger):
        self.error_logger = error_logger

    def generate(self, tara: Tara) -> MarkdownDocument:
        title_level = 0
        h1 = 1
        h2 = 2

        document_builder = MarkdownDocumentBuilder() \
            .withSection("Threat Analysis And Risk Assessment (TARA) Report", title_level) \
            .withSection("Threat Scenarios", h1) \
            .withTable(self._build_threat_scenario_table(tara)) \
            .withSection("Attack Trees", h1)
        
        for attack_tree in tara.attack_trees:
            document_builder = document_builder \
                .withSection(attack_tree.id, h2) \
                .withTable(self._build_resolved_attack_tree_table(attack_tree))

        return document_builder.build()

    def _build_resolved_attack_tree_table(self, attack_tree: AttackTree) -> MarkdownTable:
        resolved_tree = attack_tree.get_resolved_tree()

        builder = MarkdownTableBuilder() \
            .withHeader("Attack Tree", "Node", "ET", "Ex", "Kn", "WoO", "Eq", "Reasoning", "Control", "Comment")

        self._add_attack_tree_node_to_table_recursive(builder, resolved_tree.root_node, 0)

        return builder.build()

    def _add_attack_tree_node_to_table_recursive(self, builder: MarkdownTableBuilder, node: AttackTreeResolvedNode, recursion_level: int) -> None:
        """
        Recursively adds nodes of the attack tree to the table builder.
        """
        indent_str = f"{recursion_level * '--'} " if recursion_level > 0 else ""
        security_controls_str = " ".join(node.security_control_ids) if node.security_control_ids else ""

        builder.withRow(
            indent_str + node.name,
            node.type,
            elapsed_time_to_string(node.feasibility.time),
            expertise_to_string(node.feasibility.expertise),
            knowledge_to_string(node.feasibility.knowledge),
            window_of_opportunity_to_string(node.feasibility.window_of_opportunity),
            equipment_to_string(node.feasibility.equipment),
            node.reasoning,
            security_controls_str,
            node.comment
        )

        for child in node.children:
            self._add_attack_tree_node_to_table_recursive(builder, child, recursion_level + 1)

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
                    linked_feasibility = f"[{feasibility_level.name}](#{at_id.lower()})"

                    risk = RiskLevel.look_up(impact, feasibility_level)

                    attack_description: str = security_property.to_attack_description().lower()

                    threat_scenario = f"{damage_scenario_name} caused by {attack_description} of {asset.name}"

                    builder.withRow(f"TS-{i}", threat_scenario, impact_name, linked_feasibility, risk.name)
                    i += 1

        return builder.build()
    
    def _find_by_id(self, items, item_id) -> object:
        for item in items:
            if item.id == item_id:
                return item
        self.error_logger.log_error(f"Item with ID {item_id} not found.")
        return None