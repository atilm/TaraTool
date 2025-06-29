from tara.domain.feasibility import *
from tara.domain.attack_tree_parser import AttackTreeParser
from tara.domain.attack_tree import *
from tara.domain.security_control import SecurityControl
from tara.utilities.error_logger import MemoryErrorLogger
from tara.MarkdownLib.markdown_parser import MarkdownParser, MarkdownDocument

class AttackTreeTestCase:
    def __init__(self):
        self.logger = MemoryErrorLogger()
        self.object_store = ObjectStore(MemoryErrorLogger())

    def register_control(self, control_id: str, is_active: bool):
        """
        Registers a security control in the object store.
        """
        control = SecurityControl()
        control.id = control_id
        control.name = f"Control {control_id}"
        control.security_goal = "Goal"
        control.is_active = is_active
        self.object_store.add(control)

    def parse_attack_tree(self, attack_tree_description: str, attack_tree_id: str) -> AttackTree:
        parser = MarkdownParser()
        document: MarkdownDocument = parser.parse(attack_tree_description)

        table = document.getContent()[1]

        att_parser = AttackTreeParser(self.logger, self.object_store)
        tree = att_parser.parse_attack_tree(table, attack_tree_id)

        self.object_store.add(tree)

        return tree    