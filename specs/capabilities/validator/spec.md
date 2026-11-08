---
id: validator
title: Validator
owner: maintainers
updated: 2026-11-08
---

# Validator

## Purpose

Mechanical enforcement of the method: one standard-library Python file that checks the structural rules of the layout and the lifecycle, names the requirement behind every violation, and is run by the skills before they report. Exists so that the rules are enforced rather than remembered.

## Requirements

### REQ-003-01: Single standard-library file
Origin: 003

The validator SHALL be one file, `specs/validate.py`, that imports only modules from the Python standard library and runs on Python 3.9 or later.

#### Scenario: Import audit
- GIVEN `specs/validate.py`
- WHEN its import statements are collected
- THEN every imported module is in the standard library

### REQ-003-02: Invocation and exit codes
Origin: 003

When run with no arguments the validator SHALL check the whole `specs/` tree of the current project; when run with a three-digit change number it SHALL check that change alone; it SHALL exit 0 with no violations, 1 with violations, and 2 on a usage error.

#### Scenario: Clean tree
- GIVEN a project with no violations
- WHEN `python3 specs/validate.py` runs
- THEN the exit code is 0

#### Scenario: Single change with a fault
- GIVEN change 014 has a requirement without a scenario
- WHEN `python3 specs/validate.py 014` runs
- THEN the exit code is 1 and the report names change 014's `requirements.md`

#### Scenario: Bad argument
- GIVEN the argument `abc`
- WHEN the validator runs
- THEN the exit code is 2

### REQ-003-03: Report format
Origin: 003

The validator SHALL print one line per violation in the form `<path>: <rule-id> (<requirement-ids>): <message>`, followed by one summary line stating the number of violations, files and rules checked.

#### Scenario: One violation
- GIVEN exactly one violation in `specs/changes/014-x/spec.md`
- WHEN the validator runs
- THEN the output has one violation line starting with that path and containing a rule id and a requirement id, and a final summary line

### REQ-003-04: Rules are data and listable
Origin: 003

Every check SHALL be registered once as a rule with an id, the requirement ids it enforces and a one-line description, and `--rules` SHALL print that list; every structural requirement of change 001 SHALL be named by at least one rule.

#### Scenario: Listing
- GIVEN the validator
- WHEN it runs with `--rules`
- THEN every line names a rule id, its requirement ids and its description, and REQ-001-01 through REQ-001-23 except REQ-001-12 and REQ-001-15 each appear at least once

### REQ-003-05: Layout rule
Origin: 003

The validator SHALL report a violation when `specs/` contains any visible entry other than `constitution.md`, `INDEX.md`, `templates/`, `capabilities/`, `changes/`, `archive/` and `validate.py`, or lacks any of the first six.

#### Scenario: Stray file
- GIVEN `specs/notes.md` exists
- WHEN the validator runs
- THEN a violation names `specs/notes.md` and REQ-001-01

#### Scenario: Validator present
- GIVEN `specs/validate.py` exists beside the six entries
- WHEN the validator runs
- THEN no layout violation is reported

### REQ-003-06: Naming and numbering rules
Origin: 003

The validator SHALL report a violation when a directory in `specs/changes/` or `specs/archive/` does not match `NNN-name_of_change`, when its `id` frontmatter differs from its prefix, or when two directories across both folders share a number.

#### Scenario: Bad name
- GIVEN `specs/changes/12-Passwordless-Login/`
- WHEN the validator runs
- THEN a violation names that directory and REQ-001-02

#### Scenario: Collision
- GIVEN `specs/changes/012-a/` and `specs/archive/012-b/`
- WHEN the validator runs
- THEN a violation names both directories and REQ-001-18

### REQ-003-07: Tier files rule
Origin: 003

The validator SHALL report a violation when a change directory lacks a file its tier requires or contains a file its tier does not allow, where quick allows `spec.md`, `tasks.md` and `checklist.md`, standard adds `requirements.md` and `design.md`, and full adds `guardrails.md`.

#### Scenario: Missing design
- GIVEN a standard change without `design.md` and status in-progress
- WHEN the validator runs
- THEN a violation names the directory, `design.md` and REQ-001-04

