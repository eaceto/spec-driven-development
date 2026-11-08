# Working in this repository as an agent

This repository practises spec-driven development on itself. Follow these rules.

## What to load

1. `specs/constitution.md`. Always.
2. `specs/INDEX.md`. Always.
3. The one change you are working on, under `specs/changes/`. Read its `spec.md` first.
4. Only the capability specs that change lists in its `capabilities` frontmatter.

Never load every change or every capability. The index exists so you do not have to.

## How work moves

- No code before the change's `spec.md` has status `approved`.
- Work from `tasks.md`. Tick a task only when its requirement IDs are covered by code and tests.
- Every commit that belongs to a change ends with a `Change: NNN` trailer. When the commit covers requirements, add `Requirements: REQ-NNN-xx, ...`. Pull request titles start with the change number.
- Do not mark a change `done` or `archived` by hand. The checklist gates and the archive step do that.
- If a task reveals that a requirement is wrong, stop and edit `requirements.md` in a reviewed change. Do not quietly implement something else.

## Where things are

- Method reference: `docs/method.md`
- Templates: `specs/templates/`
- Skills: `skills/` (planned, see the index)
