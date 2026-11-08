---
name: sdd-implement
description: Implement the next task of an in-progress change in a project that uses spec-driven development. Takes the first unticked task, implements it with tests that reference its requirement IDs, commits with Change and Requirements trailers, ticks the task and stops. Writes nothing when a task contradicts or lacks a requirement. Use when asked to implement, build or continue work on a change.
metadata:
  version: 0.1.0
  sdd_version: 0.1.0
---

# sdd-implement

## When to use

A change is planned and has unticked tasks.

## Preconditions

- The change's `spec.md` has `status: in-progress`, or `status: approved` with every file its tier requires already present, in which case set it to in-progress first and update the index row.
- Load `specs/constitution.md`, `specs/INDEX.md`, the change directory including `guardrails.md` if present, and only the capability specs listed in the frontmatter.

## Steps

1. Check the status. Draft: stop, Gate 1. Approved without the tier's files: stop, `sdd-plan`. Done or archived: stop, the change is closed.
2. Take the first unticked task in `tasks.md`. Read the requirement IDs it cites and their scenarios in `requirements.md`, and the parts of `design.md` that bear on it.
3. Before writing anything, check the task against the requirements, the guardrails and the constitution. If doing it correctly needs behaviour no requirement describes, or contradicts one, stop. Write no code. Report the task, the requirement IDs involved and the gap. Leave `requirements.md` unchanged; a requirement changes only through a reviewed edit.
4. Implement the task. Write or extend tests so that every cited requirement ID appears in a test name or in a comment beside the test that checks its scenario. Run the tests.
5. Commit. Subject line in the project's usual style. End the message with `Change: NNN` and, on the next line, `Requirements:` followed by the IDs this commit covers, comma separated. A setup task carries `Change:` only.
6. Tick the task in `tasks.md` and set `updated` in `spec.md` to today. Commit that too, with `Change: NNN`.
7. Stop. Report what was done, which IDs are now covered, and the next unticked task. Continue to the next task only if asked.
8. If the constitution frontmatter has a `validator` key, run that command before reporting and include its output.

## Refuse when

- The status does not allow it, as in step 1.
- The task cites no requirement ID and is not marked setup. Report the missing requirement instead of guessing.
- `guardrails.md` says to stop and ask in this situation.
- The work touches a capability the change does not list.
- Asked to tick a task whose tests do not exist or do not pass.

## Done when

- Exactly one more task is ticked than before, unless asked to continue.
- Its commit carries the `Change:` trailer and, for a non-setup task, the `Requirements:` trailer with the IDs it covers.
- Each of those IDs appears in a test.
