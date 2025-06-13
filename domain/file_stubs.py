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

work in progress: will give help for selecting impact ratings and feasibility ratings for the attack trees.
"""),
}