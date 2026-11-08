# 002: Checklist

## Gate 1: approved

- [x] spec.md states why it matters before what should be done
- [x] Scope lists at least one explicit non-goal
- [x] Every success criterion is observable
- [x] Capabilities touched are listed in the frontmatter
- [x] The owner of each touched capability has reviewed spec.md
- [x] approved_by and approved_at are filled in

## Gate 2: done

- [x] Every success criterion in spec.md is met
  - Evidence, 2026-11-08: init plus new produce a validator-clean layout and change (trial observed, Devin owner-reported); plan refuses a draft (owner-reported); archive produced matching capabilities three times (trial, this repository's 001 and 003); every skill is 42 to 49 lines; the loading rule held for a fresh agent.
- [x] Every task in tasks.md is ticked
- [x] Every requirement ID is referenced by at least one test, or listed under "Not testable" with a reason
  - Evidence, 2026-11-08: structural check over all six skills passed: line limits, section order, frontmatter, vendor-neutral bodies. Covers REQ-002-01, REQ-002-02, REQ-002-03.
  - Evidence, 2026-11-08: sdd-archive dry run on a copy of change 001 marked done. 23 requirements merged into capabilities spec-layout (15) and lifecycle (8), each ID present exactly once with Origin 001, text identical to the change, directory moved to archive, index regenerated from the file system. Covers REQ-002-16.
  - Evidence, 2026-11-08, Claude Code run on a fresh Go sandbox (/tmp/sdd-trial): sdd-init created the layout, constitution, index and AGENTS.md from four questions (REQ-002-07); sdd-new produced change 001 with Why before What (REQ-002-09); sdd-plan produced three requirements with scenarios and tasks citing IDs (REQ-002-11); sdd-implement made one commit per task with Change and Requirements trailers and tests naming the IDs (REQ-002-13); sdd-verify moved it to done (REQ-002-15); sdd-archive created capability greeting with Origin, History, moved the directory and regenerated the index (REQ-002-16, REQ-002-18). One ambiguity found and fixed: which index column carries the link.
  - Evidence, 2026-11-08: the owner ran the negative paths on Claude Code and a full run on Devin CLI on another project and reported all passing. Recorded per requirement in tests/manual/skills-runs.md, which distinguishes observed results from owner-reported ones.
- [x] No open questions remain in design.md
- [x] Constitution principles that applied were checked, and none was violated
  - Tool-agnostic (skill bodies carry no vendor names, enforced by the validator), one structure, teachable in a sentence (five fixed sections), lifecycle enforced not remembered (refusals), small context (loading rule in every skill), dogfooding.
- [x] Documentation that users or operators rely on is updated
  - skills/README.md, the Agents section of docs/method.md, install.sh, AGENTS.md.

## Gate 3: archived

- [ ] Added requirements are present in their capability specs with Origin set
- [ ] Modified requirements are replaced in place with "Changed in" updated
- [ ] Removed requirements are listed under Retired in their capability specs
- [ ] Each touched capability has a History line for this change
- [ ] The change directory has moved to specs/archive/
- [ ] INDEX.md is regenerated
