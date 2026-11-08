# 003: Tasks

## Setup

- [x] T01 Create `specs/validate.py` with the command line, frontmatter parser, tree model, rule registry, report and exit codes, plus `--rules` [REQ-003-01, REQ-003-02, REQ-003-03, REQ-003-04]

## Implementation

- [x] T02 Layout, naming, numbering and tier rules, implementing the amended REQ-001-01 [REQ-003-05, REQ-003-06, REQ-003-07, REQ-001-01]
- [x] T03 Spec order and frontmatter rules [REQ-003-08, REQ-003-09]
- [x] T04 Requirement grammar and grouping rules [REQ-003-10, REQ-003-11]
- [x] T05 Capability spec rules [REQ-003-12]
- [x] T06 Status consistency rules, including coverage search and backward moves against git [REQ-003-13]
- [x] T07 Index rule [REQ-003-14]
- [x] T08 Constitution and entry file rules [REQ-003-15]
- [x] T09 Commit trailer rule [REQ-003-16]
- [x] T10 Skills rules [REQ-003-17]
- [x] T11 `tests/test_validate.py` with template-built fixtures, one passing and one failing case per rule [REQ-003-19]
- [x] T12 `install.sh` copies the validator and sets the `validator` key; set the key in this repository's constitution; document in `docs/method.md` and the skills README [REQ-003-18]
- [ ] T13 Run on this repository and on the trial sandbox; fix genuine violations in the specs or the templates, never by weakening a rule without a reviewed edit [REQ-003-20]

## Verification

- [ ] T14 Every REQ-003 id and every REQ-001 id named by a rule appears in `tests/test_validate.py`; the suite passes [all]
- [ ] T15 `--rules` output lists every structural requirement of change 001 [REQ-003-04]
- [ ] T16 Documentation: method document names the validator, its command, exit codes and the `validator` key [all]
