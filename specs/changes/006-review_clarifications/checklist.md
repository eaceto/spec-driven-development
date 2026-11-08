# 006: Checklist

## Gate 1: approved

- [x] spec.md states why it matters before what should be done
- [x] Scope lists at least one explicit non-goal
- [x] Every success criterion is observable
- [x] Capabilities touched are listed in the frontmatter
- [x] The owner of each touched capability has reviewed spec.md
- [x] approved_by and approved_at are filled in

## Gate 2: done

- [x] Every success criterion in spec.md is met
  - Evidence, 2026-11-08: skills 43 to 52 lines; validator, 47 tests and strict build green; each sentence sits on the page where its question arises.
- [x] Every task in tasks.md is ticked
- [x] Every requirement ID is referenced by at least one test, or listed under "Not testable" with a reason
  - Quick tier: no requirements changed.
- [x] No open questions remain in design.md
- [x] Constitution principles that applied were checked, and none was violated
- [x] Documentation that users or operators rely on is updated

## Gate 3: archived

- [ ] Added requirements are present in their capability specs with Origin set
- [ ] Modified requirements are replaced in place with "Changed in" updated
- [ ] Removed requirements are listed under Retired in their capability specs
- [ ] Each touched capability has a History line for this change
- [ ] The change directory has moved to specs/archive/
- [ ] INDEX.md is regenerated
