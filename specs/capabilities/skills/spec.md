---
id: skills
title: Skills
owner: maintainers
updated: 2026-11-08
---

# Skills

## Purpose

The six procedures that carry a change through the lifecycle: init, new, plan, implement, verify and archive. Each is a vendor-neutral skill that an agent runs and a person can follow by hand, with fixed preconditions and refusals, so the lifecycle is enforced rather than remembered. Exists so that every project and every agent runs the same process.

## Requirements

### REQ-002-01: Skill format
Origin: 002

Every skill SHALL live at `skills/<name>/SKILL.md` with frontmatter `name`, `description` and `metadata` holding `version` and `sdd_version`, and SHALL not exceed 150 lines including frontmatter.

#### Scenario: Oversized skill
- GIVEN a `SKILL.md` of 180 lines
- WHEN the skills are validated
- THEN the skill is reported as exceeding the limit

### REQ-002-02: Skill body sections
Origin: 002

Every skill body SHALL contain, in order, the sections When to use, Preconditions, Steps, Refuse when, and Done when, so that a person can follow it by hand.

#### Scenario: Reading a skill as a procedure
- GIVEN a developer with no agent available
- WHEN they open `skills/sdd-new/SKILL.md`
- THEN they can perform the step by following the numbered Steps section

### REQ-002-03: Vendor-neutral bodies
Origin: 002

No skill body SHALL contain a tool-specific path, command or product name; tool-specific detail SHALL live only in the install step and its documentation.

#### Scenario: Grep for vendor paths
- GIVEN all `SKILL.md` files
- WHEN their bodies are searched for `.claude`, `.devin`, `.agents` or an agent product name
- THEN no match is found

### REQ-002-04: Install locations
Origin: 002

When skills are installed into a project, the install step SHALL copy each skill directory to `.agents/skills/<name>/` and `.claude/skills/<name>/` in that project, SHALL write the installed version into `sdd_version` in the project's constitution frontmatter, and SHALL create any agent-specific entry file that points to `AGENTS.md` for agents that do not read `AGENTS.md` themselves.

#### Scenario: Fresh install
- GIVEN a project with `specs/constitution.md` and no skills
- WHEN the install step runs for version 0.1.0
- THEN both locations contain the six skill directories, the constitution reads `sdd_version: 0.1.0`, and any agent-specific entry file the install step knows about points to `AGENTS.md`

### REQ-002-05: Loading rule in skills
Origin: 002

Every skill except `sdd-init` SHALL read only `specs/constitution.md`, `specs/INDEX.md`, the target change directory, the templates, and the capability specs listed in the target change's frontmatter.

#### Scenario: Agent with many changes present
- GIVEN a project with thirty changes
- WHEN `sdd-plan` runs for change 014
- THEN only the constitution, the index, the templates, change 014 and its listed capabilities are opened

### REQ-002-06: Status preconditions
Origin: 002

Every skill that acts on a change SHALL read the change's status before acting and SHALL refuse, naming the gate or state required, when the status is not one it may act on: `sdd-plan` requires approved; `sdd-implement` requires approved or in-progress; `sdd-verify` requires in-progress; `sdd-archive` requires done.

#### Scenario: Plan on a draft
- GIVEN a change with `status: draft`
- WHEN `sdd-plan` is invoked
- THEN it writes nothing and reports that Gate 1 has not been passed

#### Scenario: Archive on in-progress
- GIVEN a change with `status: in-progress`
- WHEN `sdd-archive` is invoked
- THEN it writes nothing and reports that the change must reach done through `sdd-verify`

### REQ-002-07: Init for a new project
Origin: 002

When `sdd-init` runs in a project without `specs/`, it SHALL create the layout required by REQ-001-01, copy the templates, write the constitution from the template using answers to at most five questions, write an empty index, and write an `AGENTS.md` containing the loading rule. Agent-specific entry files are the install step's concern, per REQ-002-04.

#### Scenario: Empty repository
- GIVEN a repository with no `specs/` directory
- WHEN `sdd-init` completes
- THEN the layout satisfies REQ-001-01, the constitution satisfies REQ-001-13, and `AGENTS.md` exists at the root

### REQ-002-08: Init for an existing project
Origin: 002

When `sdd-init` runs in a project with existing code and no `specs/`, it SHALL derive the constitution from existing material such as the README, architecture decisions and CI configuration without inventing rules, and SHALL write a capability map as capability specs containing Purpose and owner only, with no requirements.

#### Scenario: Brownfield adoption
- GIVEN a repository with a README and CI configuration
- WHEN `sdd-init` completes
- THEN every principle in the constitution can be traced to a sentence in the existing material, and `specs/capabilities/` holds one folder per identified capability with an empty Requirements section

### REQ-002-09: New change
Origin: 002

When `sdd-new` runs, it SHALL ask at most five clarifying questions, write `spec.md` from the template in the order required by REQ-001-06, assign the number required by REQ-001-03, name the directory as required by REQ-001-02, and add a row with status draft to the index.

#### Scenario: Conversation to spec
- GIVEN a developer describing a feature in a few sentences
- WHEN `sdd-new` completes
- THEN a directory `NNN-name_of_change/` exists with `spec.md` whose Why section precedes its What section, and the index lists it as draft

