class FileStub:
    def __init__(self, file_path: str, file_content: str):
        self.path = file_path
        self.content = file_content


file_stubs = [
    FileStub("00_SystemDescritpion.md", 
"""# System Description and Scope

Describe the systems interfaces, data flows, and any external systems that interact with the system.
Use drawio.png files or mermaid diagrams to illustrate the system architecture.
"""),
    FileStub("01_Assumptions.md", 
"""# Assumptions

| ID  | Name | Security Claim | Comment |
| --- | ---- | -------------- | ------- |
|     |      |                |         |
"""),
    FileStub("02_Assets.md", 
"""# Assets

| ID  | Name | Availability | Integrity | Confidentiality | Reasoning | Description |
| --- | ---- | ------------ | --------- | --------------- | --------- | ----------- |
|     |      |              |           |                 |           |             |
"""),
    FileStub("03_DamageScenarios.md", 
"""# Damage Scenarios

| ID  | Name | Safety | Operational | Financial | Privacy | Reasoning | Comment |
| --- | ---- | ------ | ----------- | --------- | ------- | --------- | ------- |
|     |      |        |             |           |         |           |         |
"""),
    FileStub("MethodDescription.md",
"""# Method Description

work in progress: will give help for selecting impacct ratings and feasibility ratings for the attack trees.
"""),
]