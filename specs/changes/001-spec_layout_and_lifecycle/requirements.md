# 001: Requirements

Notation: one SHALL statement per requirement with at least one scenario. IDs are REQ-001-xx and are never reused.

## Capability: spec-layout

### REQ-001-01: Directory layout
When a project adopts the method, the project SHALL contain a top-level `specs/` directory holding `constitution.md`, `INDEX.md`, `templates/`, `capabilities/`, `changes/` and `archive/`.

#### Scenario: Fresh project
- GIVEN a repository with no `specs/` directory
- WHEN the method is initialised
- THEN `specs/` exists with exactly those six entries, and `capabilities/`, `changes/` and `archive/` may be empty

### REQ-001-02: Change directory naming
When a change is created, its directory SHALL be named `NNN-name_of_change`, where NNN is three digits and the name is lowercase words joined by underscores.

#### Scenario: Valid name
- GIVEN a new change titled "Passwordless login"
- WHEN its directory is created
- THEN the directory is `012-passwordless_login` or an equivalent lowercase underscore name with a three-digit prefix

#### Scenario: Invalid name rejected
- GIVEN a directory named `12-Passwordless-Login`
- WHEN the layout is validated
- THEN the validation reports the directory as non-conforming

### REQ-001-03: Next number
When a change is created, its number SHALL be the highest number present in `changes/` and `archive/` plus one.

#### Scenario: Archive counts
- GIVEN `changes/` holds 004 and `archive/` holds 001, 002, 003 and 005
- WHEN a change is created
- THEN it is numbered 006

### REQ-001-04: Tiers and required files
When a change declares a tier, the change directory SHALL contain exactly the files that tier requires: quick requires `spec.md`, `tasks.md` and `checklist.md`; standard adds `requirements.md` and `design.md`; full adds `guardrails.md`.

#### Scenario: Standard tier
- GIVEN a change with `tier: standard`
- WHEN its directory is validated
- THEN `spec.md`, `requirements.md`, `design.md`, `tasks.md` and `checklist.md` are present and `guardrails.md` is absent

### REQ-001-05: Quick tier cannot change requirements
When a change has `tier: quick`, the change SHALL NOT add, modify or remove any requirement.

#### Scenario: Behaviour change forces standard tier
- GIVEN a change with `tier: quick`
- WHEN its author needs to add a requirement
- THEN the tier is raised to standard before the requirement is written

### REQ-001-06: Order of spec.md
The `spec.md` of every change SHALL present, in this order: why it matters, what should be done, scope with an explicit list of non-goals, and success criteria.

#### Scenario: Reader without code access
- GIVEN a reader who has not seen the codebase
- WHEN they read `spec.md` top to bottom
- THEN they encounter the purpose before any statement of what will be built, and they find at least one non-goal

### REQ-001-07: Change frontmatter
The `spec.md` of every change SHALL carry frontmatter with `id`, `title`, `status`, `tier`, `owner`, `capabilities`, `ticket`, `docs`, `approved_by`, `approved_at`, `created` and `updated`, where `ticket`, `docs`, `approved_by` and `approved_at` may be empty.

#### Scenario: Optional links empty
- GIVEN a change with no tracker ticket
- WHEN its frontmatter is validated
- THEN `ticket` is present and empty, and validation passes

### REQ-001-08: Requirement notation
Every requirement SHALL consist of a heading of the form `### REQ-NNN-xx: Title`, one SHALL statement, an optional `Ref:` line, and at least one scenario written as GIVEN, WHEN, THEN bullets.

#### Scenario: Missing scenario
- GIVEN a requirement with a SHALL statement and no scenario
- WHEN `requirements.md` is validated
- THEN the requirement is reported as incomplete

### REQ-001-09: Requirement grouping
Requirements in `requirements.md` SHALL be grouped under headings of the form `## Capability: <capability-id>`, and every capability named SHALL appear in the change's `capabilities` frontmatter.

#### Scenario: Unlisted capability
- GIVEN a requirement under `## Capability: billing`
- WHEN the change's frontmatter lists only `auth`
- THEN validation reports the mismatch

### REQ-001-10: Requirement ID stability
When a requirement is modified by a later change, the requirement SHALL keep its original ID and gain a `Changed in:` line; when a requirement is removed, its ID SHALL be listed under Retired in the capability spec and never reused.

#### Scenario: Modification keeps ID
- GIVEN REQ-003-02 exists in capability `auth`
- WHEN change 014 modifies it
- THEN the capability spec still contains REQ-003-02 with the new text and `Changed in: 014`

#### Scenario: Removal retires ID
- GIVEN REQ-003-04 exists in capability `auth`
- WHEN change 019 removes it and is archived
- THEN REQ-003-04 appears under Retired with change 019 and a reason, and no later change may create REQ-003-04

### REQ-001-11: Capability spec structure
Every capability SHALL live at `specs/capabilities/<capability-id>/spec.md` with frontmatter `id`, `title`, `owner` and `updated`, and sections Purpose, Requirements, Retired and History.

#### Scenario: New capability from archive
- GIVEN change 001 is archived with requirements under `## Capability: lifecycle`
- WHEN no `capabilities/lifecycle/` exists
- THEN the archive step creates `capabilities/lifecycle/spec.md` from the capability template with those requirements and `Origin: 001`

