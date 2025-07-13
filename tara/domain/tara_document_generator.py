from tara.utilities.error_logger import ErrorLogger
from tara.MarkdownLib.markdown_document import *
from tara.MarkdownLib.markdown_document_builder import *
from tara.domain.tara import Tara
from tara.domain.damage_scenario import DamageScenario
from tara.domain.attack_tree import attack_tree_id, AttackTree, ResolvedAttackTree, AttackTreeResolvedNode
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


        # _build_threat_scenario_table calculates all feasibilities
        # to avoid double calculations, we resolve the attack trees here
        resolved_trees = []
        document_builder = MarkdownDocumentBuilder() \
            .withSection("Threat Analysis And Risk Assessment (TARA) Report", title_level) \
            .withSection("Threat Scenarios", h1) \
            .withTable(self._build_threat_scenario_table(tara, resolved_trees)) \
            .withSection("Attack Trees", h1)
        
        # resolved_trees = [tree.get_resolved_tree() for tree in tara.attack_trees if tree.root_node]

        for resolved_tree in resolved_trees:
            document_builder = document_builder \
                .withSection(resolved_tree.id, h2) \
                .withTable(self._build_resolved_attack_tree_table(resolved_tree))

        return document_builder.build()

    def _build_resolved_attack_tree_table(self, resolved_tree: AttackTree) -> MarkdownTable:
        builder = MarkdownTableBuilder() \
            .withHeader("Attack Tree", "Node", "ET", "Ex", "Kn", "WoO", "Eq", "Feasibility", "Reasoning", "Control", "Comment")

        self._add_attack_tree_node_to_table_recursive(builder, resolved_tree.root_node, 0)

        return builder.build()

    def _add_attack_tree_node_to_table_recursive(self, builder: MarkdownTableBuilder, node: AttackTreeResolvedNode, recursion_level: int) -> None:
        """
        Recursively adds nodes of the attack tree to the table builder.
        """
        indent_str = f"{recursion_level * '--'} " if recursion_level > 0 else ""
        security_controls_str = " ".join(node.security_control_ids) if node.security_control_ids else ""

        name = f"[{node.name}](#{node.referenced_node_id.lower()})" if node.type in ["CIRC", "REF"] else node.name

        feasibility_str = f"({node.feasibility.calculate_feasibility_score()}) {node.feasibility.calculate_feasibility_level().name}"

        def build_rating_string(security_property, to_string_func):
            if security_property is None:
                return "Unknown"
            return f"{to_string_func(security_property)} ({security_property.value})"

        builder.withRow(
            indent_str + name,
            node.type,
            build_rating_string(node.feasibility.time, elapsed_time_to_string),
            build_rating_string(node.feasibility.expertise, expertise_to_string),
            build_rating_string(node.feasibility.knowledge, knowledge_to_string),
            build_rating_string(node.feasibility.window_of_opportunity, window_of_opportunity_to_string),
            build_rating_string(node.feasibility.equipment, equipment_to_string),
            feasibility_str,
            node.reasoning,
            security_controls_str,
            node.comment
        )

        for child in node.children:
            self._add_attack_tree_node_to_table_recursive(builder, child, recursion_level + 1)

    def _build_threat_scenario_table(self, tara: Tara, resolved_trees: list[ResolvedAttackTree]) -> MarkdownTable:
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
                    feasibility = attack_tree.get_feasibility(resolved_trees) if attack_tree else Feasibility()
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