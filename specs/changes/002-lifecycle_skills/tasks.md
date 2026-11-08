# 002: Tasks

## Setup

- [x] T01 Create `skills/` with a README stating the format, the section order and the line limit [REQ-002-01, REQ-002-02, REQ-002-03]

## Implementation

- [x] T02 Write `skills/sdd-init/SKILL.md` covering new and existing projects [REQ-002-07, REQ-002-08]
- [x] T03 Write `skills/sdd-new/SKILL.md` [REQ-002-09, REQ-002-10, REQ-002-18]
- [x] T04 Write `skills/sdd-plan/SKILL.md` including quick-tier handling [REQ-002-11, REQ-002-12, REQ-002-18]
- [ ] T05 Write `skills/sdd-implement/SKILL.md` [REQ-002-13, REQ-002-14]
- [ ] T06 Write `skills/sdd-verify/SKILL.md` [REQ-002-15, REQ-002-18]
- [ ] T07 Write `skills/sdd-archive/SKILL.md` [REQ-002-16, REQ-002-17, REQ-002-18]
- [ ] T08 Add status preconditions, the loading rule and the validator hook to every skill [REQ-002-05, REQ-002-06, REQ-002-19]
- [ ] T09 Write `install.sh` and the install section in `docs/method.md` [REQ-002-04]
- [ ] T10 Install the skills into this repository and update `AGENTS.md` to name them [REQ-002-04]

## Verification

- [ ] T11 Run every skill on Devin CLI against a scratch project and record evidence in checklist.md [REQ-002-06 through REQ-002-18]
- [ ] T12 Run every skill on Claude Code against a scratch project and record evidence in checklist.md [REQ-002-06 through REQ-002-18]
- [ ] T13 Dry-run `sdd-archive` against a copy of change 001 and compare the produced capabilities to its requirements [REQ-002-16]
- [ ] T14 Check line limits, section order and vendor-neutrality of every skill body [REQ-002-01, REQ-002-02, REQ-002-03]
