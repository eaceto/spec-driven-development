---
name: sdd-verify
description: Verify an in-progress change against Gate 2 in a project that uses spec-driven development. Evaluates every Gate 2 checklist item with evidence, lists requirement IDs that no test references, and moves the change to done only when everything passes. Use when asked to verify, check completeness of, or close a change.
metadata:
  version: 0.1.0
  sdd_version: 0.2.0
---

# sdd-verify

## When to use

The tasks of a change look finished and someone wants to know whether it is done.

## Preconditions

- The change's `spec.md` has `status: in-progress`.
- Load `specs/constitution.md`, `specs/INDEX.md`, the change directory, and only the capability specs listed in the frontmatter. Search the project's tests for requirement IDs.

## Steps

1. Check the status. If it is not `in-progress`, stop and say which skill applies.
2. For each Gate 2 item in `checklist.md`, gather evidence and decide pass or fail.
   - Success criteria: for each criterion in `spec.md`, name the file, test or observation that shows it is met.
   - Tasks: every task in `tasks.md` is ticked.
   - Requirement coverage: for every `REQ-NNN-xx` in `requirements.md`, find a test that mentions it, or an entry under Not testable with a reason. List every ID with neither.
   - Open questions: the section in `design.md` is empty or says none.
   - Constitution: list the principles that applied to this change and state that each was respected, or name the one that was not.
   - Documentation: whatever users or operators rely on reflects the change.
3. Write the report as a table: item, pass or fail, evidence. Below it, the uncovered requirement IDs, if any.
4. If every item passes: tick the Gate 2 items in `checklist.md`, set `status: done` and `updated` to today in `spec.md`, update the row in `specs/INDEX.md`, and commit with `Change: NNN`.
5. If any item fails: change nothing. The report is the result. Say what would make each failed item pass.
6. If the constitution frontmatter has a `validator` key, run that command and include its output in the report.
7. Name the next step: `sdd-archive` when done, otherwise `sdd-implement` or the reviewed edit that is missing.

## Refuse when

- Status is not `in-progress`.
- Asked to set done, or to tick an item, while any item fails. The gate is the point.
- Asked to add a requirement to Not testable so that coverage passes. That entry needs a reason a reviewer would accept, written through a reviewed edit of `requirements.md`.

## Done when

- A report exists with every Gate 2 item, its verdict and its evidence.
- Either every item passed and the change is `done` in the frontmatter and the index, or nothing changed and the report says why.