### REQ-002-10: New writes spec.md only
Origin: 002

`sdd-new` SHALL create no file other than `spec.md` in the change directory.

#### Scenario: Claim rule respected
- GIVEN `sdd-new` has completed
- WHEN the change directory is listed
- THEN it contains exactly `spec.md`

### REQ-002-11: Plan
Origin: 002

When `sdd-plan` runs on an approved change, it SHALL write the files its tier requires per REQ-001-04: `requirements.md` grouped by capability with IDs `REQ-NNN-01` onward, `design.md` with at least one recorded decision, `tasks.md` whose tasks cite requirement IDs, and `checklist.md` with the Gate 1 items ticked according to the frontmatter; it SHALL then set status to in-progress and update the index row.

#### Scenario: Standard tier plan
- GIVEN an approved change with `tier: standard`
- WHEN `sdd-plan` completes
- THEN the directory contains the five standard files, every task cites at least one requirement ID, and the status is in-progress

### REQ-002-12: Plan respects the quick tier
Origin: 002

When `sdd-plan` runs on a change with `tier: quick`, it SHALL write only `tasks.md` and `checklist.md` and SHALL refuse to write any requirement, directing the author to raise the tier if behaviour changes.

#### Scenario: Quick change needing a requirement
- GIVEN a quick change whose description implies new behaviour
- WHEN `sdd-plan` runs
- THEN it stops before writing and reports that the tier must be raised to standard

### REQ-002-13: Implement one task
Origin: 002

When `sdd-implement` runs, it SHALL take the first unticked task in `tasks.md`, implement it together with tests that reference the task's requirement IDs, commit with a `Change:` trailer and a `Requirements:` trailer listing those IDs, and tick the task; it SHALL process one task per invocation unless asked to continue.

#### Scenario: Single task
- GIVEN `tasks.md` with T03 as the first unticked task citing REQ-014-02
- WHEN `sdd-implement` completes
- THEN T03 is ticked, a commit exists with `Requirements: REQ-014-02`, and T04 is still unticked

### REQ-002-14: Implement stops on contradiction
Origin: 002

When a task cannot be completed without contradicting a requirement or without a requirement that does not exist, `sdd-implement` SHALL stop, leave `requirements.md` unchanged, and report the conflict with the requirement IDs involved.

#### Scenario: Missing requirement
- GIVEN a task whose correct implementation needs behaviour no requirement describes
- WHEN `sdd-implement` reaches it
- THEN no code is written for it and the report names the gap

### REQ-002-15: Verify
Origin: 002

When `sdd-verify` runs on an in-progress change, it SHALL evaluate every Gate 2 item in `checklist.md`, report each as passed or failed with the evidence found, list every requirement ID with no referencing test and no Not testable entry, and SHALL set status to done and tick the items only when every item passes.

#### Scenario: One uncovered requirement
- GIVEN all tasks ticked and REQ-014-03 referenced by no test
- WHEN `sdd-verify` runs
- THEN the status stays in-progress and the report names REQ-014-03

### REQ-002-16: Archive merge
Origin: 002

When `sdd-archive` runs on a done change, it SHALL, for each capability named in `requirements.md`, create the capability spec from the template if absent, append added requirements with `Origin: NNN`, replace modified requirements in place adding `Changed in: NNN`, move removed requirements to Retired with the reason, append a History line, and set `updated`; it SHALL then move the change directory to `specs/archive/`, set status to archived, and regenerate the index.

#### Scenario: First archive creates capabilities
- GIVEN change 001 is done and `specs/capabilities/` is empty
- WHEN `sdd-archive` completes
- THEN `capabilities/spec-layout/spec.md` and `capabilities/lifecycle/spec.md` exist, together they contain every requirement of 001 with `Origin: 001`, and `specs/archive/001-spec_layout_and_lifecycle/` exists

### REQ-002-17: Archive refuses inconsistent input
Origin: 002

`sdd-archive` SHALL refuse and write nothing when the change is not done, or when a capability named in `requirements.md` is absent from the change's `capabilities` frontmatter.

#### Scenario: Unlisted capability
- GIVEN a done change whose `requirements.md` names capability `billing` not present in its frontmatter
- WHEN `sdd-archive` is invoked
- THEN nothing is written and the report names `billing`

### REQ-002-18: Index maintenance
Origin: 002

`sdd-new`, `sdd-plan`, `sdd-verify` and `sdd-archive` SHALL update the index row of the change they act on, including status and updated date, in the same operation.

#### Scenario: Status visible without opening the change
- GIVEN `sdd-verify` has just moved change 014 to done
- WHEN `INDEX.md` is read
- THEN the row for 014 shows done and today's date

### REQ-002-19: Validator is optional
Origin: 002

When a validator is installed in the project, every skill SHALL run it before reporting completion and include its result; when no validator is installed, every skill SHALL perform the structural checks it depends on by reading the files, and SHALL behave the same in both cases.

#### Scenario: No validator present
- GIVEN a project without a validator
- WHEN `sdd-plan` completes
- THEN it has checked file presence per tier and requirement grouping by reading the files, and reports that no validator was found

## Retired

## History
- 002 (2026-11-08): Lifecycle skills
