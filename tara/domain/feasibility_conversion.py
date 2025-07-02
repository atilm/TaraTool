from tara.domain.feasibility import *

class EmptyStringError(ValueError):
    """Raised when the elapsed time string is empty."""
    pass

class InvalidStringError(ValueError):
    """Raised when the elapsed time string is invalid."""
    pass

def parse_elapsed_time(s: str) -> ElapsedTime:
    if s == "1w":
        return ElapsedTime.OneWeek
    elif s == "1m":
        return ElapsedTime.OneMonth
    elif s == "6m":
        return ElapsedTime.SixMonths
    elif s == "3y":
        return ElapsedTime.ThreeYears
    elif s == ">3y":
        return ElapsedTime.MoreThanThreeYears
    elif s == "":
        raise EmptyStringError()
    else:
        raise InvalidStringError()

def elapsed_time_to_string(et: ElapsedTime) -> str:
    if et == ElapsedTime.OneWeek:
        return "1w"
    elif et == ElapsedTime.OneMonth:
        return "1m"
    elif et == ElapsedTime.SixMonths:
        return "6m"
    elif et == ElapsedTime.ThreeYears:
        return "3y"
    elif et == ElapsedTime.MoreThanThreeYears:
        return ">3y"
    else:
        raise ValueError(f"Unknown elapsed time: {et}")

def parse_expertise(s: str) -> Expertise:
    if s == "L":
        return Expertise.Layman
    elif s == "P":
        return Expertise.Proficient
    elif s == "E":
        return Expertise.Expert
    elif s == "ME":
        return Expertise.MultipleExperts
    elif s == "":
        raise EmptyStringError()
    else:
        raise InvalidStringError()

def expertise_to_string(expertise: Expertise) -> str:
    if expertise == Expertise.Layman:
        return "L"
    elif expertise == Expertise.Proficient:
        return "P"
    elif expertise == Expertise.Expert:
        return "E"
    elif expertise == Expertise.MultipleExperts:
        return "ME"
    else:
        raise ValueError(f"Unknown expertise: {expertise}")

def parse_knowledge(s: str) -> Knowledge:
    if s == "P":
        return Knowledge.Public
    elif s == "R":
        return Knowledge.Restricted
    elif s == "C":
        return Knowledge.Confidential
    elif s == "SC":
        return Knowledge.StrictlyConfidential
    elif s == "":
        raise EmptyStringError()
    else:
        raise InvalidStringError()

def knowledge_to_string(knowledge: Knowledge) -> str:
    if knowledge == Knowledge.Public:
        return "P"
    elif knowledge == Knowledge.Restricted:
        return "R"
    elif knowledge == Knowledge.Confidential:
        return "C"
    elif knowledge == Knowledge.StrictlyConfidential:
        return "SC"
    else:
        raise ValueError(f"Unknown knowledge: {knowledge}")

def parse_window_of_opportunity(s: str) -> WindowOfOpportunity:
    if s == "U":
        return WindowOfOpportunity.Unlimited
    elif s == "E":
        return WindowOfOpportunity.Easy
    elif s == "M":
        return WindowOfOpportunity.Moderate
    elif s == "D":
        return WindowOfOpportunity.Difficult
    elif s == "":
        raise EmptyStringError()
    else:
        raise InvalidStringError()

def window_of_opportunity_to_string(woo: WindowOfOpportunity) -> str:
    if woo == WindowOfOpportunity.Unlimited:
        return "U"
    elif woo == WindowOfOpportunity.Easy:
        return "E"
    elif woo == WindowOfOpportunity.Moderate:
        return "M"
    elif woo == WindowOfOpportunity.Difficult:
        return "D"
    else:
        raise ValueError(f"Unknown window of opportunity: {woo}")

def parse_equipment(s: str) -> Equipment:
    if s == "ST":
        return Equipment.Standard
    elif s == "SP":
        return Equipment.Specialized
    elif s == "B":
        return Equipment.Bespoke
    elif s == "MB":
        return Equipment.MultipleBespoke
    elif s == "":
        raise EmptyStringError()
    else:
        raise InvalidStringError()
    
def equipment_to_string(equipment: Equipment) -> str:
    if equipment == Equipment.Standard:
        return "ST"
    elif equipment == Equipment.Specialized:
        return "SP"
    elif equipment == Equipment.Bespoke:
        return "B"
    elif equipment == Equipment.MultipleBespoke:
        return "MB"
    else:
        raise ValueError(f"Unknown equipment: {equipment}")