### REQ-001-12: Optional external links
A change SHALL accept an optional ticket link and an optional document link in its frontmatter, and a requirement SHALL accept an optional `Ref:` link, without the method depending on any particular tracker or wiki.

#### Scenario: Links present
- GIVEN a change with `ticket:` set to a tracker URL and a requirement with `Ref:` set to a wiki URL
- WHEN the change is validated
- THEN validation passes and neither URL is interpreted beyond being a link

### REQ-001-13: Constitution structure and configuration
Every project SHALL have `specs/constitution.md` with frontmatter `extends`, `version`, `owner`, `numbering` and `sdd_version`, and sections Purpose, Principles, Definitions and Amendments, fitting on one page.

#### Scenario: Extending an organisation constitution
- GIVEN an organisation constitution at version 1.2.0
- WHEN a project constitution declares `extends: org-constitution@1.2.0`
- THEN the project constitution may add principles and may not remove or weaken any inherited principle

### REQ-001-14: Index content
`specs/INDEX.md` SHALL list every active change with number, title, status, tier, owner, ticket, capabilities and updated date, every capability with id, title, owner, requirement count and updated date, and a count of archived changes.

#### Scenario: Reader finds a change
- GIVEN twenty active changes
- WHEN a reader opens `INDEX.md`
- THEN they can identify the change they need and its owner without opening any change directory

### REQ-001-15: Cross-repository identity
When a change or requirement is referenced from outside its repository, the reference SHALL take the form `repo-name:NNN` or `repo-name:NNN/REQ-xx`.

#### Scenario: Aggregated index
- GIVEN repositories `payments-api` and `web-app` each with a change 014
- WHEN both appear in an aggregated index
- THEN they are listed as `payments-api:014` and `web-app:014`

## Capability: lifecycle

### REQ-001-16: States
Every change SHALL have exactly one status from the set draft, approved, in-progress, done, archived, and SHALL move only forward through that sequence.

#### Scenario: Skipping a state
- GIVEN a change with `status: approved`
- WHEN its status is set to `done`
- THEN validation reports an invalid transition

### REQ-001-17: Gate 1, approval
When a change moves from draft to approved, its `spec.md` SHALL have been merged to the main branch through a pull request reviewed by the owner of every capability listed in its frontmatter, and `approved_by` and `approved_at` SHALL be set.

#### Scenario: Owner review
- GIVEN a change touching capability `auth` owned by team identity
- WHEN the pull request containing `spec.md` is merged with an approving review from team identity
- THEN status becomes approved and `approved_by` names the reviewer and `approved_at` the date

### REQ-001-18: Claim rule
When a team works in parallel, the first merge to the main branch for a change SHALL contain only its directory and `spec.md`, and when two changes claim the same number, the one merged later SHALL be renumbered.

#### Scenario: Collision
- GIVEN two branches each creating change 012
- WHEN the second is merged after the first
- THEN the second is renumbered to 013 before merge

### REQ-001-19: No code before approval
When a change has status draft, the change SHALL have no `design.md` content beyond the template and no code committed against it.

#### Scenario: Agent asked to implement a draft
- GIVEN a change with `status: draft`
- WHEN an agent is asked to implement it
- THEN the agent declines and points to Gate 1

### REQ-001-20: Gate 2, done
When a change moves from in-progress to done, every item in the Gate 2 section of its `checklist.md` SHALL be ticked, and every requirement ID SHALL be referenced by at least one test or listed under Not testable with a reason.

#### Scenario: Untested requirement
- GIVEN REQ-014-03 has no test referencing it and is not listed under Not testable
- WHEN the change is moved to done
- THEN the move is refused and REQ-014-03 is named

### REQ-001-21: Gate 3, archive
When a change moves from done to archived, the archive step SHALL merge its added requirements into their capability specs with Origin set, replace modified requirements in place, list removed requirements under Retired, append a History line to each touched capability, move the change directory to `specs/archive/`, and regenerate `INDEX.md`.

#### Scenario: Archive refused with unmerged requirements
- GIVEN a change with requirements not yet present in their capability specs
- WHEN status is set to archived by editing the frontmatter
- THEN validation reports the change as archived with unmerged requirements

### REQ-001-22: Loading rule
When a person or an agent works on a change, they SHALL load the constitution, the index, that change, and only the capability specs that change lists.

#### Scenario: Agent instructions
- GIVEN `AGENTS.md` at the repository root
- WHEN an agent is asked to work on change 014
- THEN the agent reads `specs/constitution.md`, `specs/INDEX.md`, `specs/changes/014-*/` and the listed capabilities, and does not read other changes

### REQ-001-23: Commit traceability
When a commit belongs to a change, the commit message SHALL carry a `Change: NNN` trailer and MAY carry a `Requirements:` trailer listing the requirement IDs the commit covers, and the title of a pull request for a change SHALL start with the change number.

#### Scenario: Finding a change's commits
- GIVEN change 014 with several commits over two weeks
- WHEN `git log --grep "^Change: 014"` is run
- THEN all of that change's commits are listed and no others

#### Scenario: Requirement coverage from history
- GIVEN a commit with `Requirements: REQ-014-01, REQ-014-03`
- WHEN Gate 2 is checked
- THEN REQ-014-01 and REQ-014-03 count as having implementation commits

## Modified requirements

None. This is the first change.

## Removed requirements

None.

## Not testable

- REQ-001-06 scenario "Reader without code access" relies on human judgement of readability. The structural part, section order, is testable and is what the validator checks.
