---
id: "008"
title: Explicit exemptions and refusal wording
status: done
tier: standard
owner: maintainers
capabilities: [validator, skills]
ticket:
docs:
approved_by: Ezequiel Aceto
approved_at: 2026-11-08
created: 2026-11-08
updated: 2026-11-08
---

# 008: Explicit exemptions and refusal wording

## Why it matters

Closing change 007 showed that any requirement id mentioned anywhere under Not testable is treated as exempt from test coverage, reasons unexamined. A sentence that merely refers to an id silently removes it from the gate. The gate's whole value is that it cannot be satisfied by accident. Separately, the refusal-path runs found three places where a skill's words leave an agent to decide: whether raising a quick change's tier needs re-approval, whether a cited id that does not exist counts as "no id", and whether an empty leftover `specs/` directory blocks initialisation.

## What should be done

An exemption is one bullet under Not testable that starts with the requirement id and gives a reason; only those ids are exempt, and any other id mentioned in the section is a violation that says how to write the exemption. The three skills gain one sentence each: `sdd-plan` says the approver confirms a raised tier; `sdd-implement` refuses a task citing an id that does not exist; `sdd-init` refuses only when `specs/` exists and is not empty.

## Scope

### In

- The validator's Not testable parsing and a rule for malformed exemptions, with tests
- Amendment of REQ-003-13's wording on exemptions
- One sentence each in `sdd-plan`, `sdd-implement`, `sdd-init`

### Out

- Judging whether an exemption's reason is good. That stays with the reviewer.
- Any other change to the gates.

## Success criteria

- A requirement id mentioned in prose under Not testable, not on its own bullet, no longer counts as exempt and produces a violation naming the bullet form.
- Every archived change in this repository still passes the validator after the change.
- The three skills stay under 150 lines and the suite is green.
