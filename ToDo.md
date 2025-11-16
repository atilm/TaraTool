# To Do


## Refactoring

* [ ] Remove Threat Scenario Document Generator
* [ ] Remove duplication of header contents

## Next

* [ ] Call pandoc from the app when report is generated
* [ ] Remove duplicate TOC from generated HTML
* [ ] Customize the reports title
* [ ] Add example document
* [ ] Add Readme documentation

* [ ] Test for non-existing control ids
* [ ] ToDo remove threat_scenario_document_generator
* [ ] Find a possibility to persistently document the handling of remaining risks
  * [ ] Output threat scenario in separate file
    * [ ] reference asset, security property and damage scenario
    * [ ] Column for specifying risk handling and security goal or security claim
    * [ ] Initial Risk and Mitigated Risk
  * [ ] Read-in threat scenario file if present and preserve risk handling entries
* [ ] Detect circular references in attack trees
* [ ] Refactor Report builder and improve error handling
* [ ] Output more information about object on exception in ObjectStore
* [ ] Empty assets and controls tables should not lead to errors -> ignore completely empty rows
* [ ] Complete the generated report
  * [x] Insert complete attack trees (with calculated feasibilities and updated reference links)

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
  * [ ] Title and Company
  * [x] Table of Contents
  * [ ] Summary: Initial and Final Risk Matrix
  * [ ] System Description inserted
  * [x] List of Assumptions -> translated into security claims
  * [x] Security Control with Link to Security Goal
  * [x] List of Damage Scenarios
  * [x] List of Assets with Security Properties (and damage when violated)
  * [x] List of Threats, List of Threat Scenarios
  * [x] List of Attack Trees. Leafs with detailed description and reasoning
  * [ ] List of Risk Treatments (reduce -> Security Goal, share -> Security Claim, retain -> Security Claim) Threat Scenarios grouped by damage scenario with initial risk, risk treatment, security goals and security claims
  * [-] List of Security Claims linked to assumptions (with responsible entities)
  * [-] List of Security Goals
  * [ ] Description of Methodology
* [ ] Update IDs -> VSCode search / replace?
* [ ] Simple but non-trivial example document

### Error Cases

* [ ] AttackTrees
  * [ ] Empty table -> probably caught by general error
  * [ ] Output warnings for unneeded attack tree files
* [ ] Missing Files
  * [ ] Assumptions
  * [ ] ...
* [ ] Mis-formatted tables