---
name: sdd-archive
description: Archive a done change in a project that uses spec-driven development. Merges its requirements into the living capability specs, creating capabilities that do not exist yet, moves the change directory to the archive, sets the status to archived and regenerates the index. Refuses unless the change is done and its capabilities are consistent. Use when asked to archive, close out or merge a finished change.
metadata:
  version: 0.1.0
  sdd_version: 0.2.0
---

# sdd-archive

## When to use

A change has passed Gate 2 and its requirements must become part of how the system is described today.

## Preconditions

- The change's `spec.md` has `status: done`.
- Load `specs/constitution.md`, `specs/INDEX.md`, the change directory, `specs/templates/capability.md`, and the capability specs listed in the frontmatter.

## Steps

1. Check consistency before writing anything. Status is `done`. Every `## Capability:` heading in `requirements.md` names a capability in the frontmatter. Every ID under Modified requirements and Removed requirements exists in its capability spec. If any check fails, stop and report exactly what is inconsistent.
2. A quick change has no `requirements.md`: merge nothing, give each capability in its frontmatter a History line, and go to step 3. Otherwise, for each `## Capability: <id>` section of `requirements.md`:
   - If `specs/capabilities/<id>/spec.md` does not exist, create it from the template with `id`, a title from the id, `owner` from the change, and a Purpose of one or two sentences taken from the change's Why and What. Note in the report that the owner should refine the Purpose.
   - Append each added requirement to the Requirements section, keeping its heading, SHALL statement, `Ref:` line and scenarios, with the line `Origin: NNN` under the heading.
   - For each modified requirement, replace the block with the same ID in place with the new text, keep `Origin`, and add or extend `Changed in:` with NNN.
   - For each removed requirement, delete its block and add a line under Retired: the ID, "removed by change NNN", and the reason.
   - Append to History: `- NNN (YYYY-MM-DD): <change title>`.
   - Set `updated` in the frontmatter to today.
3. Move the change directory from `specs/changes/` to `specs/archive/`, keeping its name. Use the version control system's move so history follows.
4. In the archived `spec.md`, set `status: archived` and `updated`. Tick the Gate 3 items in its `checklist.md`.
5. Regenerate `specs/INDEX.md` from the file system, not from the previous index. Active changes: every directory in `specs/changes/`, reading each `spec.md` frontmatter. Capabilities: every `specs/capabilities/*/spec.md` as id, title linked to the spec, owner, the count of `### REQ-` headings, updated. Archived changes: a count and a link to `specs/archive/`.
6. If the constitution frontmatter has a `validator` key, run that command and include its output. Otherwise check by reading: every requirement ID from the change appears in exactly one capability spec, the archive directory exists, `specs/changes/` no longer has it, the index matches the file system.
7. Commit with `Change: NNN`. Report which requirements went to which capabilities, which capabilities were created, and which Purposes need an owner's attention.

## Refuse when

- Status is not `done`. Point to `sdd-verify`.
- A capability section in `requirements.md` is missing from the frontmatter.
- A modified or removed ID is not found in its capability spec.
- Asked to edit requirement text while merging. Merging copies; it does not rewrite.
- Asked to skip the move or the index. Partial archives are how specs go stale.

## Done when

- Every added requirement is in its capability spec with `Origin: NNN`, modified ones carry `Changed in: NNN`, removed ones are under Retired.
- Each touched capability has a History line and today's `updated`.
- The change is under `specs/archive/` with `status: archived`.
- The index reflects the file system.
