from enum import Enum

class SecurityProperty(Enum):
    Confidentiality = 1
    Integrity = 2
    Availability = 3

    def to_attack_description(self) -> str:
        """
        Returns a human-readable description of the security property.
        
        :return: A string description of the security property.
        """
        descriptions = {
            SecurityProperty.Confidentiality: "Extraction",
            SecurityProperty.Integrity: "Manipulation",
            SecurityProperty.Availability: "Blocking"
        }
        return descriptions.get(self, "Unknown Security Property")

    def to_attack_id(self) -> str:
        """
        Returns a string representation of the security property for use in attack IDs.
        
        :return: A string representation of the security property.
        """
        descriptions = {
            SecurityProperty.Confidentiality: "EXT",
            SecurityProperty.Integrity: "MAN",
            SecurityProperty.Availability: "BLOCK"
        }
        return descriptions.get(self, "Unknown Security Property")