from asset import Asset
from assumption import Assumption
from damage_scenario import DamageScenario
from attack_tree import AttackTree


class Tara:
    def __init__(self):
        self.assumptions: list[Assumption] = []
        self.assets: list[Asset] = []
        self.damage_scenarios: list[DamageScenario] = []
        self.attack_trees: list[AttackTree] = []

