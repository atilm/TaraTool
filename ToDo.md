# Todos

## Refactorings

* [ ] Remove duplication of header contents

## Features

* [.] Check for duplicate IDs
  * [x] Damage Scenarios
  * [x] Assets
  * [ ] Attack Trees (is already implemented by using file names, but do it anyway)
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
  * [ ] Output warnings for unneeded attack tree files
* [ ] Parse Attack Trees
  * [ ] Test for all existing feasibility ratings
  * [ ] Only accept defined feasibility ratings
  * [ ] Only accept defined node types (empty = leaf)
  * [.] Parse Leaf Nodes
  * [ ] Parse Reference Nodes
* [ ] Feasibility-Calculation
  * [ ] Include Reference Nodes
* [ ] Risk Calculation
* [ ] Create report
* [ ] Update IDs -> VSCode search / replace?
* [ ] Simple but non-trivial example document

### Error Cases

* [x] Missing Assumptions Table
* [ ] Mssing Attack Tree Table -> File Name in error message
* [ ] Missing Files
  * [ ] Assumptions
  * [ ] ...
* [ ] Misformatted tables
* [x] Damage Scenarios: only accept defined impacts