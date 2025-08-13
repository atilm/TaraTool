import sys, os
from tara.domain.file_stubs import file_stubs
from tara.domain.tara_parser import TaraParser
from tara.domain.attack_tree_stub_generator import AttackTreeStubGenerator
from tara.domain.tara_document_generator import TaraDocumentGenerator
from tara.domain.threat_scenario_document_generator import ThreatScenarioDocumentGenerator
from tara.utilities.file_reader import FileReader
from tara.utilities.file_writer import FileWriter
from tara.utilities.error_logger import ErrorLogger
from tara.MarkdownLib.markdown_writer import MarkdownWriter

usage_help = "Usage: python tara.py [init|check|gentrees|generate]"

def init():
    """The init command initializes the directory tara with stubs for the necessary files."""

    print("Initializing...")
    os.makedirs("tara", exist_ok=True)

    for file_stub in file_stubs.values():
        file_path = os.path.join("tara", file_stub.path)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write(file_stub.content)

def check():
    print("Checking...")
    parser = TaraParser(FileReader(), ErrorLogger())
    parser.parse(".")

def generate_attack_trees():
    print("Parsing input files...")
    error_logger = ErrorLogger()
    parser = TaraParser(FileReader(), error_logger)
    directory = "."
    tara = parser.parse(directory)
    if error_logger.has_errors():
        print("Errors found during parsing. Please fix them before generating attack trees.")
        sys.exit(1)
        
    print("Generating attack trees...")
    generator = AttackTreeStubGenerator(FileWriter(), error_logger)
    generator.update_stubs(tara, directory)

def generate():
    print("Generating...")
    error_logger = ErrorLogger()
    parser = TaraParser(FileReader(), error_logger)
    directory = "."
    tara = parser.parse(directory)
    if error_logger.has_errors():
        print("Errors found during parsing. Please fix them before generating the document.")
        sys.exit(1)

    threat_scenario_generator = ThreatScenarioDocumentGenerator()
    threat_scenarios_document = threat_scenario_generator.generate(tara)
    
    generator = TaraDocumentGenerator(error_logger)
    document = generator.generate(tara)
    if error_logger.has_errors():
        print("Errors found tara generation.")
        sys.exit(1)

    with open("06_ThreatScenarios.md", 'w') as f:
        writer = MarkdownWriter()
        f.write(writer.write(threat_scenarios_document))

    with open("tara_report.md", 'w') as f:
        writer = MarkdownWriter()
        f.write(writer.write(document))

def main():
    if len(sys.argv) < 2:
        print(usage_help)
        sys.exit(1)
    command = sys.argv[1]
    if command == "init":
        init()
    elif command == "check":
        check()
    elif command == "gentrees":
        generate_attack_trees()
    elif command == "generate":
        generate()
    else:
        print(f"Unknown command: {command}")
        print(usage_help)
        sys.exit(1)

if __name__ == "__main__":
    main()
