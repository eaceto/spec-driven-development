# 004: Requirements

Notation: one SHALL statement per requirement with at least one scenario. IDs are REQ-004-xx and are never reused.

## Capability: website

### REQ-004-01: Build and deploy on push
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
The site build SHALL declare its dependencies with exact versions in one requirements file used only by continuous integration, and the repository SHALL remain readable as plain Markdown without installing anything.

#### Scenario: Reproducible build
- GIVEN the requirements file
- WHEN it is installed on a fresh machine
- THEN the same versions are installed and `mkdocs build --strict` succeeds

### REQ-004-03: Home page order
The home page SHALL present, in order, what spec-driven development is and why this method exists, the fifteen-minute first change, and the map of the reference, and SHALL state which agents are tested and which are untested.

#### Scenario: First screen
- GIVEN a reader opening the home page
- WHEN they read from the top
- THEN they meet the one-sentence definition and the state diagram before any command, and reach the tutorial link before the reference links

### REQ-004-04: Tutorial from install to archive with real transcripts
The tutorial SHALL walk a reader from installing the skills to archiving a first change in six steps, SHALL show each step with content tabs for Claude Code and Devin CLI, SHALL include on each step a transcript from a real Claude Code run stating the date it was captured, and SHALL state in the Devin CLI tab that the request is the same and that a transcript is added when one is captured.

#### Scenario: Step page
- GIVEN the tutorial step for planning
- WHEN the reader opens it
- THEN they see the prompt to give the agent, a Claude Code tab with what the agent said and did and the date, and a Devin CLI tab that names the same request and says a transcript is pending

### REQ-004-05: Entry pages by role
The site SHALL have one entry page for developers and one for team leads, each opening with the questions that role brings and linking into the tutorial and the reference.

#### Scenario: Lead arrives
- GIVEN a team lead landing on their entry page
- WHEN they read it
- THEN ownership, approval, the constitution and the index are explained before any command, with links to the method document sections

### REQ-004-06: One copy of every rule
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
The site SHALL have an agents page listing Claude Code and Devin CLI as tested, and other agents that read the open skills standard as untested, with the install locations each reads.

#### Scenario: Untested agent
- GIVEN a reader using an agent other than Claude Code or Devin CLI
- WHEN they open the agents page
- THEN they find it listed as untested, with the directory it is expected to read

### REQ-004-08: Greenfield example
The repository SHALL contain `examples/greenfield-go`, the trial project as the skills produced it, passing the validator with zero violations, and the site SHALL tell its history as one narrative page from the first question to the archived capability.

#### Scenario: Example validates
- GIVEN `examples/greenfield-go`
- WHEN `python3 specs/validate.py --root examples/greenfield-go` runs
- THEN the exit code is 0

### REQ-004-09: Reading time
Every authored page SHALL stay under 1000 words, excluding the included method document and the generated pages.

#### Scenario: Long page
- GIVEN an authored page of 1300 words
- WHEN the test suite runs
- THEN the page is reported as over the limit

### REQ-004-10: UK English
Authored pages SHALL use UK spelling, and the test suite SHALL reject a fixed list of US spellings in them.

#### Scenario: US spelling
- GIVEN a page containing "organize"
- WHEN the test suite runs
- THEN the page is reported with the word

### REQ-004-11: Diagrams render
The site SHALL render Mermaid fenced blocks as diagrams, and the home page SHALL show the state diagram of the method this way.

#### Scenario: State diagram
- GIVEN the home page source with a `mermaid` fence
- WHEN the site is built
- THEN the configuration routes `mermaid` fences to the diagram renderer

### REQ-004-12: Title and address
The site SHALL be titled "Spec-driven development" and SHALL declare the repository's github.io address as its site URL.

#### Scenario: Configuration
- GIVEN `mkdocs.yml`
- WHEN it is read
- THEN `site_name` is "Spec-driven development" and `site_url` is the github.io address of this repository

## Capability: ci

### REQ-004-13: Checks on pull requests
A GitHub Actions workflow SHALL run the validator, the test suite and a strict site build on every pull request and every push to main, and SHALL fail when any of them fails.

#### Scenario: Failing validator
- GIVEN a pull request that leaves a change directory misnamed
- WHEN the workflow runs
- THEN the checks fail and name the validator step

## Modified requirements

None.

## Removed requirements

None.

## Not testable

- REQ-004-01 scenario "Clean push" and REQ-004-13 depend on GitHub's runners; they are verified by the workflow runs recorded in the checklist, not by the local test suite.
