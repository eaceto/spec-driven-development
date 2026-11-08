---
id: website
title: Website
owner: maintainers
updated: 2026-11-08
---

# Website

## Purpose

The teaching site at https://eaceto.github.io/spec-driven-development/: what the method is and why, a first change in fifteen minutes with real transcripts, entry pages by role, and a reference generated from the repository's own files so that no rule exists in two copies. Exists so that a newcomer can learn the method without cloning anything.

## Requirements

### REQ-004-01: Build and deploy on push
Origin: 004

When a commit reaches the main branch, a GitHub Actions workflow SHALL build the site with MkDocs in strict mode and deploy it to the repository's GitHub Pages address, failing the build on any broken internal link.

#### Scenario: Clean push
- GIVEN a push to main with valid pages
- WHEN the workflow runs
- THEN the site is published at the repository's github.io address

#### Scenario: Broken link
- GIVEN a page linking to a path that does not exist
- WHEN the workflow runs
- THEN the build fails and nothing is deployed

### REQ-004-02: Pinned build dependencies, nothing required offline
Origin: 004

The site build SHALL declare its dependencies with exact versions in one requirements file used only by continuous integration, and the repository SHALL remain readable as plain Markdown without installing anything.

#### Scenario: Reproducible build
- GIVEN the requirements file
- WHEN it is installed on a fresh machine
- THEN the same versions are installed and `mkdocs build --strict` succeeds

### REQ-004-03: Home page order
Origin: 004

The home page SHALL present, in order, what spec-driven development is and why this method exists, the fifteen-minute first change, and the map of the reference, and SHALL state which agents are tested and which are untested.

#### Scenario: First screen
- GIVEN a reader opening the home page
- WHEN they read from the top
- THEN they meet the one-sentence definition and the state diagram before any command, and reach the tutorial link before the reference links

### REQ-004-04: Tutorial from install to archive with real transcripts
Origin: 004

The tutorial SHALL walk a reader from installing the skills to archiving a first change in six steps, SHALL show each step with content tabs for Claude Code and Devin CLI, SHALL include on each step a transcript from a real Claude Code run stating the date it was captured, and SHALL state in the Devin CLI tab that the request is the same and that a transcript is added when one is captured.

#### Scenario: Step page
- GIVEN the tutorial step for planning
- WHEN the reader opens it
- THEN they see the prompt to give the agent, a Claude Code tab with what the agent said and did and the date, and a Devin CLI tab that names the same request and says a transcript is pending

### REQ-004-05: Entry pages by role
Origin: 004

The site SHALL have one entry page for developers and one for team leads, each opening with the questions that role brings and linking into the tutorial and the reference.

#### Scenario: Lead arrives
- GIVEN a team lead landing on their entry page
- WHEN they read it
- THEN ownership, approval, the constitution and the index are explained before any command, with links to the method document sections

### REQ-004-06: One copy of every rule
Origin: 004

The site SHALL serve the method document from `docs/method.md` as it stands, and SHALL generate its skills, templates and validator pages at build time from `skills/*/SKILL.md`, `specs/templates/` and the validator's rule list, so that no rule text is hand-copied into a site page.

#### Scenario: Skill page
- GIVEN `skills/sdd-new/SKILL.md`
- WHEN the site is built
- THEN a skills page exists whose body is that file's body, without the frontmatter, and editing the skill changes the page on the next build

#### Scenario: Validator page
- GIVEN the validator's rule list
- WHEN the site is built
- THEN the validator page lists every rule id, its requirement ids and its description

### REQ-004-07: Agents page
Origin: 004

The site SHALL have an agents page listing Claude Code and Devin CLI as tested, and other agents that read the open skills standard as untested, with the install locations each reads.

#### Scenario: Untested agent
- GIVEN a reader using an agent other than Claude Code or Devin CLI
- WHEN they open the agents page
- THEN they find it listed as untested, with the directory it is expected to read

### REQ-004-08: Greenfield example
Origin: 004

The repository SHALL contain `examples/greenfield-go`, the trial project as the skills produced it, passing the validator with zero violations, and the site SHALL tell its history as one narrative page from the first question to the archived capability.

#### Scenario: Example validates
- GIVEN `examples/greenfield-go`
- WHEN `python3 specs/validate.py --root examples/greenfield-go` runs
- THEN the exit code is 0

### REQ-004-09: Reading time
Origin: 004

Every authored page SHALL stay under 1000 words, excluding the included method document and the generated pages.

#### Scenario: Long page
- GIVEN an authored page of 1300 words
- WHEN the test suite runs
- THEN the page is reported as over the limit

### REQ-004-10: UK English
Origin: 004

