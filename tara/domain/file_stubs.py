from enum import Enum

class FileStub:
    def __init__(self, file_path: str, file_content: str):
        self.path = file_path
        self.content = file_content

class FileType(Enum):
    DESCRIPTION = "description"
    ASSUMPTIONS = "assumptions"
    ASSETS = "assets"
    DAMAGE_SCENARIOS = "damage_scenarios"
    ATTACK_TREE = "attack_tree"
    METHOD_DESCRIPTION = "method_description"
        
    @classmethod
    def to_path(cls, file_type: 'FileType') -> str:
        if file_type == cls.DESCRIPTION:
            return "00_SystemDescription.md"
        elif file_type == cls.ASSUMPTIONS:
            return "01_Assumptions.md"
        elif file_type == cls.ASSETS:
            return "02_Assets.md"
        elif file_type == cls.DAMAGE_SCENARIOS:
            return "03_DamageScenarios.md"
        elif file_type == cls.METHOD_DESCRIPTION:
            return "MethodDescription.md"
        elif file_type == cls.ATTACK_TREE:
            raise ValueError("There is no fixed file name for attack tree files.")
        else:
            raise ValueError(f"Unknown file type: {file_type}")
        
    @classmethod
    def get_header(cls, file_type: 'FileType') -> list[str]:
        if file_type == cls.DESCRIPTION:
            return []
        elif file_type == cls.ASSUMPTIONS:
            return ["ID", "Name", "Security Claim", "Comment"]
        elif file_type == cls.ASSETS:
            return ["ID", "Name", "Availability", "Integrity", "Confidentiality", "Reasoning", "Description"]
        elif file_type == cls.DAMAGE_SCENARIOS:
            return ["ID", "Name", "Safety", "Operational", "Financial", "Privacy", "Reasoning", "Comment"]
        elif file_type == cls.ATTACK_TREE:
            return ["Attack Tree", "Node", "ET", "Ex", "Kn", "WoO", "Eq", "Reasoning", "Control", "Comment"]
        elif file_type == cls.METHOD_DESCRIPTION:
            return []
        else:
            raise ValueError(f"Unknown file type: {file_type}")
        
    
        
