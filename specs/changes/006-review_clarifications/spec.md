---
id: "006"
title: Clarifications from the 0.2.0 review
status: in-progress
tier: quick
owner: maintainers
capabilities: [skills, website, lifecycle]
ticket:
docs:
approved_by: Ezequiel Aceto
approved_at: 2026-11-08
created: 2026-11-08
updated: 2026-11-08
---

# 006: Clarifications from the 0.2.0 review

## Why it matters

A review of the repository at 0.2.0 found places where the text leaves a reader or an agent to guess: the Go example carries templates older than the canonical ones without saying so; the method does not say that an id in a test file is a floor, not a proof; `sdd-archive` has no words for a quick change; `sdd-implement` does not say whether a behaviour recorded only in the design counts as described; and the method is silent on squash merges. None of these changes what anything does. Each is a sentence that stops the next person deciding differently.

## What should be done

- The Go example's page says its templates are a snapshot from the day it was produced and links to the canonical folder.
- The method's Gate 2 explanation says that a requirement id in a test file is the floor the validator can check, and judgement is the rest; the same sentence appears on the site's validator page.
- The method says that a squash merge keeps the `Change:` trailer and lists every `Requirements:` id the squashed commits delivered.
- `sdd-archive` says a change without `requirements.md` merges nothing and its listed capabilities receive a History line.
- `sdd-implement` says a behaviour recorded as a decision in `design.md` counts as described, and only behaviour found in neither requirements nor design stops the task.

## Scope

### In

- `docs/examples/greenfield-go.md`, `docs/method.md`, `docs/reference/validator.md`
- `skills/sdd-archive/SKILL.md`, `skills/sdd-implement/SKILL.md`

### Out

- Any change to what a skill produces, refuses or checks, and any change to a requirement. Those are change 007.
- The Devin tabs on the tutorial, kept for one release.

## Success criteria

- Every skill stays under 150 lines; validator, tests and strict build stay green.
- Each of the five sentences can be found by a reader on the page where the question would arise.