Authored pages SHALL use UK spelling, and the test suite SHALL reject a fixed list of US spellings in them.

#### Scenario: US spelling
- GIVEN a page containing "organize"
- WHEN the test suite runs
- THEN the page is reported with the word

### REQ-004-11: Diagrams render
Origin: 004

The site SHALL render Mermaid fenced blocks as diagrams, and the home page SHALL show the state diagram of the method this way.

#### Scenario: State diagram
- GIVEN the home page source with a `mermaid` fence
- WHEN the site is built
- THEN the configuration routes `mermaid` fences to the diagram renderer

### REQ-004-12: Title and address
Origin: 004

The site SHALL be titled "Spec-driven development" and SHALL declare the repository's github.io address as its site URL.

#### Scenario: Configuration
- GIVEN `mkdocs.yml`
- WHEN it is read
- THEN `site_name` is "Spec-driven development" and `site_url` is the github.io address of this repository

### REQ-007-01: Notes example
Origin: 007

The repository SHALL contain `examples/notes-python`, the tutorial's project as the skills produced it, passing the validator with zero violations, and the site SHALL tell its story on one page linked from the tutorial's last step.

#### Scenario: Example validates
- GIVEN `examples/notes-python`
- WHEN `python3 specs/validate.py --root examples/notes-python` runs
- THEN the exit code is 0

### REQ-009-01: Home page first screen
Origin: 009

The home page SHALL define agents in its first paragraph, give the reason to adopt in three sentences before the call to action, and state the prerequisites and a realistic total time beside the call to action.

#### Scenario: Visitor reads the first screen
- GIVEN the home page source
- WHEN it is read from the top to the tutorial button
- THEN the words "agent" and a definition appear in the first paragraph, a reason-to-adopt block precedes the button, and git, Python and a time in minutes appear beside it

### REQ-009-02: Glossary and single Devin note
Origin: 009

The tutorial overview SHALL carry a glossary of change, capability, gate, tier and the five statuses, one line each, and one note on Devin CLI; step tabs for Devin SHALL say only that the request is the same.

#### Scenario: No pending notes
- GIVEN the tutorial pages
- WHEN they are searched for "being added"
- THEN nothing is found, and the overview defines "gate"

### REQ-009-03: A refusal is shown
Origin: 009

Tutorial step 3 SHALL show the recorded refusal of `sdd-plan` on a draft change, verbatim from the run, under a heading that invites the reader to try it.

#### Scenario: Refusal present
- GIVEN step 3
- WHEN it is read
- THEN a section shows the agent refusing to plan with the words "Gate 1" and the date of the run

### REQ-009-04: No product comparisons
Origin: 009

No site page and not the README SHALL name spec-kit, Kiro or OpenSpec.

#### Scenario: Grep
- GIVEN every Markdown file under docs/ and the README
- WHEN searched case-insensitively for those three names
- THEN nothing is found

### REQ-009-05: Adoption and questions pages
Origin: 009

The site SHALL have a page on adopting an existing project built from the recorded brownfield run, and a page of questions people ask with short answers linking into the method, both in the navigation.

#### Scenario: Pages present
- GIVEN the navigation
- WHEN it is read
- THEN both pages are listed, each under 1000 words

### REQ-009-06: Skills pages open with the request
Origin: 009

Each generated skill page SHALL open, after its heading, with the request a person says to the agent to trigger that skill.

#### Scenario: Generated page
- GIVEN the hook renders `sdd-new`
- WHEN the output is read
- THEN a "Say to your agent" line appears before the skill's sections

### REQ-009-07: Rules link to capabilities
Origin: 009

The generated validator rules page SHALL link every requirement id to its capability spec in the repository.

#### Scenario: Linked id
- GIVEN the rules page output
- WHEN REQ-001-02 appears
- THEN it is a link to the spec-layout capability spec

### REQ-009-08: Example pages carry no counts
Origin: 009

Example pages SHALL show the validator command without hard-coded output counts.

#### Scenario: Counts absent
- GIVEN the two example pages
- WHEN searched for "rules"
- THEN no line of the form "N violations, N files, N rules" is present

### REQ-009-09: Logo and favicon
Origin: 009

The theme SHALL configure a logo icon and a favicon file that exists in the docs folder.

#### Scenario: Configuration
- GIVEN mkdocs.yml
- WHEN read
- THEN `favicon` points to a file that exists and `logo` is set

## Retired

## History
- 004 (2026-11-08): Teaching site on GitHub Pages
- 006 (2026-11-08): Clarifications from the 0.2.0 review
- 007 (2026-11-08): Fixes from the 0.2.0 review
- 009 (2026-11-08): Site improvements from the first review
