from enum import Enum
from domain.feasibility import FeasibilityLevel
from domain.impacts import Impact

class RiskLevel(Enum):
    VeryLow = 1
    Low = 2
    Medium = 3
    High = 4
    Critical = 5

    @staticmethod
    def look_up(impact: Impact, feasibility: FeasibilityLevel) -> 'RiskLevel':
        """
        Look up the risk level based on feasibility and impact.
        """
        risk_map: dict[Impact, dict[FeasibilityLevel, RiskLevel]] = {
            Impact.Severe: {
                FeasibilityLevel.High: RiskLevel.Critical,
                FeasibilityLevel.Medium: RiskLevel.High,
                FeasibilityLevel.Low: RiskLevel.Medium,
                FeasibilityLevel.VeryLow: RiskLevel.Low
            },
            Impact.Major: {
                FeasibilityLevel.High: RiskLevel.High,
                FeasibilityLevel.Medium: RiskLevel.Medium,
                FeasibilityLevel.Low: RiskLevel.Low,
                FeasibilityLevel.VeryLow: RiskLevel.VeryLow
            },
            Impact.Moderate: {
                FeasibilityLevel.High: RiskLevel.Medium,
                FeasibilityLevel.Medium: RiskLevel.Low,
                FeasibilityLevel.Low: RiskLevel.Low,
                FeasibilityLevel.VeryLow: RiskLevel.VeryLow
            },
            Impact.Negligible: {
                FeasibilityLevel.High: RiskLevel.VeryLow,
                FeasibilityLevel.Medium: RiskLevel.VeryLow,
                FeasibilityLevel.Low: RiskLevel.VeryLow,
                FeasibilityLevel.VeryLow: RiskLevel.VeryLow
            }
        }

        if impact not in risk_map:
            raise ValueError(f"Invalid impact: {impact}")
        
        if feasibility not in risk_map[impact]:
            raise ValueError(f"Invalid feasibility level: {feasibility}")  
        
        return risk_map[impact][feasibility]
