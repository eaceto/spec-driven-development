# Working in this repository as an agent

This repository uses spec-driven development. Follow these rules.

## What to load

1. `specs/constitution.md`. Always.
2. `specs/INDEX.md`. Always.
3. The one change you are working on, under `specs/changes/`. Read its `spec.md` first.
4. Only the capability specs that change lists in its `capabilities` frontmatter.

Never load every change or every capability. The index exists so you do not have to.

## How work moves

- No design and no code before the change's `spec.md` has `status: approved`.
- Use the skills: `sdd-new` to start a change, `sdd-plan` after approval, `sdd-implement` one task at a time, `sdd-verify` to reach done, `sdd-archive` to close it.
- Work from `tasks.md`. Tick a task only when its requirement IDs are covered by code and tests.
- Every commit that belongs to a change ends with a `Change: NNN` trailer. When the commit covers requirements, add `Requirements: REQ-NNN-xx, ...`. Pull request titles start with the change number.
- Do not change a status by hand. The one exception is Gate 1, where the approver sets `status: approved`, `approved_by` and `approved_at`.
- If a task contradicts a requirement, stop and report. Do not quietly implement something else.
