from domain.asset import Asset
from domain.assumption import Assumption
from domain.damage_scenario import DamageScenario
from domain.attack_tree import AttackTree

class Tara:
    def __init__(self):
        self.assumptions: list[Assumption] = []
        self.assets: list[Asset] = []
        self.damage_scenarios: list[DamageScenario] = []
        self.attack_trees: list[AttackTree] = []
