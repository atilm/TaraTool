from enum import Enum

class ElapsedTime(Enum):
    OneWeek = 1
    OneMonth = 4
    SixMonths = 17
    MoreThanSixMonths = 19

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
    VeryLow = 0
    Low = 1
    Medium = 2
    High = 3

class Feasibility:
    def __init__(self):
        self.time: ElapsedTime = ElapsedTime.OneWeek
        self.expertise: Expertise = Expertise.Layman
        self.knowledge: Knowledge = Knowledge.Public
        self.window_of_opportunity: WindowOfOpportunity = WindowOfOpportunity.Unlimited
        self.equipment: Equipment = Equipment.Standard
        
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