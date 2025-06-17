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
  * [x] Only accept defined node types (empty = leaf)
  * [x] Parse Leaf Nodes
  * [x] Test for all existing feasibility ratings
  * [ ] Parse Reference Nodes
* [ ] Feasibility-Calculation
  * [ ] Include Reference Nodes
* [ ] Risk Calculation
* [ ] Create report
* [ ] Update IDs -> VSCode search / replace?
* [ ] Simple but non-trivial example document

### Error Cases

* [ ] AttackTrees
  * [ ] None-existent feasibility rating
  * [ ] uneven number of indentations
  * [ ] Non-zero indentation for root-node
  * [ ] And or Or-Nodes without children
  * [ ] Unknown node type
  * [ ] Multiple level-0 nodes
  * [ ] Mssing Attack Tree Table -> File Name in error message
  * [ ] Output warnings for unneeded attack tree files
* [x] Missing Assumptions Table
* [ ] Missing Files
  * [ ] Assumptions
  * [ ] ...
* [ ] Misformatted tables
* [x] Damage Scenarios: only accept defined impacts