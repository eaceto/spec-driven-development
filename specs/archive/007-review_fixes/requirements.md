# 007: Requirements

Notation: one SHALL statement per requirement with at least one scenario. IDs are REQ-007-xx and are never reused.

## Capability: website

### REQ-007-01: Notes example
The repository SHALL contain `examples/notes-python`, the tutorial's project as the skills produced it, passing the validator with zero violations, and the site SHALL tell its story on one page linked from the tutorial's last step.

#### Scenario: Example validates
- GIVEN `examples/notes-python`
- WHEN `python3 specs/validate.py --root examples/notes-python` runs
- THEN the exit code is 0

## Capability: validator

### REQ-007-02: Block-style list diagnostic
When a frontmatter list is written in block style, one item per line starting with a dash, the validator SHALL report a violation on that file naming the key and the `[a, b]` form to use.

#### Scenario: Block list under capabilities
- GIVEN a `spec.md` whose frontmatter has `capabilities:` followed by `  - auth` on the next line
- WHEN the validator runs
- THEN a violation names `capabilities` and the form `[a, b]`

### REQ-007-03: Ticket numbering in the validator
When the constitution says `numbering: ticket`, the validator SHALL accept change directories named `KEY-123-name_of_change`, where KEY is upper-case letters and digits, and SHALL require the `id` to be `KEY-123`; when the constitution says `numbering: sequential`, such a directory SHALL be a violation.

#### Scenario: Ticket project
- GIVEN `numbering: ticket` and a directory `specs/changes/ABC-123-passwordless_login/` with `id: "ABC-123"`
- WHEN the validator runs
- THEN no naming or id violation is reported

#### Scenario: Sequential project
- GIVEN `numbering: sequential` and the same directory
- WHEN the validator runs
- THEN a violation cites REQ-001-02

## Modified requirements

### REQ-001-02: Change directory naming
Changed in: 007

When a change is created, its directory SHALL be named `NNN-name_of_change` where NNN is three digits, or `KEY-123-name_of_change` where `KEY-123` is a tracker key when the constitution says `numbering: ticket`, and the name is lowercase words joined by underscores.

#### Scenario: Valid sequential name
- GIVEN a new change titled "Passwordless login" and `numbering: sequential`
- WHEN its directory is created
- THEN the directory is `012-passwordless_login` or an equivalent lowercase underscore name with a three-digit prefix

#### Scenario: Valid ticket name
- GIVEN a new change for tracker key ABC-123 and `numbering: ticket`
- WHEN its directory is created
- THEN the directory is `ABC-123-passwordless_login` and the `id` is `ABC-123`

#### Scenario: Invalid name rejected
- GIVEN a directory named `12-Passwordless-Login`
- WHEN the layout is validated
- THEN the validation reports the directory as non-conforming

### REQ-002-01: Skill format
Changed in: 007

Every skill SHALL live at `skills/<name>/SKILL.md` with frontmatter `name`, `description` and `metadata` holding `sdd_version`, and SHALL not exceed 150 lines including frontmatter.

#### Scenario: Oversized skill
- GIVEN a `SKILL.md` of 180 lines
- WHEN the skills are validated
- THEN the skill is reported as exceeding the limit

#### Scenario: Missing version
- GIVEN a `SKILL.md` without `metadata.sdd_version`
- WHEN the skills are validated
- THEN the skill is reported

### REQ-003-13: Status consistency rule
Changed in: 007

The validator SHALL report a violation when a draft change contains any file other than `spec.md`; when a done change has an unticked task, an unticked Gate 2 item, or a requirement id that appears in no test file outside comment lines and is not listed under Not testable; when an archived change is under `specs/changes/`, a change under `specs/archive/` is not archived, or an archived change has an added requirement absent from its capability spec, a modified one without `Changed in`, a removed one not under Retired, or an unticked Gate 3 item; and, when the project is a git repository, when a status has moved backwards relative to the committed version.

#### Scenario: Draft with design
- GIVEN a draft change containing `design.md`
- WHEN the validator runs
- THEN a violation cites REQ-001-19

#### Scenario: Id only in a comment
- GIVEN a done change whose REQ-014-03 appears in a test file only on a line that is a comment
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

### REQ-003-17: Skills rules
Changed in: 007

When the project root contains `skills/`, the validator SHALL report a violation for a `skills/<name>/SKILL.md` that exceeds 150 lines, whose `name` differs from its directory, that lacks `description` or `metadata.sdd_version`, whose level-two sections are not When to use, Preconditions, Steps, Refuse when, Done when in order, or whose body contains `.claude`, `.devin`, `.agents` or an agent product name.

#### Scenario: Vendor path in body
- GIVEN a skill body mentioning `.claude/skills`
- WHEN the validator runs
- THEN a violation cites REQ-002-03

## Removed requirements

None.

## Not testable

- The narrative page of the notes example is reviewed by a person; the folder's validation is tested.
