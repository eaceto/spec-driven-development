---
id: "005"
title: Skill clarifications from the first tutorial run
status: archived
tier: quick
owner: maintainers
capabilities: [skills]
ticket:
docs:
approved_by: Ezequiel Aceto
approved_at: 2026-11-08
created: 2026-11-08
updated: 2026-11-08
---

# 005: Skill clarifications from the first tutorial run

## Why it matters

The first fresh run of `sdd-init` for the tutorial produced a correct project and twelve observations about the skill text. None changes what the skills do. Each is a place where an agent had to decide something the skill should have said, and where the next agent may decide differently. Left alone, these become drift between projects: one with `.gitkeep` files, one without; one constitution with guidance comments, one without.

## What should be done

Clarify the skill texts and one template without changing any requirement:

- `sdd-init` asks its questions before creating files, leaves a `.gitkeep` in `capabilities/`, `changes/` and `archive/` so the folders survive a commit, says that agent configuration and the installed skills do not count as source code when picking the mode, says what to write under Principles and Definitions when a team has none yet, tells the agent to read `sdd_version` from the SKILL.md file when its tool hides frontmatter, marks the Capabilities table step as existing-project only, and states the one-page limit as 80 lines.
- `sdd-init`, `sdd-new` and `sdd-plan` say to remove the templates' guidance comments as sections are filled.
- `sdd-new` says that when the answers name a person rather than a team, `owner` is the constitution's owner; that the tier is proposed by the skill and confirmed in one line rather than asked open; that the constraints section may be omitted; that `capabilities` uses the `[a, b]` form; and that the skill does not commit, so its report tells the person to commit `spec.md` alone as the claim.
- The constitution template's first amendment row uses `none` in the Change column, since the initial constitution comes from no change.

## Scope

### In

- Text edits to `skills/sdd-init/SKILL.md`, `skills/sdd-new/SKILL.md`, `skills/sdd-plan/SKILL.md`, informed by the first two fresh tutorial runs
- The amendment row in `specs/templates/constitution.md`

### Out

- Any change to what a skill produces, refuses or checks. If one is needed, it is a standard change against the `skills` capability.
- The validator. It already ignores hidden entries and does not require numbered principles.

## Success criteria

- A fresh `sdd-init` run commits six entries under `specs/`, not three.
- No skill exceeds 150 lines after the edits, and the validator and tests stay green.
- The tutorial note about this change can be removed from step 2 once it is archived.