file_stubs = {
    FileType.DESCRIPTION: FileStub(FileType.to_path(FileType.DESCRIPTION), 
"""# System Description and Scope

Describe the systems interfaces, data flows, and any external systems that interact with the system.
Use drawio.png files or mermaid diagrams to illustrate the system architecture.
"""),
   FileType.ASSUMPTIONS: FileStub(FileType.to_path(FileType.ASSUMPTIONS), 
"""# Assumptions

| ID  | Name | Security Claim | Comment |
| --- | ---- | -------------- | ------- |
|     |      |                |         |
"""),
    FileType.ASSETS: FileStub(FileType.to_path(FileType.ASSETS), 
"""# Assets

| ID  | Name | Availability | Integrity | Confidentiality | Reasoning | Description |
| --- | ---- | ------------ | --------- | --------------- | --------- | ----------- |
|     |      |              |           |                 |           |             |
"""),
    FileType.DAMAGE_SCENARIOS: FileStub(FileType.to_path(FileType.DAMAGE_SCENARIOS), 
"""# Damage Scenarios

| ID  | Name | Safety | Operational | Financial | Privacy | Reasoning | Comment |
| --- | ---- | ------ | ----------- | --------- | ------- | --------- | ------- |
|     |      |        |             |           |         |           |         |
"""),
    FileType.METHOD_DESCRIPTION: FileStub(FileType.to_path(FileType.METHOD_DESCRIPTION),
"""# Method Description

## Impact Ratings

|                | Safety                                                         | Financial                                                                                                                                            | Operational                                                                                       | Privacy                                                                                                                                                                                                                             |
| -------------- | -------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Severe**     | Life-threatening injuries (survival uncertain), fatal injuries | The financial damage leads to catastrophic consequences which the affected system/component user(s) might not overcome.                              | The operational damage leads to loss or impairment of a core function.                            | The privacy damage leads to significant or even irreversible impact to the system user(s). The information regarding the user is highly sensitive and easy to link to a PII principal.                                              |
| **Major**      | Severe and life-threatening injuries (survival probable)       | The financial damage leads to substantial consequences which the affected sytem/component user(s) will be able to overcome.                          | The operational damage leads to the loss or impairment of an important system/component function. | The privacy damage leads to serious impact to the system user(s). The information regarding the users is (a) highly sensitive and difficult to link to a PII principal or (b) sensitive and easy to link to a PII principal.        |
| **Moderate**   | Light and moderate injuries                                    | The financial damage leads to inconvenient consequences which the affected system/component user(s) will be able to overcome with limited resources. | The operational damage leads to partial degradation of a system function.                         | The privacy damage leads to inconvenient consequences to the system user(s). The information regarding the user is (a) sensitive but difficult to link to a PII principal or (b) not sensitive but easy to link to a PII principal. |
| **Negligible** | No injuries                                                    | The financial damage leads to no effect, negligible consequences or is irrelevant to the system/component user(s).                                   | The operational damage leads to no impairment or non-perceivable impairment of a system function. | The privacy damage leads to no effect or negligible consequences or is irrelevant to the system user(s). The information regarding the user is not sensitive and difficult to link to a PII principal.                              |

## Feasibility Ratings

### Feasibility Mapping

| Level | Value    |
| ----- | -------- |
| 0     | High     |
| 13    | High     |
| 14    | Medium   |
| 19    | Medium   |
| 20    | Low      |
| 24    | Low      |
| 25    | Very Low |

### Elapsed Time (T)

| ID  | Level       | Description                                                                                                                                           | Value |
| --- | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ----- |
| 1w  | < 1 week    | Performing simple attacks, with large accessible information and automated scripts and tools online.                                                  | 0     |
| 1m  | < 1 month   | Simple attacks which require some simple and known vulnerabilities exploitations, such as vulnerabilities in external interfaces (e.g., BT and Wi-Fi) | 1     |
| 6m  | < 6 months  | Complex attack which require some preparation time, such writing tools, PoCs, etc.                                                                    | 4     |
| 3y  | < 3 years   | Very complex attacks which require vulnerability research in more complex systems such as embedded components with less accessible information.       | 10    |
| >3y | \>= 3 years | Require Long research time to perform and prepare the attack. Usually use for multiple and complex vulnerability exploitation, including 0-days.      | 19    |

### Expertise (Ex)

| ID  | Level            | Description                                                                                                                                                                                                                                                                                                                                                                                                                                | Value |
| --- | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----- |
| L   | Layman           | Laymen are unknowledgeable compared to experts or proficient persons, with no particular expertise. Example: Ordinary person using step-by-step descriptions of an attack that is publicly available.                                                                                                                                                                                                                                      | 0     |
| P   | Proficient       | Proficient persons are knowledgeable in that they are familiar with the security behaviour of the product or system type. Examples: experienced owner, ordinary technician knowing simple, popular attacks, e.g., odometer tuning, installation of counterfeit parts.                                                                                                                                                                      | 3     |
| E   | Expert           | Experts are familiar with the underlying algorithms, protocols, hardware, structures, security behaviour, principles and concepts of security employed, techniques and tools for the definition of new attacks, cryptography, classical attacks for the product type, attack methods, etc.implemented in the product or system type. Example: Specially experienced technician or engineer.                                                | 6     |
| ME  | Multiple Experts | The level "Multiple Expert" is introduced to allow for a situation, where different fields of expertise are required at an Expert level for distinct steps of an attack. Example: Highly experienced engineer who has expertise in different fields which are required at an Expert level for distinct steps of an attack. Knows also very recent state-of-the-art (academic) attacks, e.g., side-channels, cryptanalysis, 0-day exploits. | 8     |


### Knowledge of Item (K)

| ID  | Level                             | Description                                                                                                                                                                                                                                                     | Value |
| --- | --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----- |
| P   | Public information                | Public information concerning the product (e.g., as gained from the Internet). Example: Information and documents published on the product homepage or on a internet forum.                                                                                     | 0     |
| R   | Restricted information            | Restricted information concerning the product (e.g., knowledge that is controlled within the developer organization and shared with other organizations under a NDA). Example: Source code and internal documentation shared between manufacturer and supplier. | 3     |
| C   | Confidential information          | Sensitive information about the product (e.g., knowledge that is shared between discrete teams within the developer organization, access to which is constrained only to members of the specified teams). Example: Immobilizer-related information.             | 7     |
| SC  | Strictly confidential information | Critical information about the product (e.g., knowledge that is known by only a few individuals, access to which is very tightly controlled on a strict need to know basis and individual undertaking). Example: Secret root signing key.                       | 11    |

### Window of Opportunity (W)

| ID  | Level     | Description                                                                                                                                                                                                                                                                                                                                     | Value |
| --- | --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----- |
| U   | Unlimited | High availability via public/untrusted network without any time limitation (i.e., asset is always accessible). Remote access without physical presence or time limitation as well as unlimited physical access to the item or component. Example: Attack is carried out remotely (e.g. cellular interfaces) without need for any preconditions. | 0     |
| E   | Easy      | High availability and limited access time. Remote access without physical presence to the item or component. Examples: Short range wireless communications (Bluetooth, Wi-Fi), remote software update, remote attack.                                                                                                                           | 1     |
| M   | Moderate  | Low availability of the item or component. Limited physical and/or logical access. Physical access to the system or component without using any special tools. Example: Attacker is able to get access to the system and itsexposed phyiscal interface, e.g., physical access via USB.                                                          | 4     |
| D   | Difficult | Very low availability of the item or component. Impractical level of access to the item or component to perform the attack. Example: Decapping an IC to extract information.                                                                                                                                                                    | 10    |

### Equipment (Eq)

| ID  | Level            | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | Value |
| --- | ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----- |
| ST  | Standard         | Standard equipment is readily available to the attacker, either for the identification of a vulnerability or for an attack. This equipment may be a part of the product itself (e.g., a debugger in an operating system), or can be readily obtained (e.g., Internet downloads, protocol analyzer or simple attack scripts). Example: A laptop, a CAN adapter, a universal diagnostic tester, or ordinary tools(e.g., screwdriver, soldering iron, pliers).                                                                                                                  | 0     |
| SP  | Specialized      | Specialized equipment is not readily available to the attacker, but could be acquired without undue effort. This could include purchase of moderate amounts of equipment (e.g., power analysis tools, use of hundreds of PCs linked across the Internet would fall into this category), or development of more extensive attack scripts or programs. If clearly different test benches consisting of specialized equipment are required for distinct steps of an attack this would be rated as bespoke. Example: A specialized hardware debugging device or an oscilloscope. | 4     |
| B   | Bespoke          | Bespoke equipment is not readily available to the public as it may need to be specially produced (e.g., very sophisticated software), or because the equipment is so specialized that its distribution is controlled, possibly even restricted. Alternatively, the equipment may be very expensive. Example: Manufacturer-restricted tools or equipment costing more than 50 000 Euro, e.g., a electron microscope.                                                                                                                                                          | 7     |
| MB  | Multiple Bespoke | The level "Multiple Bespoke" is introduced to allow for a situation, where different types of bespoke equipment are required for distinct steps of an attack.                                                                                                                                                                                                                                                                                                                                                                                                                | 9     |

## Risk Matrix as Matrix

|          | Negligible | Moderate | Major    | Severe   |
| -------- | ---------- | -------- | -------- | -------- |
| Very Low | Very Low   | Very Low | Very Low | Low      |
| Low      | Very Low   | Low      | Low      | Medium   |
| Medium   | Very Low   | Low      | Medium   | High     |
| High     | Very Low   | Medium   | High     | Critical |

## Risk Matrix as Table

| Impact Level | Feasibility Level | Risk Level | ID  |
| ------------ | ----------------- | ---------- | --- |
| Severe       | High              | Critical   | 1   |
| Severe       | Medium            | High       | 2   |
| Severe       | Low               | Medium     | 3   |
| Severe       | Very Low          | Low        | 4   |
| Major        | High              | High       | 5   |
| Major        | Medium            | Medium     | 6   |
| Major        | Low               | Low        | 7   |
| Major        | Very Low          | Very Low   | 8   |
| Moderate     | High              | Medium     | 9   |
| Moderate     | Medium            | Low        | 10  |
| Moderate     | Low               | Low        | 11  |
| Moderate     | Very Low          | Very Low   | 12  |
| Negligible   | High              | Very Low   | 13  |
| Negligible   | Medium            | Very Low   | 14  |
| Negligible   | Low               | Very Low   | 15  |
| Negligible   | Very Low          | Very Low   | 16  |

"""),
}