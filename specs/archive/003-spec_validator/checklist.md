# 003: Checklist

## Gate 1: approved

- [x] spec.md states why it matters before what should be done
- [x] Scope lists at least one explicit non-goal
- [x] Every success criterion is observable
- [x] Capabilities touched are listed in the frontmatter
- [x] The owner of each touched capability has reviewed spec.md
- [x] approved_by and approved_at are filled in

## Gate 2: done

- [x] Every success criterion in spec.md is met
  - Evidence, 2026-11-08: `python3 specs/validate.py` reports 0 violations on this repository and on the trial sandbox; `--rules` names REQ-001-01 to REQ-001-23 except 12 and 15, which have direct tests; each of the seven listed faults has a failing test case in tests/test_validate.py; the 3.9 promise is checked statically (parser feature_version 3.9 plus a scan for newer APIs) because no 3.9 interpreter was available here.
- [x] Every task in tasks.md is ticked
- [x] Every requirement ID is referenced by at least one test, or listed under "Not testable" with a reason
  - Evidence, 2026-11-08: 31 tests pass; the suite names every REQ-003 id and REQ-001-01, the one modified requirement.
- [x] No open questions remain in design.md
- [x] Constitution principles that applied were checked, and none was violated
  - Purpose before mechanism, one structure, teachable in a sentence (every rule has a one-line description), tool-agnostic (standard library only), lifecycle enforced not remembered (this change is the enforcement), small context (one file), dogfooding.
- [x] Documentation that users or operators rely on is updated
  - docs/method.md gained "The validator"; skills/README.md and install.sh describe the key it sets.

## Gate 3: archived

- [x] Added requirements are present in their capability specs with Origin set
- [x] Modified requirements are replaced in place with "Changed in" updated
- [x] Removed requirements are listed under Retired in their capability specs
- [x] Each touched capability has a History line for this change
- [x] The change directory has moved to specs/archive/
- [x] INDEX.md is regenerated
