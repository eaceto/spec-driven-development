# Manual test log: lifecycle skills (change 002)

Behavioural requirements of the skills are tested by running the skills in real agents. This log is the test artefact for them: one row per requirement, with how it was tested and what was seen. "Observed" means the artefacts were inspected on the maintainer's machine. "Owner-reported" means the owner ran it on another project and reported the result; no artefacts were inspected.

| Requirement | Scenario | Agent | Date | How | Result |
|---|---|---|---|---|---|
| REQ-002-04 | Install into a project | n/a | 2026-11-08 | `install.sh` into a scratch project and `--link` into this repo; both skill locations populated, version written | Observed, pass |
| REQ-002-05 | Loading rule | Claude Code | 2026-11-08 | Fresh agent following AGENTS.md opened only constitution, index, one change and its listed capability | Observed, pass |
| REQ-002-06 | Plan on a draft refuses and names Gate 1 | Claude Code | 2026-11-08 | Negative path run on another project | Owner-reported, pass |
| REQ-002-06 | Archive on in-progress refuses and points to sdd-verify | Claude Code | 2026-11-08 | Negative path run on another project | Owner-reported, pass |
| REQ-002-07 | Init on an empty repository | Claude Code | 2026-11-08 | /tmp/sdd-trial: layout, constitution from four questions, index, AGENTS.md; validator clean | Observed, pass |
| REQ-002-07 | Init on an empty repository | Devin CLI | 2026-11-08 | Full run on another project | Owner-reported, pass |
| REQ-002-08 | Init on an existing codebase: constitution traced to documents, capability map with purpose only | Claude Code | 2026-11-08 | Negative path run on another project | Owner-reported, pass |
| REQ-002-09 | New change from a conversation, Why before What, index row | Claude Code and Devin CLI | 2026-11-08 | /tmp/sdd-trial change 001 observed; Devin run owner-reported | Observed and owner-reported, pass |
| REQ-002-10 | New writes spec.md only | Claude Code | 2026-11-08 | Trial history shows spec and plan in one first commit, so the claim-only commit was not observed separately; owner reports the directory held spec.md alone before approval | Owner-reported, pass |
| REQ-002-11 | Plan produces requirements with scenarios, design, tasks citing ids, checklist, status in-progress | Claude Code and Devin CLI | 2026-11-08 | /tmp/sdd-trial observed: three requirements with scenarios, tasks citing ids | Observed and owner-reported, pass |
| REQ-002-12 | Plan on a quick change implying behaviour change asks to raise the tier | Claude Code | 2026-11-08 | Negative path run on another project | Owner-reported, pass |
| REQ-002-13 | Implement one task, tests naming ids, Change and Requirements trailers, task ticked | Claude Code and Devin CLI | 2026-11-08 | /tmp/sdd-trial observed: one commit per task with both trailers, tests name REQ ids | Observed and owner-reported, pass |
| REQ-002-14 | Implement stops when a requirement is missing, writes no code | Claude Code | 2026-11-08 | Negative path run on another project | Owner-reported, pass |
| REQ-002-15 | Verify evaluates Gate 2 and moves to done only when all pass | Claude Code and Devin CLI | 2026-11-08 | /tmp/sdd-trial observed: Gate 2 commit, status done | Observed and owner-reported, pass |
| REQ-002-16 | Archive merges into capabilities with Origin, creates missing capabilities, moves, regenerates index | Claude Code | 2026-11-08 | /tmp/sdd-trial capability greeting observed; this repository's changes 001 and 003 archived by following the skill; dry run on a copy of 001 | Observed, pass |
| REQ-002-17 | Archive refuses on in-progress and on capability mismatch | Claude Code | 2026-11-08 | Negative path run on another project; mismatch refusal exercised by the validator rule status-archived in tests/test_validate.py | Owner-reported, pass |
| REQ-002-18 | Index rows updated by new, plan, verify, archive | Claude Code | 2026-11-08 | /tmp/sdd-trial index shows the archived state and the greeting capability | Observed, pass |
| REQ-002-19 | Skills behave the same with and without a validator | Claude Code | 2026-11-08 | Trial ran without a validator and produced files the validator later accepts with zero violations; this repository runs with the key set | Observed, pass |

Open observations from the runs, each a candidate improvement rather than a failure:

- The trial's first commit held spec and plan together. The claim rule asks for spec.md alone to be merged first; the skills say so, but an agent that commits only at the end hides it. A later change could make `sdd-new` commit the claim itself.
- The trial's index linked the capability id rather than the title; fixed in the skills on 2026-11-08.
- `sdd-archive` describes the merge for changes with a `requirements.md`. A quick change has none; its listed capabilities should still receive a History line. Done by hand for change 005 on 2026-11-08; a later quick change should say so in the skill.
