# 008: Requirements

Notation: one SHALL statement per requirement with at least one scenario. IDs are REQ-008-xx and are never reused.

## Capability: validator

### REQ-008-01: Exemptions are explicit
The validator SHALL treat a requirement id as exempt from coverage only when it appears under Not testable as the start of its own bullet followed by a reason, and SHALL report a violation for any other requirement id mentioned in that section, naming the bullet form.

#### Scenario: Id in prose
- GIVEN a Not testable section reading "REQ-014-03 is hard to test"
- WHEN the validator runs
- THEN a violation names REQ-014-03 and the form `- REQ-014-03: reason`, and REQ-014-03 is not exempt

#### Scenario: Proper bullet
- GIVEN a Not testable section containing `- REQ-014-03: needs a person to judge readability`
- WHEN the validator runs
- THEN REQ-014-03 is exempt and no violation is reported for it

## Capability: skills

### REQ-008-02: Refusal wording from the runs
The skills SHALL state that raising a quick change's tier is confirmed by the approver before planning continues, that `sdd-implement` refuses a task citing a requirement id that does not exist, and that `sdd-init` refuses only when `specs/` exists and is not empty.

#### Scenario: Reading the skills
- GIVEN the three skill files
- WHEN a reader searches for those three situations
- THEN each has one sentence that decides it

## Modified requirements

### REQ-003-13: Status consistency rule
Changed in: 007, 008

The validator SHALL report a violation when a draft change contains any file other than `spec.md`; when a done change has an unticked task, an unticked Gate 2 item, or a requirement id that appears in no test file outside comment lines and is not exempted by its own bullet with a reason under Not testable; when an archived change is under `specs/changes/`, a change under `specs/archive/` is not archived, or an archived change has an added requirement absent from its capability spec, a modified one without `Changed in`, a removed one not under Retired, or an unticked Gate 3 item; and, when the project is a git repository, when a status has moved backwards relative to the committed version.

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

## Removed requirements

None.

## Not testable

None.
