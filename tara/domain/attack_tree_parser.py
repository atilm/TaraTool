import os
import re
from tara.domain.attack_tree import AttackTree, AttackTreeNode, AttackTreeOrNode, AttackTreeAndNode, AttackTreeLeafNode, AttackTreeReferenceNode
from tara.domain.feasibility import Feasibility, ElapsedTime, Expertise, Knowledge, WindowOfOpportunity, Equipment
from tara.utilities.error_logger import IErrorLogger
from tara.MarkdownLib.markdown_parser import MarkdownTable
from tara.domain.object_store import ObjectStore
from tara.domain.feasibility_conversion import *

class AttackTreeParser:
    def __init__(self, logger: IErrorLogger, object_store: ObjectStore):
        self.logger = logger
        self.object_store = object_store

    def parse_attack_tree(self, table: MarkdownTable, attack_tree_id: str) -> AttackTree:
        try:
            node: AttackTreeNode = None
            prev_node: AttackTreeNode = None
            node_stack: list[AttackTreeNode] = []
            prev_indentation: int = 0
            indentation: int = 0
            root_node_count: int = 0

            for row in range(table.getRowCount()):
                # determine indentation and node name
                name = table.getCell(row, 0)

                prev_indentation = indentation
                indentation = 0
                while name.startswith("-"):
                    name = name[1:]
                    indentation += 1

                # ToDo: check that indentation is even
                # Convert number of dashes to indentation level:
                indentation = indentation // 2
                name = name.strip()

                if indentation == 0:
                    root_node_count += 1
                    if root_node_count > 1:
                        self.logger.log_error(f"Multiple root nodes found in attack tree {attack_tree_id}. Only one root node is allowed.")
                        return AttackTree(attack_tree_id)

                comment = table.getCell(row, 9)
                reasoning = table.getCell(row, 7)
                security_control_ids = table.getCell(row, 8).strip().split() if table.getCell(row, 8) else []
                
                prev_node = node
                node: AttackTreeNode = None

                row_type = table.getCell(row, 1)
                if row_type == "OR":
                    node = AttackTreeOrNode(self.object_store)
                elif row_type == "AND":
                    node = AttackTreeAndNode(self.object_store)
                elif row_type == "LEAF" or row_type == "":
                    feasibility = Feasibility()
                    feasibility.time = AttackTreeParser.parse_elapsed_time_static(table.getCell(row, 2), attack_tree_id, self.logger)
                    feasibility.expertise = AttackTreeParser.parse_expertise_static(table.getCell(row, 3), attack_tree_id, self.logger)
                    feasibility.knowledge = AttackTreeParser.parse_knowledge_static(table.getCell(row, 4), attack_tree_id, self.logger)
                    feasibility.window_of_opportunity = AttackTreeParser.parse_window_of_opportunity_static(table.getCell(row, 5), attack_tree_id, self.logger)
                    feasibility.equipment = AttackTreeParser.parse_equipment_static(table.getCell(row, 6), attack_tree_id, self.logger)
                    node = AttackTreeLeafNode(feasibility, self.object_store)
                elif row_type == "REF":
                    node = AttackTreeReferenceNode(self.object_store)
                    match = re.match(r"\[(.*?)\]\((.*?)\)", name)
                    if match:
                        name = match.group(1)
                        ref_path = match.group(2)
                        node.referenced_node_id = os.path.splitext(os.path.basename(ref_path))[0]
                    else:
                        self.logger.log_error(f"Invalid reference node format in attack tree {attack_tree_id}: '{name}'")

                else:
                    self.logger.log_error(f"Invalid node type found in attack tree {attack_tree_id}: '{row_type}'")
                    continue

                node.name = name
                node.comment = comment
                node.reasoning = reasoning
                node.security_control_ids = security_control_ids

                indentation_delta = indentation - prev_indentation
                if indentation_delta == 1:
                    node_stack.append(prev_node)
                elif indentation_delta < 0:
                    for _ in range(-indentation_delta):
                        node_stack.pop()
                elif indentation_delta > 1:
                    # ToDo: log this as an error instead of rasing an exception
                    raise ValueError(f"Invalid indentation level in attack tree {attack_tree_id}: {indentation_delta}")
                
                if len(node_stack) != 0:
                    node_stack[-1].add_child(node)    
            tree =  AttackTree(attack_tree_id)
            tree.root_node = node_stack[0] if len(node_stack) > 0 else node
            return tree
        except Exception as e:
            self.logger.log_error(f"Error parsing attack tree {attack_tree_id}")
            return AttackTree(attack_tree_id)

    @staticmethod
    def parse_elapsed_time_static(s: str, tree_id: str, logger: IErrorLogger) -> ElapsedTime:
        try:
            return parse_elapsed_time(s)
        except EmptyStringError:
            logger.log_warning(f"Empty elapsed time string found in attack tree {tree_id}. Defaulting to easiest rating.")
            return ElapsedTime.OneWeek
        except InvalidStringError:
            logger.log_error(f"Invalid elapsed time string found in attack tree {tree_id}: '{s}'")
            return ElapsedTime.OneWeek

    @staticmethod
    def parse_expertise_static(s: str, tree_id: str, logger: IErrorLogger) -> Expertise:
        try:
            return parse_expertise(s)
        except EmptyStringError:
            logger.log_warning(f"Empty expertise string found in attack tree {tree_id}. Defaulting to easiest rating.")
            return Expertise.Layman
        except InvalidStringError:
            logger.log_error(f"Invalid expertise string found in attack tree {tree_id}: '{s}'")
            return Expertise.Layman

    @staticmethod
    def parse_knowledge_static(s: str, tree_id: str, logger: IErrorLogger) -> Knowledge:
        try:
            return parse_knowledge(s)
        except EmptyStringError:
            logger.log_warning(f"Empty knowledge string found in attack tree {tree_id}. Defaulting to easiest rating.")
            return Knowledge.Public
        except InvalidStringError:
            logger.log_error(f"Invalid knowledge string found in attack tree {tree_id}: '{s}'")
            return Knowledge.Public

    @staticmethod
    def parse_window_of_opportunity_static(s: str, tree_id: str, logger: IErrorLogger) -> WindowOfOpportunity:
        try:
            return parse_window_of_opportunity(s)
        except EmptyStringError:
            logger.log_warning(f"Empty window of opportunity string found in attack tree {tree_id}. Defaulting to easiest rating.")
            return WindowOfOpportunity.Unlimited
        except InvalidStringError:
            logger.log_error(f"Invalid window of opportunity string found in attack tree {tree_id}: '{s}'")
            return WindowOfOpportunity.Unlimited

    @staticmethod
    def parse_equipment_static(s: str, tree_id: str, logger: IErrorLogger) -> Equipment:
        try:
            return parse_equipment(s)
        except EmptyStringError:
            logger.log_warning(f"Empty equipment string found in attack tree {tree_id}. Defaulting to easiest rating.")
            return Equipment.Standard
        except InvalidStringError:
            logger.log_error(f"Invalid equipment string found in attack tree {tree_id}: '{s}'")
            return Equipment.Standard