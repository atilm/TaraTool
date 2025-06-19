from enum import Enum

class ComparableEnum(Enum):
    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.value < other.value
        return NotImplemented
    def __le__(self, other):
        if isinstance(other, self.__class__):
            return self.value <= other.value
        return NotImplemented
    def __gt__(self, other):
        if isinstance(other, self.__class__):
            return self.value > other.value
        return NotImplemented
    def __ge__(self, other):
        if isinstance(other, self.__class__):
            return self.value >= other.value
        return NotImplemented

class ElapsedTime(ComparableEnum):
    OneWeek = 0
    OneMonth = 1
    SixMonths = 4
    ThreeYears = 10
    MoreThanThreeYears = 19

class Expertise(ComparableEnum):
    Layman = 0
    Proficient = 3
    Expert = 6
    MultipleExperts = 8

class Knowledge(ComparableEnum):
    Public = 0
    Restricted = 3
    Confidential = 7
    StrictlyConfidential = 11

class WindowOfOpportunity(ComparableEnum):
    Unlimited = 0
    Easy = 1
    Moderate = 4
    Difficult = 10

class Equipment(ComparableEnum):
    Standard = 0
    Specialized = 4
    Bespoke = 7
    MultipleBespoke = 9

class FeasibilityLevel(ComparableEnum):
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

    def or_feasibility(self, other: 'Feasibility') -> 'Feasibility':
        if not isinstance(other, Feasibility):
            raise ValueError("Can only combine with another Feasibility instance")
        
        if self.calculate_feasibility_score() <= other.calculate_feasibility_score():
            return self.get_deep_copy()
        else:
            return other.get_deep_copy()
        
    def and_feasibility(self, other: 'Feasibility') -> 'Feasibility':
        if not isinstance(other, Feasibility):
            raise ValueError("Can only combine with another Feasibility instance")
        
        new_feasibility = Feasibility()
        new_feasibility.time = max(self.time, other.time)
        new_feasibility.expertise = max(self.expertise, other.expertise)
        new_feasibility.knowledge = max(self.knowledge, other.knowledge)
        new_feasibility.window_of_opportunity = max(self.window_of_opportunity, other.window_of_opportunity)
        new_feasibility.equipment = max(self.equipment, other.equipment)
        
        return new_feasibility

    def get_deep_copy(self) -> 'Feasibility':
        new_feasibility = Feasibility()
        new_feasibility.time = self.time
        new_feasibility.expertise = self.expertise
        new_feasibility.knowledge = self.knowledge
        new_feasibility.window_of_opportunity = self.window_of_opportunity
        new_feasibility.equipment = self.equipment
        return new_feasibility

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