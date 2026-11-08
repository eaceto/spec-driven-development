---
name: sdd-plan
description: Plan an approved change in a project that uses spec-driven development. Writes requirements grouped by capability with stable IDs, a design with recorded decisions, tasks citing requirement IDs and the checklist, then moves the change to in-progress. Refuses on a draft. Use when asked to plan, write requirements for, design or break down an approved change.
metadata:
  sdd_version: 0.2.0
---

# sdd-plan

## When to use

A change has passed Gate 1 and needs its requirements, design and tasks before any code is written.

## Preconditions

- The change's `spec.md` has `status: approved`.
- Load `specs/constitution.md`, `specs/INDEX.md`, the change directory, `specs/templates/change/`, and only the capability specs listed in the change's `capabilities` frontmatter.

## Steps

1. Check the status. If it is not `approved`, stop and say what applies: draft needs Gate 1; in-progress is already planned; done and archived are closed.
2. Check the tier. For `quick`, read `spec.md` once more. If what it describes adds, modifies or removes any behaviour, stop and ask the author to raise the tier to standard; the tier is part of what was approved, so the approver confirms it before planning continues. Otherwise write only `tasks.md` and `checklist.md`, skipping to step 6.
3. Write `requirements.md` from the template, removing the template's guidance comments as you fill it; do the same for every file below. One `## Capability: <id>` section per capability in the frontmatter. Derive requirements from What should be done and Success criteria. Each requirement has a heading `### REQ-NNN-xx: Title`, numbered from 01 across the whole file, one SHALL statement shaped as "When <trigger>, the <subject> SHALL <behaviour>" or "The <subject> SHALL <behaviour>", an optional `Ref:` line, and at least one scenario with GIVEN, WHEN and THEN bullets. Compare with the capability's existing requirements: one this change rewrites goes under Modified requirements with its original ID and `Changed in: NNN`; one it retires goes under Removed requirements with the reason. If a requirement belongs to a capability the frontmatter does not list, stop and report it. The author adds it to `spec.md`, and that capability's owner reviews.
4. Write `design.md` from the template: the approach, at least one decision with alternatives and why, the interfaces and data this change touches, risks, and open questions. Open questions must be closed before Gate 2, so resolve them now where you can.
5. For `full` tier, write `guardrails.md` from the template using the constraints in `spec.md`.
6. Write `tasks.md` from the template. Order the tasks. Every task cites the requirement IDs it satisfies in brackets; a task with none is marked `[setup]`. End with verification tasks: tests covering every ID, and documentation.
7. Write `checklist.md` from the template. Tick the Gate 1 items the frontmatter proves: capabilities listed, `approved_by` and `approved_at` present. Leave the rest to a person.
8. Set `status: in-progress` and `updated` to today in `spec.md`. Update the change's row in `specs/INDEX.md`.
9. If the constitution frontmatter has a `validator` key, run that command and include its output. Otherwise check by reading: the files match the tier, every requirement has a scenario, every task cites an ID or is setup, every capability section is in the frontmatter.
10. Report the counts of requirements and tasks, and name the next step: `sdd-implement`.

## Refuse when

- Status is not `approved`. For a draft, name Gate 1.
- The tier is `quick` and the spec implies a behaviour change.
- A requirement needs a capability that the approved `spec.md` does not list.
- You would change `spec.md` beyond status and date. Purpose and scope were approved; changing them restarts Gate 1.

## Done when

- The directory holds exactly the files the tier requires.
- Every requirement has an ID, a SHALL statement and a scenario, under a capability from the frontmatter.
- Every task cites a requirement ID or is setup.
- `status: in-progress` in the frontmatter and the index.
