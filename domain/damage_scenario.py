from domain.impacts import *

class DamageScenario:
    def __init__(self):
        self.id: str = ""
        self.name: str = ""
        self.reasoning: str = ""
        self.comment: str = ""
        self.impacts: dict = { ImpactCategory.Safety: Impact.Negligible,
                              ImpactCategory.Operational: Impact.Negligible,
                              ImpactCategory.Financial: Impact.Negligible,
                              ImpactCategory.Privacy: Impact.Negligible }
