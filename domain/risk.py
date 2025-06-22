from enum import Enum
from domain.feasibility import FeasibilityLevel
from domain.impacts import Impact

class RiskLevel(Enum):
    VeryLow = 1
    Low = 2
    Medium = 3
    High = 4
    Critical = 5

    risk_map: dict[Impact, dict[FeasibilityLevel, 'RiskLevel']] = {
            Impact.Severe: {
                FeasibilityLevel.High: Critical,
                FeasibilityLevel.Medium: High,
                FeasibilityLevel.Low: Medium,
                FeasibilityLevel.VeryLow: Low
            },
            Impact.Major: {
                FeasibilityLevel.High: High,
                FeasibilityLevel.Medium: Medium,
                FeasibilityLevel.Low: Low,
                FeasibilityLevel.VeryLow: VeryLow
            },
            Impact.Moderate: {
                FeasibilityLevel.High: Medium,
                FeasibilityLevel.Medium: Low,
                FeasibilityLevel.Low: Low,
                FeasibilityLevel.VeryLow: VeryLow
            },
            Impact.Negligible: {
                FeasibilityLevel.High: VeryLow,
                FeasibilityLevel.Medium: VeryLow,
                FeasibilityLevel.Low: VeryLow,
                FeasibilityLevel.VeryLow: VeryLow
            }
        }

    @classmethod
    def look_up(cls, impact: Impact, feasibility: FeasibilityLevel) -> 'RiskLevel':
        """
        Look up the risk level based on feasibility and impact.
        """
        if impact not in cls.risk_map:
            raise ValueError(f"Invalid impact: {impact}")
        
        if feasibility not in cls.risk_map[impact]:
            raise ValueError(f"Invalid feasibility level: {feasibility}")  
        
        return cls.risk_map[impact][feasibility]
