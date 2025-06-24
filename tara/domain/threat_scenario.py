from tara.domain.asset import Asset
from tara.domain.security_property import SecurityProperty
from tara.domain.damage_scenario import DamageScenario
from tara.domain.feasibility import Feasibility

class ThreatScenario:
    def __init__(self, asset: Asset, security_property: SecurityProperty, damage_scenario: DamageScenario, feasibility: Feasibility):
        """
        Initializes a ThreatScenario with an asset, security property, damage scenario, and feasibility.
        
        :param asset: The asset associated with the threat scenario.
        :param security_property: The security property associated with the threat scenario.
        :param damage_scenario: The damage scenario associated with the threat scenario.
        :param feasibility: The feasibility of the threat scenario.
        """
        self.asset = asset
        self.security_property = security_property
        self.damage_scenario = damage_scenario
        self.feasibility = feasibility
