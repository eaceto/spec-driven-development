---
id: "002"
title: Lifecycle skills
status: done
tier: standard
owner: maintainers
capabilities: [skills]
ticket:
docs:
approved_by: Ezequiel Aceto
approved_at: 2026-11-08
created: 2026-11-08
updated: 2026-11-08
---

# 002: Lifecycle skills

## Why it matters

Templates and a method document make spec-driven development possible. They do not make it happen. Every existing tool shows where adoption dies: people skip the clarifying questions, start designing before the spec is agreed, declare work done without checking the list, and never archive. The specs then drift from the code and the method is abandoned within months.

Agents now do much of the implementation work in many teams. An agent without a procedure improvises a different process every time, and a team with several agents gets several processes. Skills turn each step of the lifecycle into a procedure that runs the same way every time, in every repository, from any supported tool. Without them the method is a style guide. With them it is a workflow.

## What should be done

Deliver one skill per step of the lifecycle, in the open Agent Skills format, so that an agent can carry a change from an empty repository to an archived capability without a person remembering the rules:

- `sdd-init`: create `specs/` in a new project, or adopt an existing one by writing the constitution from existing material and a thin capability map.
- `sdd-new`: turn a conversation into a `spec.md`, asking a bounded number of clarifying questions, claim the next number, and add the change to the index.
- `sdd-plan`: after approval, write requirements, design and tasks. Refuse on a draft.
- `sdd-implement`: execute one task at a time, cite requirement IDs in commits, and stop when a task contradicts a requirement.
- `sdd-verify`: run the Gate 2 checklist and report exactly what blocks done.
- `sdd-archive`: merge requirements into capability specs, move the change to the archive, regenerate the index.

Each skill knows which status it may act on and refuses otherwise. Each loads only what the loading rule allows. Each leaves the files in a state the templates and the method define, whether or not the validator is installed. Installing the skills into a project places them where Devin, Claude Code and other agents following the standard look for them.

## Scope

### In

- The six skills above, each as a `SKILL.md` with any supporting files
- Preconditions and refusals per skill, keyed on the change status
- Clarifying questions in `sdd-new`, with an upper bound
- Capability map generation in `sdd-init` for existing projects
- Index maintenance by `sdd-new` and `sdd-archive`
- The install step: where skills are copied or linked in a target project, and how a project pins the version
- Behaviour when the validator is absent: the skill performs the checks it can by reading the files

### Out

- The validator script. It is change 003. Skills call it when present.
- Role guides for people. Change 004.
- The aggregated index across repositories. Change 005.
- Publishing to a skills marketplace or package registry.
- Verified support for agents other than Devin CLI and Claude Code in this version.

## Success criteria

- From an empty repository, `sdd-init` followed by `sdd-new` produces a layout and a change directory that satisfy every requirement of change 001, with no manual edits, in both Devin CLI and Claude Code.
- `sdd-plan` invoked on a change with status draft refuses and names Gate 1.
- `sdd-archive` run on a done change produces capability specs whose requirements match the change's requirements exactly, with Origin set, and the change directory ends in `specs/archive/`.
- Each skill, read by a person, is a procedure they could follow by hand. No skill exceeds two screens.
- A skill run on a change loads the constitution, the index, that change and its listed capabilities, and nothing else.

## Constraints specific to this change

- No vendor-specific instruction inside a skill body. Tool-specific paths appear only in the install step.
- Skills must behave identically with and without the validator; the validator only makes the checks faster and stricter.
