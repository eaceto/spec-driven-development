# 007: Checklist

## Gate 1: approved

- [x] spec.md states why it matters before what should be done
- [x] Scope lists at least one explicit non-goal
- [x] Every success criterion is observable
- [x] Capabilities touched are listed in the frontmatter
- [x] The owner of each touched capability has reviewed spec.md
- [x] approved_by and approved_at are filled in

## Gate 2: done

- [x] Every success criterion in spec.md is met
  - Evidence, 2026-11-08: examples/notes-python validates clean and is linked from tutorial step 6; no skill carries metadata.version and the validator, hook and 50 tests pass; a test proves an id only in a comment is not coverage; a block list yields a violation naming `[a, b]`; ticket numbering passes under `numbering: ticket` and fails under sequential in the suite; five refusal paths observed in fresh runs, one with a caveat on skill version.
- [x] Every task in tasks.md is ticked
- [x] Every requirement ID is referenced by at least one test, or listed under "Not testable" with a reason
- [x] No open questions remain in design.md
- [x] Constitution principles that applied were checked, and none was violated
- [x] Documentation that users or operators rely on is updated

## Gate 3: archived

- [x] Added requirements are present in their capability specs with Origin set
- [x] Modified requirements are replaced in place with "Changed in" updated
- [x] Removed requirements are listed under Retired in their capability specs
- [x] Each touched capability has a History line for this change
- [x] The change directory has moved to specs/archive/
- [x] INDEX.md is regenerated
