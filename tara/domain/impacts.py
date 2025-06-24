from enum import Enum

class ImpactCategory(Enum):
    Safety = 1
    Operational = 2
    Financial = 3
    Privacy = 4


class Impact(Enum):
    Negligible = 1
    Moderate = 2
    Major = 3
    Severe = 4
