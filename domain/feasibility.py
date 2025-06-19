from enum import Enum

class ElapsedTime(Enum):
    OneWeek = 0
    OneMonth = 1
    SixMonths = 4
    ThreeYears = 10
    MoreThanThreeYears = 19

class Expertise(Enum):
    Layman = 0
    Proficient = 3
    Expert = 6
    MultipleExperts = 8

class Knowledge(Enum):
    Public = 0
    Restricted = 3
    Confidential = 7
    StrictlyConfidential = 11

class WindowOfOpportunity(Enum):
    Unlimited = 0
    Easy = 1
    Moderate = 4
    Difficult = 10

class Equipment(Enum):
    Standard = 0
    Specialized = 4
    Bespoke = 7
    MultipleBespoke = 9

class FeasibilityLevel(Enum):
    High = 13       # 0  to 13: high feasibility
    Medium = 19     # 14 to 19: medium feasibility
    Low = 24        # 20 to 24: low feasibility
    VeryLow = 0     #     > 25: very low feasibility

class Feasibility:
    def __init__(self):
        self.time: ElapsedTime = ElapsedTime.OneWeek
        self.expertise: Expertise = Expertise.Layman
        self.knowledge: Knowledge = Knowledge.Public
        self.window_of_opportunity: WindowOfOpportunity = WindowOfOpportunity.Unlimited
        self.equipment: Equipment = Equipment.Standard
        
    def calculate_feasibility_level(self) -> FeasibilityLevel:
        total_score = self.calculate_feasibility_score()
        
        if total_score <= 13:
            return FeasibilityLevel.High
        elif total_score <= 19:
            return FeasibilityLevel.Medium
        elif total_score <= 24:
            return FeasibilityLevel.Low
        else:
            return FeasibilityLevel.VeryLow

    def calculate_feasibility_score(self) -> int:
        return (self.time.value + self.expertise.value +
                self.knowledge.value + self.window_of_opportunity.value +
                self.equipment.value)

    def __eq__(self, other):
        if not isinstance(other, Feasibility):
            return False
        
        if self.time != other.time:
            return False
        if self.expertise != other.expertise:
            return False
        if self.knowledge != other.knowledge:
            return False
        if self.window_of_opportunity != other.window_of_opportunity:
            return False
        if self.equipment != other.equipment:
            return False
        
        return True