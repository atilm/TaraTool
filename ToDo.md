# Todos

## Refactorings

* [ ] Remove duplication of header contents

## Features

* [.] Check for duplicate IDs
  * [x] Damage Scenarios
  * [x] Assets
  * [ ] Attack Trees
  * [ ] Security Goals
  * [ ] Security Controls
* [.] Check for references to non-existing IDs
  * [x] Assets to Damage Scenarios
  * [ ] Mentions in Reasonings and Comments
* [x] Parse Damage Scenarios
* [x] Parse Assets
* [.] Generate & Update Attack Tree Stubs
  * [x] Create AttackTrees directory
  * [x] Create correct content
  * [x] Do not overwrite existing files
  * [ ] Output warnings for unneeded attack tree files
* [ ] Parse Attack Trees
  * [ ] Only accept defined feasibility ratings
  * [ ] Only accept defined node types (empty = leaf)
* [ ] Feasibility-Calculation
* [ ] Risk Calculation
* [ ] Create report
* [ ] Update IDs -> VSCode search / replace?
* [ ] Simple but non-trivial example document

### Error Cases

* [x] Missing Assumptions Table
* [ ] Missing Files
  * [ ] Assumptions
  * [ ] ...
* [ ] Misformatted tables
* [x] Damage Scenarios: only accept defined impacts