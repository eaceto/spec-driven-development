# 004: Checklist

## Gate 1: approved

- [x] spec.md states why it matters before what should be done
- [x] Scope lists at least one explicit non-goal
- [x] Every success criterion is observable
- [x] Capabilities touched are listed in the frontmatter
- [x] The owner of each touched capability has reviewed spec.md
- [x] approved_by and approved_at are filled in

## Gate 2: done

- [x] Every success criterion in spec.md is met
  - Evidence, 2026-11-08 (first deploy attempt): the workflow failed at the Python setup step because the pip cache looked for requirements.txt and the file is requirements-site.txt; fixed by naming the dependency path in both workflows. Recorded here so the second attempt is the one that counts for T12.
  - Evidence, 2026-11-08 (first deploy succeeds): after the cache-path fix the Deploy site workflow published https://eaceto.github.io/spec-driven-development/ from main. Fetched the live page: title "Spec-driven development", the one sentence on the first screen, navigation with "Your first change", "Skills" and "Validator rules", and the state diagram rendered with its gates. Covers REQ-004-01's clean-push scenario and T12.
  - Evidence, 2026-11-08 (tutorial transcripts are real): six fresh Claude Code runs in a scratch project carried a notes command-line tool from an empty folder to an archived capability; each step page quotes that run with agent and date. The finished project passes the validator with zero violations. Covers REQ-004-04 for the Claude Code tabs; the Devin tabs await the owner's transcripts (T09).
  - Evidence, 2026-11-08 (checks fail a faulty pull request): the pull request from branch checks-smoke-test, holding one misnamed change directory, failed the Checks workflow at the validator step with `specs/changes/12-Bad-Name: change-dirname (REQ-001-02)` and exit code 1. Closed unmerged. Covers REQ-004-13 and T13.
  - Evidence, 2026-11-08 (a newcomer follows the site alone): the owner reports that one person who had not used the method reached an archived first change following the site alone, within the fifteen minutes. Owner-reported; time and sticking points were not recorded beyond "OK". Covers the second success criterion and T14.
  - Evidence, 2026-11-08 (build fails on a broken link): with the tutorial overview linking to five pages not yet written, `mkdocs build --strict` aborted with six warnings and produced no site. Covers REQ-004-01's broken-link scenario.
- [x] Every task in tasks.md is ticked
- [x] Every requirement ID is referenced by at least one test, or listed under "Not testable" with a reason
  - tests/test_site.py names REQ-004-01 to 13; REQ-004-01 clean push and REQ-004-13 are verified by the recorded workflow runs and listed under Not testable for the local suite.
- [x] No open questions remain in design.md
- [x] Constitution principles that applied were checked, and none was violated
  - One copy of every rule (generated pages), tool-agnostic (agents labelled, nothing vendor-specific in the method), small context, dogfooding. REQ-004-04 was amended by a reviewed edit on 2026-11-08 because no Devin session was available for transcripts; the owner approved the edit.
- [x] Documentation that users or operators rely on is updated
  - The site is the documentation; README and the method document link to it.

## Gate 3: archived

- [ ] Added requirements are present in their capability specs with Origin set
- [ ] Modified requirements are replaced in place with "Changed in" updated
- [ ] Removed requirements are listed under Retired in their capability specs
- [ ] Each touched capability has a History line for this change
- [ ] The change directory has moved to specs/archive/
- [ ] INDEX.md is regenerated
