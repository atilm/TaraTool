from tara.domain.asset import Asset
from tara.domain.assumption import Assumption
from tara.domain.damage_scenario import DamageScenario
from tara.domain.attack_tree import AttackTree

class Tara:
    def __init__(self):
        self.assumptions: list[Assumption] = []
        self.assets: list[Asset] = []
        self.damage_scenarios: list[DamageScenario] = []
        self.attack_trees: list[AttackTree] = []
