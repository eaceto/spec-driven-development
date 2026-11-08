# 005: Checklist

## Gate 1: approved

- [x] spec.md states why it matters before what should be done
- [x] Scope lists at least one explicit non-goal
- [x] Every success criterion is observable
- [x] Capabilities touched are listed in the frontmatter
- [x] The owner of each touched capability has reviewed spec.md
- [x] approved_by and approved_at are filled in

## Gate 2: done

- [x] Every success criterion in spec.md is met
  - Evidence, 2026-11-08: a fresh init followed by hand from the revised skill commits six entries under specs/ (the three empty folders carry .gitkeep); every skill is between 42 and 52 lines; validator and tests green; the tutorial note is updated at archive.
- [x] Every task in tasks.md is ticked
- [x] Every requirement ID is referenced by at least one test, or listed under "Not testable" with a reason
  - Quick tier: no requirements were added, modified or removed.
- [x] No open questions remain in design.md
  - Quick tier: no design file.
- [x] Constitution principles that applied were checked, and none was violated
- [x] Documentation that users or operators rely on is updated

## Gate 3: archived

- [x] Added requirements are present in their capability specs with Origin set
- [x] Modified requirements are replaced in place with "Changed in" updated
- [x] Removed requirements are listed under Retired in their capability specs
- [x] Each touched capability has a History line for this change
- [x] The change directory has moved to specs/archive/
- [x] INDEX.md is regenerated
