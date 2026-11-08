---
id: lifecycle
title: Lifecycle
owner: maintainers
updated: 2026-11-08
---

# Lifecycle

## Purpose

How a change moves from idea to living truth: the five states, the three gates, the claim rule for teams, approval and ownership, commit traceability, the loading rule and the archive step that merges requirements into capabilities. Exists so that specs cannot drift from the code without someone noticing.

## Requirements

### REQ-001-16: States
Origin: 001

Every change SHALL have exactly one status from the set draft, approved, in-progress, done, archived, and SHALL move only forward through that sequence.

#### Scenario: Skipping a state
- GIVEN a change with `status: approved`
- WHEN its status is set to `done`
- THEN validation reports an invalid transition

### REQ-001-17: Gate 1, approval
Origin: 001

When a change moves from draft to approved, its `spec.md` SHALL have been merged to the main branch through a pull request reviewed by the owner of every capability listed in its frontmatter, and `approved_by` and `approved_at` SHALL be set.

#### Scenario: Owner review
- GIVEN a change touching capability `auth` owned by team identity
- WHEN the pull request containing `spec.md` is merged with an approving review from team identity
- THEN status becomes approved and `approved_by` names the reviewer and `approved_at` the date

### REQ-001-18: Claim rule
Origin: 001

When a team works in parallel, the first merge to the main branch for a change SHALL contain only its directory and `spec.md`, and when two changes claim the same number, the one merged later SHALL be renumbered.

#### Scenario: Collision
- GIVEN two branches each creating change 012
- WHEN the second is merged after the first
- THEN the second is renumbered to 013 before merge

### REQ-001-19: No code before approval
Origin: 001

When a change has status draft, the change SHALL have no `design.md` content beyond the template and no code committed against it.

#### Scenario: Agent asked to implement a draft
- GIVEN a change with `status: draft`
- WHEN an agent is asked to implement it
- THEN the agent declines and points to Gate 1

### REQ-001-20: Gate 2, done
Origin: 001

When a change moves from in-progress to done, every item in the Gate 2 section of its `checklist.md` SHALL be ticked, and every requirement ID SHALL be referenced by at least one test or listed under Not testable with a reason.

#### Scenario: Untested requirement
- GIVEN REQ-014-03 has no test referencing it and is not listed under Not testable
- WHEN the change is moved to done
- THEN the move is refused and REQ-014-03 is named

### REQ-001-21: Gate 3, archive
Origin: 001

When a change moves from done to archived, the archive step SHALL merge its added requirements into their capability specs with Origin set, replace modified requirements in place, list removed requirements under Retired, append a History line to each touched capability, move the change directory to `specs/archive/`, and regenerate `INDEX.md`.

#### Scenario: Archive refused with unmerged requirements
- GIVEN a change with requirements not yet present in their capability specs
- WHEN status is set to archived by editing the frontmatter
- THEN validation reports the change as archived with unmerged requirements

### REQ-001-22: Loading rule
Origin: 001

When a person or an agent works on a change, they SHALL load the constitution, the index, that change, and only the capability specs that change lists.

#### Scenario: Agent instructions
- GIVEN `AGENTS.md` at the repository root
- WHEN an agent is asked to work on change 014
- THEN the agent reads `specs/constitution.md`, `specs/INDEX.md`, `specs/changes/014-*/` and the listed capabilities, and does not read other changes

### REQ-001-23: Commit traceability
Origin: 001

When a commit belongs to a change, the commit message SHALL carry a `Change: NNN` trailer and MAY carry a `Requirements:` trailer listing the requirement IDs the commit covers, and the title of a pull request for a change SHALL start with the change number.

#### Scenario: Finding a change's commits
- GIVEN change 014 with several commits over two weeks
- WHEN `git log --grep "^Change: 014"` is run
- THEN all of that change's commits are listed and no others

#### Scenario: Requirement coverage from history
- GIVEN a commit with `Requirements: REQ-014-01, REQ-014-03`
- WHEN Gate 2 is checked
- THEN REQ-014-01 and REQ-014-03 count as having implementation commits

## Retired

## History
- 001 (2026-11-08): Spec layout and lifecycle
- 006 (2026-11-08): Clarifications from the 0.2.0 review
