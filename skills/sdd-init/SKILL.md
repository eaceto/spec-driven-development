---
name: sdd-init
description: Set up spec-driven development in a project that has no specs/ directory. Creates the layout, constitution, index, templates and agent entry file for a new project, or adopts an existing codebase by deriving the constitution from existing documents and writing a capability map without requirements. Use when asked to start, adopt or initialise spec-driven development.
metadata:
  sdd_version: 0.3.0
---

# sdd-init

## When to use

The project has no `specs/` directory and wants to adopt spec-driven development. Works for an empty repository and for a codebase that already exists.

## Preconditions

- You are at the project root.
- `specs/` does not exist, or exists and is empty.
- This skill's `templates/` directory is present. The install step bundles it.

## Steps

1. Pick the mode. If the repository contains source code, a README or CI configuration, it is an existing project. Otherwise it is a new project. Agent configuration files and the installed skills themselves do not count as source code.
2. Ask before you create anything.
   - New project: ask at most five questions, skipping any the person already answered: what the project is for; which team owns the constitution; up to five rules the team already follows; terms that must mean one thing; whether numbering is sequential or by ticket.
   - Existing project: read the README, contributing guide, architecture decisions, CI and lint configuration. Ask only who owns the constitution.
3. Create the layout: `specs/constitution.md`, `specs/INDEX.md`, `specs/templates/`, `specs/capabilities/`, `specs/changes/`, `specs/archive/`. Leave an empty `.gitkeep` in `capabilities/`, `changes/` and `archive/` so the folders survive a commit. Copy everything in this skill's `templates/` into `specs/templates/`. Copy `specs/templates/INDEX.md` to `specs/INDEX.md`.
4. Write the constitution from `specs/templates/constitution.md`, removing the template's guidance comments as you fill each section.
   - New project: purpose and principles from the answers. If the team has no rules or shared terms yet, write "None yet" under Principles and under Definitions; both grow by amendment.
   - Existing project: derive each principle from a sentence found in what you read and name the source in its "why". Invent nothing.
   - Frontmatter: `extends: none` unless told otherwise, `version: 1.0.0`, `owner`, `numbering`, and `sdd_version` copied from `metadata.sdd_version` in this skill's `SKILL.md` file. Read the file if your tool shows you only the body.
   - The first Amendments row has `none` in its Change column: the initial constitution comes from no change.
   - At most 80 lines, which is what the validator treats as one page. With more than ten candidate principles, keep the ten that matter most.
5. Existing project only: write the capability map. Identify capabilities from the top-level modules, services or domains named in what you read. For each, create `specs/capabilities/<id>/spec.md` from `specs/templates/capability.md` with `id`, `title`, `owner` if known, a one-paragraph Purpose, and empty Requirements, Retired and History sections. Write no requirements. Stop at the obvious ones; fifteen is already too many.
6. Existing project only: fill the Capabilities table in `specs/INDEX.md` from the map: id, title linked to the capability spec, owner, requirement count 0, today.
7. Write `AGENTS.md` at the project root from `specs/templates/AGENTS.md`. If one already exists, append the two sections instead of replacing it.
8. If the constitution frontmatter has a `validator` key, run that command and include its output in your report. Otherwise check by reading: the six entries exist, the constitution has its five frontmatter keys and four sections, the index has its three tables.
9. Report what you created, suggest committing it as the project's first commit, and name the next step: `sdd-new` to start the first change.

## Refuse when

- `specs/` already exists and is not empty. Say so and stop.
- You are asked to write requirements for existing code. The capability map holds purpose only. Requirements enter through changes, starting with the next thing the team was going to build anyway.
- A proposed principle cannot be traced to existing material in an existing project. Leave it out and say so.

## Done when

- `specs/` has exactly the six entries, each empty folder holding a `.gitkeep`.
- `specs/constitution.md` fits in 80 lines and has `extends`, `version`, `owner`, `numbering` and `sdd_version`.
- `specs/INDEX.md` has Active changes, Capabilities and Archived changes.
- `AGENTS.md` at the root contains the loading rule.
- Existing project: one capability folder per identified capability, each with a Purpose and no requirements.
