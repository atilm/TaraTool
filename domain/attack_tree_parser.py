import os
import re
from domain.attack_tree import AttackTree, AttackTreeNode, AttackTreeOrNode, AttackTreeAndNode, AttackTreeLeafNode, AttackTreeReferenceNode
from domain.feasibility import Feasibility, ElapsedTime, Expertise, Knowledge, WindowOfOpportunity, Equipment
from utilities.error_logger import IErrorLogger
from MarkdownLib.markdown_parser import MarkdownTable

class AttackTreeParser:
    def __init__(self, logger: IErrorLogger):
        self.logger = logger

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
                name = name.strip()

                if indentation == 0:
                    root_node_count += 1
                    if root_node_count > 1:
                        self.logger.log_error(f"Multiple root nodes found in attack tree {attack_tree_id}. Only one root node is allowed.")
                        return AttackTree(attack_tree_id)

                comment = table.getCell(row, 9)
                reasoning = table.getCell(row, 7)
                
                prev_node = node
                node: AttackTreeNode = None

                row_type = table.getCell(row, 1)
                if row_type == "OR":
                    node = AttackTreeOrNode()
                elif row_type == "AND":
                    node = AttackTreeAndNode()
                elif row_type == "LEAF" or row_type == "":
                    feasibility = Feasibility()
                    feasibility.time = AttackTreeParser.parse_elapsed_time_static(table.getCell(row, 2), attack_tree_id, self.logger)
                    feasibility.expertise = AttackTreeParser.parse_expertise_static(table.getCell(row, 3), attack_tree_id, self.logger)
                    feasibility.knowledge = AttackTreeParser.parse_knowledge_static(table.getCell(row, 4), attack_tree_id, self.logger)
                    feasibility.window_of_opportunity = AttackTreeParser.parse_window_of_opportunity_static(table.getCell(row, 5), attack_tree_id, self.logger)
                    feasibility.equipment = AttackTreeParser.parse_equipment_static(table.getCell(row, 6), attack_tree_id, self.logger)
                    node = AttackTreeLeafNode(feasibility)
                elif row_type == "REF":
                    node = AttackTreeReferenceNode()
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

                if indentation > prev_indentation:
                    node_stack.append(prev_node)
                elif indentation < prev_indentation:
                    node_stack.pop()
                
                if len(node_stack) != 0:
                    node_stack[-1].add_child(node)    
            tree =  AttackTree(attack_tree_id)
            tree.root_node = node_stack[0]
            return tree
        except Exception:
            self.logger.log_error(f"Error parsing attack tree {attack_tree_id}")
            return AttackTree(attack_tree_id)

    @staticmethod
    def parse_elapsed_time_static(s: str, tree_id: str, logger: IErrorLogger) -> ElapsedTime:
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
        else:
            logger.log_error(f"Invalid elapsed time string found in attack tree {tree_id}: '{s}'")

    @staticmethod
    def parse_expertise_static(s: str, tree_id: str, logger: IErrorLogger) -> Expertise:
        if s == "L":
            return Expertise.Layman
        elif s == "P":
            return Expertise.Proficient
        elif s == "E":
            return Expertise.Expert
        elif s == "ME":
            return Expertise.MultipleExperts
        else:
            logger.log_error(f"Invalid expertise string found in attack tree {tree_id}: '{s}'")

    @staticmethod
    def parse_knowledge_static(s: str, tree_id: str, logger: IErrorLogger) -> Knowledge:
        if s == "P":
            return Knowledge.Public
        elif s == "R":
            return Knowledge.Restricted
        elif s == "C":
            return Knowledge.Confidential
        elif s == "SC":
            return Knowledge.StrictlyConfidential
        else:
            logger.log_error(f"Invalid knowledge string found in attack tree {tree_id}: '{s}'")

    @staticmethod
    def parse_window_of_opportunity_static(s: str, tree_id: str, logger: IErrorLogger) -> WindowOfOpportunity:
        if s == "U":
            return WindowOfOpportunity.Unlimited
        elif s == "E":
            return WindowOfOpportunity.Easy
        elif s == "M":
            return WindowOfOpportunity.Moderate
        elif s == "D":
            return WindowOfOpportunity.Difficult
        else:
            logger.log_error(f"Invalid window of opportunity string found in attack tree {tree_id}: '{s}'")

    @staticmethod
    def parse_equipment_static(s: str, tree_id: str, logger: IErrorLogger) -> Equipment:
        if s == "ST":
            return Equipment.Standard
        elif s == "SP":
            return Equipment.Specialized
        elif s == "B":
            return Equipment.Bespoke
        elif s == "MB":
            return Equipment.MultipleBespoke
        else:
            logger.log_error(f"Invalid equipment string found in attack tree {tree_id}: '{s}'")
