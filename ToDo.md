# To Do

## Refactoring

* [ ] Remove duplication of header contents

## Next

* [ ] Refactor Report builder and improve error handling
* [ ] Output more information about object on exception in ObjectStore
* [ ] Empty assets and controls tables should not lead to errors -> ignore completely empty rows
* [ ] Complete the generated report
  * [.] Insert complete attack trees (with calculated feasibilities and updated reference links)
* [ ] Find a possibility to persistently document the handling of remaining risks
* [ ] Detect circular references in attack trees

## Features List

* [.] Check for duplicate IDs
  * [x] Damage Scenarios
  * [x] Assets
  * [x] Attack Trees (is already implemented by using file names, but do it anyway)
  * [x] Security Controls
  * [ ] Security Goals
* [.] Check for references to non-existing IDs
  * [x] Assets to Damage Scenarios
  * [ ] Mentions in Reasonings and Comments
* [x] Parse Damage Scenarios
* [x] Parse Assets
* [.] Generate & Update Attack Tree Stubs
  * [ ] Update Attack Tree stubs to example from parser test
  * [ ] Move as much as possible of the attack tree file stub content to file_stubs.py -> here was a wrong test!
  * [x] Create AttackTrees directory
  * [x] Create correct content
  * [x] Do not overwrite existing files
* [ ] Parse Attack Trees
  * [x] Only output warnings for empty attack trees and generate easiest feasibility, so that I can view results of an incomplete analysis
  * [x] Parse all files in the AttackTrees subdirectory
    * [x] TAT will be "Technical Attack Trees"
    * [x] CIRC_<ControlId> will be "Circumvent Trees" (both could be user conventions)
    * [x] Circumvent Trees should be able to reference controls, too.
  * [x] Only accept defined node types (empty = leaf)
  * [x] Parse Leaf Nodes
  * [x] Test for all existing feasibility ratings
  * [x] Parse Reference Nodes
    * [x] Reference has unexpected format
    * [x] Referenced trees do not exist
* [x] Feasibility-Calculation
  * [x] Feasibility level
  * [x] Feasibility and
  * [x] Feasibility or
  * [x] Calculation in attack trees
    * [x] Include Reference Nodes
* [x] Risk Calculation
* [.] Create report
  * [ ] Add existing damage scenarios
  * [ ] Add existing controls
  * [ ] Link from threat scenarios to damage scenarios
  * [ ] Link from threat scenario feasibilities to existing attack trees
  * [ ] Add extended attack trees (feasibilities, circumvent trees)
  * [ ] Link from threat scenario feasibilities to extended attack trees
  * [ ] Create table of contents
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