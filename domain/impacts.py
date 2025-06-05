from enum import Enum

class ImpactCategory(Enum):
    Safety = 1
    Operational = 2
    Financial = 3
    Privacy = 4

class Impact(Enum):
    Severe = 1
    Major = 2
    Moderate = 3
    Negligible = 4
