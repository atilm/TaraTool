from tara.MarkdownLib.markdown_document import MarkdownDocument, MarkdownSection, MarkdownTable
from tara.MarkdownLib.markdown_document_builder import MarkdownDocumentBuilder, MarkdownTableBuilder
from tara.domain.tara import Tara
from tara.domain.damage_scenario import DamageScenario
from tara.domain.attack_tree import attack_tree_id, AttackTree
from tara.domain.feasibility import Feasibility
from tara.domain.risk import RiskLevel
from tara.domain.security_property import SecurityProperty

class FeasibilityComparision:
    def __init__(self):
        self.initial: Feasibility = Feasibility()
        self.residual: Feasibility = Feasibility()

class ThreatScenarioDocumentGenerator:
    def generate(self, tara: Tara) -> MarkdownDocument:
        h1 = 1

        document_builder = MarkdownDocumentBuilder() \
            .withSection("Threat Scenarios", h1) \
            .withTable(self._build_threat_scenario_table(tara))

        return document_builder.build()

    def _build_threat_scenario_table(self, tara: Tara) -> MarkdownTable:
        builder = MarkdownTableBuilder() \
            .withHeader("ID", "Asset" ,"Damage", "Threat", "Threat Scenario", "Impact", "Initial Risk", "Risk Handling", "Residual Risk", "Feasibility")

        # Here all feasibilites are collected
        feasibilities = {}

        # Calculate and cache all initial feasibilities
        self._calculate_feasibilities(tara, without_controls=True, feasibilities=feasibilities)

        # Calculate and cache all residual feasibilities
        self._calculate_feasibilities(tara, without_controls=False, feasibilities=feasibilities)

        # Build the table rows
        i = 1
        for asset in tara.assets:
            for security_property, damage_scenario_ids in asset.damage_scenarios.items():
                for ds_id in damage_scenario_ids:
                    damage_scenario: DamageScenario = self._find_by_id(tara.damage_scenarios, ds_id)
                    damage_scenario_name = damage_scenario.name if damage_scenario else "Unknown"
                    impact = damage_scenario.get_impact() if damage_scenario else None
                    impact_name = impact.name if impact else "Unknown"

                    at_id = attack_tree_id(asset, security_property)
                    # attack_tree: AttackTree = self._find_by_id(tara.attack_trees, at_id)
                    
                    feasibility_id = (asset.id, security_property)

                    initial_feasibility: Feasibility = feasibilities[feasibility_id].initial
                    initial_feasibility_level = initial_feasibility.calculate_feasibility_level()
                    initial_risk = RiskLevel.look_up(impact, initial_feasibility_level)

                    feasibility: Feasibility = feasibilities[feasibility_id].residual
                    feasibility_level = feasibility.calculate_feasibility_level()
                    risk = RiskLevel.look_up(impact, feasibility_level)
                    
                    linked_feasibility = f"[{feasibility_level.name}](#{at_id.lower()})"

                    attack_description: str = security_property.to_attack_description().lower()

                    threat_scenario = f"{damage_scenario_name} caused by {attack_description} of {asset.name}"

                    builder.withRow(f"TS-{i}", f"{asset.id}", f"{ds_id}", f"{SecurityProperty.to_attack_id(security_property)}", threat_scenario, impact_name, initial_risk.name, "", risk.name, linked_feasibility)
                    i += 1

        return builder.build()

    def _calculate_feasibilities(self, tara: Tara, without_controls: bool, feasibilities: dict) -> None:
        for t in tara.attack_trees:
            t.invalidate_cache()

        for asset in tara.assets:
            for security_property, _damage_scenario_ids in asset.damage_scenarios.items():
                at_id = attack_tree_id(asset, security_property)
                attack_tree: AttackTree = self._find_by_id(tara.attack_trees, at_id)
                
                initial_feasibility = attack_tree.get_feasibility(without_controls) if attack_tree else Feasibility()

                feasibility_id = (asset.id, security_property)
                fc = feasibilities.get(feasibility_id)
                if not fc:
                    fc = FeasibilityComparision()
                    feasibilities[feasibility_id] = fc

                if without_controls:
                    fc.initial = initial_feasibility
                else:
                    fc.residual = initial_feasibility

    def _find_by_id(self, items, item_id) -> object:
        for item in items:
            if item.id == item_id:
                return item
        return None
