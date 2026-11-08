---
name: sdd-init
description: Set up spec-driven development in a project that has no specs/ directory. Creates the layout, constitution, index, templates and agent entry file for a new project, or adopts an existing codebase by deriving the constitution from existing documents and writing a capability map without requirements. Use when asked to start, adopt or initialise spec-driven development.
metadata:
  version: 0.1.0
  sdd_version: 0.1.0
---

# sdd-init

## When to use

The project has no `specs/` directory and wants to adopt spec-driven development. Works for an empty repository and for a codebase that already exists.

## Preconditions

- You are at the project root.
- `specs/` does not exist.
- This skill's `templates/` directory is present. The install step bundles it.

## Steps

1. Pick the mode. If the repository contains source code, a README or CI configuration, it is an existing project. Otherwise it is a new project.
2. Create the layout: `specs/constitution.md`, `specs/INDEX.md`, `specs/templates/`, `specs/capabilities/`, `specs/changes/`, `specs/archive/`. Copy everything in this skill's `templates/` into `specs/templates/`. Copy `specs/templates/INDEX.md` to `specs/INDEX.md`.
3. Write the constitution from `specs/templates/constitution.md`.
   - New project: ask at most five questions, skipping any the person already answered: what the project is for; which team owns the constitution; up to five rules the team already follows; terms that must mean one thing; whether numbering is sequential or by ticket.
   - Existing project: read the README, contributing guide, architecture decisions, CI and lint configuration. Derive each principle from a sentence found there and name the source in its "why". Invent nothing. Ask only who owns the constitution.
   - Frontmatter: `extends: none` unless told otherwise, `version: 1.0.0`, `owner`, `numbering`, and `sdd_version` from this skill's metadata.
   - Keep it to one page. With more than ten candidate principles, keep the ten that matter most.
4. Existing project only: write the capability map. Identify capabilities from the top-level modules, services or domains named in what you read. For each, create `specs/capabilities/<id>/spec.md` from `specs/templates/capability.md` with `id`, `title`, `owner` if known, a one-paragraph Purpose, and empty Requirements, Retired and History sections. Write no requirements. Stop at the obvious ones; fifteen is already too many.
5. Fill the Capabilities table in `specs/INDEX.md` from the map: id, title linked to the capability spec, owner, requirement count 0, today.
6. Write `AGENTS.md` at the project root from `specs/templates/AGENTS.md`. If one already exists, append the two sections instead of replacing it.
7. If the constitution frontmatter has a `validator` key, run that command and include its output in your report. Otherwise check by reading: the six entries exist, the constitution has its five frontmatter keys and four sections, the index has its three tables.
8. Report what you created and name the next step: `sdd-new` to start the first change.

## Refuse when

- `specs/` already exists. Say so and stop.
- You are asked to write requirements for existing code. The capability map holds purpose only. Requirements enter through changes, starting with the next thing the team was going to build anyway.
- A proposed principle cannot be traced to existing material in an existing project. Leave it out and say so.

## Done when

- `specs/` has exactly the six entries.
- `specs/constitution.md` fits on one page and has `extends`, `version`, `owner`, `numbering` and `sdd_version`.
- `specs/INDEX.md` has Active changes, Capabilities and Archived changes.
- `AGENTS.md` at the root contains the loading rule.
- Existing project: one capability folder per identified capability, each with a Purpose and no requirements.
