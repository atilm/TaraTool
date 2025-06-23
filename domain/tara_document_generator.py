from utilities.error_logger import ErrorLogger
from MarkdownLib.markdown_document import *
from MarkdownLib.markdown_document_builder import *

class TaraDocumentGenerator:
    def __init__(self, error_logger: ErrorLogger):
        self.error_logger = error_logger

    def generate(self, tara) -> MarkdownDocument:
        # Placeholder: implement document generation logic here
        # For now, just print a message and simulate writing a file

        title_level = 0
        h1 = 1

        return MarkdownDocumentBuilder() \
            .withSection("Threat Analysis And Risk Assessment (TARA) Report", title_level) \
            .withSection("Threat Scenarios", h1) \
            .withTable(self._build_threat_scenario_table(tara)) \
            .build()

    def _build_threat_scenario_table(self, tara) -> MarkdownTable:
        return MarkdownTableBuilder() \
                .withHeader(["Threat Scenario", "Description", "Risk Level", "Mitigation Strategy"]) \
                .withRow(["Example Threat Scenario", "This is a description of the threat scenario.", "High", "Implement security measures."]) \
                .build()