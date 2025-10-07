from tara.domain.impacts import *

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

    def get_impact_by_category(self, category: ImpactCategory) -> Impact:
        """
        Returns the impact for the specified category.
        """
        return self.impacts.get(category, Impact.Negligible)

    def get_impact(self) -> Impact:
        """
        Returns the highest impact from all categories.
        """
        return max(self.impacts.values(), key=lambda x: x.value)