# 004: Checklist

## Gate 1: approved

- [x] spec.md states why it matters before what should be done
- [x] Scope lists at least one explicit non-goal
- [x] Every success criterion is observable
- [x] Capabilities touched are listed in the frontmatter
- [x] The owner of each touched capability has reviewed spec.md
- [x] approved_by and approved_at are filled in

## Gate 2: done

- [ ] Every success criterion in spec.md is met
  - Evidence, 2026-11-08 (first deploy attempt): the workflow failed at the Python setup step because the pip cache looked for requirements.txt and the file is requirements-site.txt; fixed by naming the dependency path in both workflows. Recorded here so the second attempt is the one that counts for T12.
  - Evidence, 2026-11-08 (build fails on a broken link): with the tutorial overview linking to five pages not yet written, `mkdocs build --strict` aborted with six warnings and produced no site. Covers REQ-004-01's broken-link scenario.
- [ ] Every task in tasks.md is ticked
- [ ] Every requirement ID is referenced by at least one test, or listed under "Not testable" with a reason
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