#### Scenario: Quick with requirements
- GIVEN a quick change containing `requirements.md`
- WHEN the validator runs
- THEN a violation cites REQ-001-04 and REQ-001-05

### REQ-003-08: Spec order rule
Origin: 003

The validator SHALL report a violation when the level-two headings of a change's `spec.md` are not, in order, Why it matters, What should be done, Scope, Success criteria, optionally followed by Constraints specific to this change, or when Scope lacks an Out subsection with at least one bullet.

#### Scenario: What before Why
- GIVEN a `spec.md` whose first heading is What should be done
- WHEN the validator runs
- THEN a violation names the file and REQ-001-06

### REQ-003-09: Frontmatter rule
Origin: 003

The validator SHALL report a violation when a change's `spec.md` lacks any of `id`, `title`, `status`, `tier`, `owner`, `capabilities`, `ticket`, `docs`, `approved_by`, `approved_at`, `created`, `updated`, when `status` or `tier` is outside its allowed set, when a non-empty date is not `YYYY-MM-DD`, or when status is approved or later and `approved_by` or `approved_at` is empty.

#### Scenario: Approved without approver
- GIVEN `status: approved` and `approved_by:` empty
- WHEN the validator runs
- THEN a violation cites REQ-001-17

#### Scenario: Optional links empty
- GIVEN `ticket:` and `docs:` present and empty
- WHEN the validator runs
- THEN no frontmatter violation is reported

### REQ-003-10: Requirement grammar rule
Origin: 003

The validator SHALL report a violation when a requirement block in `requirements.md` lacks a heading of the form `### REQ-NNN-xx: Title`, lacks exactly one statement line containing `SHALL`, lacks at least one `#### Scenario:` with GIVEN, WHEN and THEN bullets, when an added requirement's NNN differs from the change's id, or when a modified requirement lacks `Changed in: <change id>`.

#### Scenario: No scenario
- GIVEN a requirement with a SHALL statement and no scenario
- WHEN the validator runs
- THEN a violation names the requirement id and REQ-001-08

#### Scenario: AND accepted
- GIVEN a scenario with GIVEN, WHEN, THEN and AND bullets
- WHEN the validator runs
- THEN no grammar violation is reported

### REQ-003-11: Grouping rule
Origin: 003

The validator SHALL report a violation when a `## Capability:` heading in `requirements.md` names a capability absent from the change's `capabilities` frontmatter, when an added requirement sits outside a capability section, or when the sections Modified requirements, Removed requirements and Not testable are missing.

#### Scenario: Unlisted capability
- GIVEN `## Capability: billing` and frontmatter `capabilities: [auth]`
- WHEN the validator runs
- THEN a violation names `billing` and REQ-001-09

### REQ-003-12: Capability spec rule
Origin: 003

The validator SHALL report a violation when a capability spec is not at `specs/capabilities/<id>/spec.md` with `id` equal to its directory, lacks `title`, `owner` or `updated`, lacks the sections Purpose, Requirements, Retired and History in order, has a requirement block without `Origin:`, or when a requirement id appears in more than one capability or both as active and retired.

#### Scenario: Missing origin
- GIVEN a capability requirement block without an `Origin:` line
- WHEN the validator runs
- THEN a violation names the id and REQ-001-11

#### Scenario: Reused id
- GIVEN REQ-003-02 is active in capability `a` and listed under Retired in capability `b`
- WHEN the validator runs
- THEN a violation cites REQ-001-10

### REQ-003-13: Status consistency rule
Origin: 003

The validator SHALL report a violation when a draft change contains any file other than `spec.md`; when a done change has an unticked task, an unticked Gate 2 item, or a requirement id that appears in no test file and is not listed under Not testable; when an archived change is under `specs/changes/`, a change under `specs/archive/` is not archived, or an archived change has an added requirement absent from its capability spec, a modified one without `Changed in`, a removed one not under Retired, or an unticked Gate 3 item; and, when the project is a git repository, when a status has moved backwards relative to the committed version.

#### Scenario: Draft with design
- GIVEN a draft change containing `design.md`
- WHEN the validator runs
- THEN a violation cites REQ-001-19

#### Scenario: Done but uncovered
- GIVEN a done change whose REQ-014-03 is in no test file and not under Not testable
- WHEN the validator runs
- THEN a violation names REQ-014-03 and cites REQ-001-20

