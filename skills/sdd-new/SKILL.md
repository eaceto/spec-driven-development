---
name: sdd-new
description: Start a new change in a project that uses spec-driven development. Turns a description of a problem or feature into a numbered change directory containing only spec.md, written purpose first after at most five clarifying questions, and adds the change to the index as a draft. Use when asked to create, start or propose a spec, change or feature.
metadata:
  version: 0.1.1
  sdd_version: 0.2.0
---

# sdd-new

## When to use

Someone describes a problem, a feature or a piece of work and wants it captured as a change. Nothing exists for it yet.

## Preconditions

- `specs/` exists. If not, stop and point to `sdd-init`.
- Load `specs/constitution.md`, `specs/INDEX.md` and `specs/templates/change/spec.md`. Load nothing else.

## Steps

1. Read the description. Ask at most five clarifying questions, and only those it leaves open: who feels the problem and what it costs them; what will be observably true when the work is done; what a reader might assume is included that is not; which capabilities are touched, using the Capabilities table of the index; which tier fits. Skip every question already answered.
2. Choose the tier and state it in one line for the person to confirm. Quick is for work that changes no behaviour, so no requirement will be added, modified or removed. Otherwise standard. Full only when the change needs guardrails of its own.
3. Assign the number. With `numbering: sequential` in the constitution, take the highest three-digit prefix across `specs/changes/` and `specs/archive/` and add one. With `numbering: ticket`, use the ticket key. Name the directory `NNN-name_of_change`: the number, a dash, then two to five lowercase words joined by underscores.
4. Create the directory with `spec.md` only, from the template, removing the template's guidance comments as you fill each section. Fill the frontmatter: `id` quoted, `title`, `status: draft`, `tier`, `owner` as the team named in the answers or, when the answers name a person or nobody, the constitution's owner, `capabilities` in the form `[a, b]`, `ticket` and `docs` if given, `approved_by` and `approved_at` empty, `created` and `updated` today.
5. Write the sections in this order and no other: Why it matters, What should be done, Scope with In and Out, Success criteria, and Constraints specific to this change only when there are any. Why holds the problem, who has it and the cost of doing nothing, and no solution. What holds the outcome in plain language. Out lists at least one non-goal. Every success criterion is observable.
6. Add a row to Active changes in `specs/INDEX.md`: number, title linked to the spec, draft, tier, owner, ticket, capabilities, today.
7. If the constitution frontmatter has a `validator` key, run that command and include its output. Otherwise check by reading: the directory holds exactly `spec.md`, the number is unique, the sections are in order, Out is not empty.
8. Report the path and what happens next. This skill does not commit: tell the person to commit `spec.md` and the index row alone, with a `Change: NNN` trailer, so the number is claimed. Then Gate 1: the owner of each listed capability reviews `spec.md`, and the approver sets `status: approved`, `approved_by` and `approved_at`. Then `sdd-plan`.

## Refuse when

- Asked to also write requirements, design or tasks now. Those come from `sdd-plan` after Gate 1. The first thing merged for a change is its `spec.md` alone, so the number is claimed before anyone branches.
- The description has no purpose you can state. Ask for it rather than inventing one.
- A capability is named that is not in the index. Ask whether it is new. If so, list it anyway and say it will be created when the change is archived.

## Done when

- `specs/changes/NNN-name_of_change/` exists and contains exactly `spec.md`.
- The frontmatter has every field, with `status: draft`.
- Why precedes What, Out has at least one entry, success criteria are observable.
- The index shows the change as draft.
