# 002: Checklist

## Gate 1: approved

- [x] spec.md states why it matters before what should be done
- [x] Scope lists at least one explicit non-goal
- [x] Every success criterion is observable
- [x] Capabilities touched are listed in the frontmatter
- [x] The owner of each touched capability has reviewed spec.md
- [x] approved_by and approved_at are filled in

## Gate 2: done

- [ ] Every success criterion in spec.md is met
- [ ] Every task in tasks.md is ticked
- [ ] Every requirement ID is referenced by at least one test, or listed under "Not testable" with a reason
  - Evidence, 2026-11-08: structural check over all six skills passed: line limits, section order, frontmatter, vendor-neutral bodies. Covers REQ-002-01, REQ-002-02, REQ-002-03.
  - Evidence, 2026-11-08: sdd-archive dry run on a copy of change 001 marked done. 23 requirements merged into capabilities spec-layout (15) and lifecycle (8), each ID present exactly once with Origin 001, text identical to the change, directory moved to archive, index regenerated from the file system. Covers REQ-002-16.
  - Pending: recorded runs of each skill on Devin CLI (T11) and Claude Code (T12) for REQ-002-06 through REQ-002-18.
- [ ] No open questions remain in design.md
- [ ] Constitution principles that applied were checked, and none was violated
- [ ] Documentation that users or operators rely on is updated

## Gate 3: archived

- [ ] Added requirements are present in their capability specs with Origin set
- [ ] Modified requirements are replaced in place with "Changed in" updated
- [ ] Removed requirements are listed under Retired in their capability specs
- [ ] Each touched capability has a History line for this change
- [ ] The change directory has moved to specs/archive/
- [ ] INDEX.md is regenerated
