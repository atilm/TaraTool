# Todos

## Refactorings

* [ ] Remove duplication of header contents

## Features

* [.] Check for duplicate IDs
  * [x] Damage Scenarios
  * [x] Assets
  * [x] Attack Trees (is already implemented by using file names, but do it anyway)
  * [ ] Security Goals
  * [ ] Security Controls
* [.] Check for references to non-existing IDs
  * [x] Assets to Damage Scenarios
  * [ ] Mentions in Reasonings and Comments
* [x] Parse Damage Scenarios
* [x] Parse Assets
* [.] Generate & Update Attack Tree Stubs
  * [ ] Update Attack Tree stubs to example from parser test
  * [ ] Move as much as possible of the attack tree file stub content to file_stubs.py
  * [x] Create AttackTrees directory
  * [x] Create correct content
  * [x] Do not overwrite existing files
* [ ] Parse Attack Trees
  * [ ] Only output warnings for empty attack trees and generate easiest feasibility, so that I can view results of an incomplete analysis
  * [ ] Parse all files in the AttackTrees subdirectory
    * [ ] TAT will be "Technical Attack Trees"
    * [ ] CIRC_<ControlId> will be "Circumvent Trees"
  * [x] Only accept defined node types (empty = leaf)
  * [x] Parse Leaf Nodes
  * [x] Test for all existing feasibility ratings
  * [x] Parse Reference Nodes
    * [x] Reference has unexpected format
    * [x] Referenced trees do not exist
* [ ] Feasibility-Calculation
  * [x] Feasibility level
  * [x] Feasibility and
  * [x] Feasibility or
  * [x] Calculation in attack trees
    * [ ] Include Reference Nodes
* [ ] Risk Calculation
* [ ] Create report
* [ ] Update IDs -> VSCode search / replace?
* [ ] Simple but non-trivial example document

### Error Cases

* [ ] AttackTrees
  * [x] Non-existent feasibility rating
  * [x] Unknown node type
  * [x] Missing Attack Tree Table -> File Name in error message
  * [x] Multiple level-0 nodes
  * [x] Non-zero indentation for root-node
  * [x] And or Or-Nodes without children
  * [ ] Empty table -> probably caught by general error
  * [ ] uneven number of indentations -> unnecessary restriction?
  * [ ] Output warnings for unneeded attack tree files
* [x] Missing Assumptions Table
* [ ] Missing Files
  * [ ] Assumptions
  * [ ] ...
* [ ] Mis-formatted tables
* [x] Damage Scenarios: only accept defined impacts