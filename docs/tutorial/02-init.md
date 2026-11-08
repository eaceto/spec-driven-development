# 2. Set up the project

One request. The agent asks a few questions, writes a one-page constitution, and leaves you with a `specs/` folder that every later step builds on.

## What to say

> Set up spec-driven development in this project.

## What happens

=== "Claude Code"

    Transcript from a fresh Claude Code session on 8 November 2026. The newcomer's answers were scripted so the run could be repeated; the agent's words are its own, lightly trimmed.

    > **You:** Set up spec-driven development in this project.
    >
    > **Agent:** I'll use the `sdd-init` skill. First I checked the folder: there is no `specs/` directory, and apart from `CLAUDE.md` and the installed skills it is empty, with no source code, README or CI configuration. So this is a new project, not an existing codebase to adopt.
    >
    > I created the layout: `specs/constitution.md`, `specs/INDEX.md`, `specs/templates/`, `specs/capabilities/`, `specs/changes/` and `specs/archive/`, copied the skill's bundled templates into `specs/templates/`, and copied the index template to `specs/INDEX.md`.
    >
    > Before I write the constitution, five quick questions:
    >
    > 1. What is this project for? One or two sentences.
    > 2. Which team owns the constitution?
    > 3. Up to five rules the team already follows?
    > 4. Any terms that must mean exactly one thing across all specs?
    > 5. Should changes be numbered sequentially or by ticket?
    >
    > **You:**
    >
    > 1. A small command-line tool that saves short notes to a text file and lists them. It is a sandbox for learning spec-driven development.
    > 2. notes-team
    > 3. None yet
    > 4. None yet
    > 5. Sequential
    >
    > **Agent:** I'm writing the constitution from the template with your answers, pinning it to the version of the skills installed here, and writing the agent entry file `AGENTS.md` at the project root. The capability map only applies when adopting an existing codebase, so I'm skipping it.
    >
    > Spec-driven development is set up:
    >
    > - `specs/constitution.md`: owner `notes-team`, version 1.0.0, sequential numbering. Purpose is your two sentences. Principles and Definitions say "None yet"; both grow by amendment.
    > - `specs/INDEX.md`: the index with its three tables, all empty.
    > - `specs/templates/`: the templates the other skills will use.
    > - `specs/capabilities/`, `specs/changes/`, `specs/archive/`: empty for now.
    > - `AGENTS.md`: the loading rule and the lifecycle rules for agents. Your `CLAUDE.md` already points to it.
    >
    > Checks: the constitution has no `validator` key, so I checked by reading. `specs/` has exactly six entries; the constitution has its five frontmatter keys and four sections and fits on one page; the index has its three tables; `AGENTS.md` contains the loading rule.
    >
    > Next step: run `sdd-new` to start the first change. Describe the first thing you want the tool to do, for example saving a note, and it becomes change 001.

=== "Devin CLI"

    The same request. Devin reads `.agents/skills/` and `AGENTS.md` on its own, so no slash command is needed. The questions and the files are the same as in the Claude Code tab. A transcript from the owner's Devin run is being added.

## What you now have

```
specs/
  constitution.md     one page: purpose, principles, definitions, amendments
  INDEX.md            three empty tables
  templates/          copied in, so the project does not depend on the skills to read them
  capabilities/       empty until the first archive
  changes/            empty until the first change
  archive/            empty
AGENTS.md             the loading rule and the lifecycle rules
```

The constitution the agent wrote:

```markdown
---
extends: none
version: 1.0.0
owner: notes-team
numbering: sequential
sdd_version: 0.1.0
---

# Constitution

## Purpose

A small command-line tool that saves short notes to a text file and lists them.
It is a sandbox for learning spec-driven development.

## Principles

None yet. Principles are added by amendment, each one sentence a new teammate
can repeat, followed by why it exists.

## Definitions

None yet.

## Amendments

| Version | Date | Change | Summary |
|---|---|---|---|
| 1.0.0 | 2026-11-08 | none | Initial constitution |
```

Commit it, so the first thing in the project's history is its constitution:

```
git add -A && git commit -m "Adopt spec-driven development"
```

!!! note "Two things this run taught us"
    Git does not keep empty folders, so a fresh clone would have lacked `capabilities/`, `changes/` and `archive/` until something landed in them. And the agent created files before asking its questions. Both were fixed the same day in change 005, a quick-tier change: the skill now asks first and leaves a `.gitkeep` in each empty folder. The transcript above shows the skill as it was; the method fixing itself is part of the lesson.

Next: [3. Start a change](03-new.md).
