# 004: Tasks

## Setup

- [x] T01 `mkdocs.yml`, `requirements-site.txt`, a home page skeleton; local strict build in a scratch virtual environment [REQ-004-02, REQ-004-11, REQ-004-12]

## Implementation

- [x] T02 Build hook generating the skills, templates and validator pages [REQ-004-06]
- [x] T03 Deploy workflow and checks workflow [REQ-004-01, REQ-004-13]
- [x] T04 `examples/greenfield-go` from the trial, validator-clean, and its narrative page [REQ-004-08]
- [x] T05 Home page and the what-and-why page [REQ-004-03, REQ-004-11]
- [x] T06 Agents page [REQ-004-07]
- [x] T07 Entry pages for developers and team leads [REQ-004-05]
- [ ] T08 Tutorial, six steps, with Claude Code transcripts from fresh runs [REQ-004-04]
- [ ] T09 Devin CLI transcripts added to the tutorial tabs, from the owner's runs [REQ-004-04]
- [x] T10 `tests/test_site.py`: configuration, hook output, word limits, UK spelling [REQ-004-06, REQ-004-09, REQ-004-10, REQ-004-11, REQ-004-12]
- [ ] T11 README links to the site; method document mentions where the site lives [REQ-004-03]

## Verification

- [ ] T12 First deploy on main succeeds and the address serves the home page; record the run in checklist.md [REQ-004-01]
- [ ] T13 A pull request with a deliberate fault fails the checks workflow; record the run [REQ-004-13]
- [ ] T14 One person who has not used the method follows the site alone to an archived first change; record time and sticking points [success criteria]
