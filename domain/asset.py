from domain.security_property import SecurityProperty
from domain.damage_scenario import DamageScenario

class Asset:
    def __init__(self):
        self.id: str = ""
        self.name: str = ""
        self.description: str = ""
        # Maps SecurityProperty to DamageScenario ids
        # An empty list for a security property means the security property is not relevant for this asset
        self.damage_scenarios: dict[SecurityProperty, list[str]] = {}
        self.damage_scenarios[SecurityProperty.Availability] = []
        self.damage_scenarios[SecurityProperty.Integrity] = []
        self.damage_scenarios[SecurityProperty.Confidentiality] = []
        # A text continaining an explanation for the asset's security properties and damage scenarios
        self.reasoning: str = ""