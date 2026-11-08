# 001: Checklist

## Gate 1: approved

- [x] spec.md states why it matters before what should be done
- [x] Scope lists at least one explicit non-goal
- [x] Every success criterion is observable
- [x] Capabilities touched are listed in the frontmatter
- [x] The owner of each touched capability has reviewed spec.md
- [x] approved_by and approved_at are filled in

## Gate 2: done

- [x] Every success criterion in spec.md is met
  - Evidence, 2026-11-08 (criterion 1, a newcomer creates a correct change in under fifteen minutes): the owner accepted the Claude Code trial in a fresh Go sandbox as evidence. There, a change was created from the templates through the skills and the validator reports it clean. Caveat recorded by the owner's decision: the method document alone was not tested on a person who had never seen the repository.
  - Evidence, 2026-11-08 (criterion 2, every rule backed by a requirement): audit of docs/method.md against requirements.md. Every rule maps to a requirement: folders 01/11/21, tiers 04/05, spec order 06, states and gates 16/17/20/21, requirements and ids 08/09/10/12, numbering and claim 02/03/18, ownership 17, commits 23, links 12, constitution 13, identity 15, index 14, loading rule 22. The only statements without one are the two documented variants (ticket numbering, domain grouping), now marked in the document as not yet accepted by the validator and left for a later change.
  - Evidence, 2026-11-08 (criterion 4, agent loads only what the rule allows): a fresh agent given only AGENTS.md and asked to prepare change 002 opened AGENTS.md, specs/constitution.md, specs/INDEX.md, the five files of specs/changes/002-lifecycle_skills/ and looked for the one listed capability. It opened no other change and ran nothing. It reported five ambiguities in the loading rule, which are now fixed in the AGENTS.md template and this repository's copy.
  - Evidence, 2026-11-08 (criterion 3, this repository follows the layout): `python3 specs/validate.py` reports 0 violations with 21 rules.
- [x] Every task in tasks.md is ticked
- [x] Every requirement ID is referenced by at least one test, or listed under "Not testable" with a reason
  - Evidence, 2026-11-08: tests/test_validate.py names REQ-001-01 through REQ-001-23; the validator's status-done rule confirms coverage when this change is marked done. REQ-001-06's readability scenario is listed under Not testable.
- [x] No open questions remain in design.md
- [x] Constitution principles that applied were checked, and none was violated
  - All eight applied. The bootstrap exception to REQ-001-19, authoring design and tasks before approval, is recorded in design.md and is the only departure.
- [x] Documentation that users or operators rely on is updated
  - README.md, docs/method.md, AGENTS.md and the templates are the documentation this change delivers.

## Gate 3: archived

- [ ] Added requirements are present in their capability specs with Origin set
- [ ] Modified requirements are replaced in place with "Changed in" updated
- [ ] Removed requirements are listed under Retired in their capability specs
- [ ] Each touched capability has a History line for this change
- [ ] The change directory has moved to specs/archive/
- [ ] INDEX.md is regenerated
