# 009: Requirements

Notation: one SHALL statement per requirement with at least one scenario. IDs are REQ-009-xx and are never reused.

## Capability: website

### REQ-009-01: Home page first screen
The home page SHALL define agents in its first paragraph, give the reason to adopt in three sentences before the call to action, and state the prerequisites and a realistic total time beside the call to action.

#### Scenario: Visitor reads the first screen
- GIVEN the home page source
- WHEN it is read from the top to the tutorial button
- THEN the words "agent" and a definition appear in the first paragraph, a reason-to-adopt block precedes the button, and git, Python and a time in minutes appear beside it

### REQ-009-02: Glossary and single Devin note
The tutorial overview SHALL carry a glossary of change, capability, gate, tier and the five statuses, one line each, and one note on Devin CLI; step tabs for Devin SHALL say only that the request is the same.

#### Scenario: No pending notes
- GIVEN the tutorial pages
- WHEN they are searched for "being added"
- THEN nothing is found, and the overview defines "gate"

### REQ-009-03: A refusal is shown
Tutorial step 3 SHALL show the recorded refusal of `sdd-plan` on a draft change, verbatim from the run, under a heading that invites the reader to try it.

#### Scenario: Refusal present
- GIVEN step 3
- WHEN it is read
- THEN a section shows the agent refusing to plan with the words "Gate 1" and the date of the run

### REQ-009-04: No product comparisons
No site page and not the README SHALL name spec-kit, Kiro or OpenSpec.

#### Scenario: Grep
- GIVEN every Markdown file under docs/ and the README
- WHEN searched case-insensitively for those three names
- THEN nothing is found

### REQ-009-05: Adoption and questions pages
The site SHALL have a page on adopting an existing project built from the recorded brownfield run, and a page of questions people ask with short answers linking into the method, both in the navigation.

#### Scenario: Pages present
- GIVEN the navigation
- WHEN it is read
- THEN both pages are listed, each under 1000 words

### REQ-009-06: Skills pages open with the request
Each generated skill page SHALL open, after its heading, with the request a person says to the agent to trigger that skill.

#### Scenario: Generated page
- GIVEN the hook renders `sdd-new`
- WHEN the output is read
- THEN a "Say to your agent" line appears before the skill's sections

### REQ-009-07: Rules link to capabilities
The generated validator rules page SHALL link every requirement id to its capability spec in the repository.

#### Scenario: Linked id
- GIVEN the rules page output
- WHEN REQ-001-02 appears
- THEN it is a link to the spec-layout capability spec

### REQ-009-08: Example pages carry no counts
Example pages SHALL show the validator command without hard-coded output counts.

#### Scenario: Counts absent
- GIVEN the two example pages
- WHEN searched for "rules"
- THEN no line of the form "N violations, N files, N rules" is present

### REQ-009-09: Logo and favicon
The theme SHALL configure a logo icon and a favicon file that exists in the docs folder.

#### Scenario: Configuration
- GIVEN mkdocs.yml
- WHEN read
- THEN `favicon` points to a file that exists and `logo` is set

## Modified requirements

None.

## Removed requirements

None.

## Not testable

- The method page's on-this-page list and the collapsed blocks are judged by reading; the word limits are tested.