#### Scenario: Archived by hand
- GIVEN `status: archived` in a change still under `specs/changes/`
- WHEN the validator runs
- THEN a violation cites REQ-001-21

#### Scenario: Backward transition
- GIVEN the committed `spec.md` says done and the working copy says in-progress
- WHEN the validator runs in that repository
- THEN a violation cites REQ-001-16

### REQ-003-14: Index rule
Origin: 003

The validator SHALL report a violation when `specs/INDEX.md` lacks the sections Active changes, Capabilities and Archived changes, when the set of numbers in Active changes differs from the directories in `specs/changes/`, when a row's status, tier, owner, capabilities or updated date differs from the change's frontmatter, when the Capabilities rows differ from `specs/capabilities/` in ids or requirement counts, or when the archived count differs from the directories in `specs/archive/`.

#### Scenario: Stale status
- GIVEN change 014 is in-progress and its index row says approved
- WHEN the validator runs
- THEN a violation names `specs/INDEX.md`, change 014 and REQ-001-14

### REQ-003-15: Constitution and entry file rules
Origin: 003

The validator SHALL report a violation when `specs/constitution.md` lacks `extends`, `version`, `owner`, `numbering` or `sdd_version`, lacks the sections Purpose, Principles, Definitions and Amendments, or exceeds 80 lines, and when the project root lacks an `AGENTS.md` that names `specs/constitution.md` and `specs/INDEX.md`.

#### Scenario: Long constitution
- GIVEN a constitution of 120 lines
- WHEN the validator runs
- THEN a violation cites REQ-001-13

#### Scenario: No entry file
- GIVEN no `AGENTS.md` at the root
- WHEN the validator runs
- THEN a violation cites REQ-001-22

### REQ-003-16: Commit trailer rule
Origin: 003

When the project is a git repository, the validator SHALL report a violation for each of the most recent ten commits that touches `specs/changes/NNN-*` or `specs/archive/NNN-*` and lacks a `Change: NNN` trailer.

#### Scenario: Missing trailer
- GIVEN the latest commit edits `specs/changes/014-x/tasks.md` and has no `Change:` trailer
- WHEN the validator runs
- THEN a violation names that commit and cites REQ-001-23

### REQ-003-17: Skills rules
Origin: 003

When the project root contains `skills/`, the validator SHALL report a violation for a `skills/<name>/SKILL.md` that exceeds 150 lines, whose `name` differs from its directory, that lacks `description`, `metadata.version` or `metadata.sdd_version`, whose level-two sections are not When to use, Preconditions, Steps, Refuse when, Done when in order, or whose body contains `.claude`, `.devin`, `.agents` or an agent product name.

#### Scenario: Vendor path in body
- GIVEN a skill body mentioning `.claude/skills`
- WHEN the validator runs
- THEN a violation cites REQ-002-03

### REQ-003-18: Installation
Origin: 003

When `install.sh` runs against a project, it SHALL copy `specs/validate.py` into the project's `specs/` and set `validator: python3 specs/validate.py` in the project's constitution frontmatter if that file exists; in link mode against this repository it SHALL set the key without copying.

#### Scenario: Install into a project
- GIVEN a project with `specs/constitution.md` and no validator
- WHEN `install.sh <project>` runs
- THEN `<project>/specs/validate.py` exists and the constitution contains `validator: python3 specs/validate.py`

### REQ-003-19: Self-tests
Origin: 003

The validator SHALL ship with `tests/test_validate.py`, runnable with `python3 -m unittest`, containing for every rule at least one case that passes and one that fails, each test naming the requirement ids it covers.

#### Scenario: Run the suite
- GIVEN the repository
- WHEN `python3 -m unittest discover tests` runs
- THEN every test passes and the test source mentions every REQ-003 id and every REQ-001 id named by a rule

### REQ-003-20: Clean on real projects
Origin: 003

When run on this repository and on the trial sandbox at the state they are in when this change is verified, the validator SHALL report zero violations.

#### Scenario: This repository
- GIVEN this repository after the layout amendment
- WHEN `python3 specs/validate.py` runs at its root
- THEN the exit code is 0

## Retired

## History
- 003 (2026-11-08): Spec validator
