# Your first change in fifteen minutes

You will take one small change from nothing to an archived capability, with an agent doing the typing and you making the decisions. The project is a command-line tool that saves short notes to a text file. The language does not matter; the method does.

## What you need

- A terminal with `git` and Python 3.9 or later. Python runs the validator; nothing is installed.
- An agent. The transcripts show Claude Code and Devin CLI, in tabs. Other agents that read the open skills standard should work and are [listed as untested](../agents.md).
- An empty folder.

## Words the steps use

- **Change**: a numbered folder under `specs/changes/` holding one unit of work, from one page of purpose to an ordered task list.
- **Capability**: a living description of how the system behaves today, under `specs/capabilities/`. Finished changes merge into it.
- **Gate**: a condition a change must meet to move on. Gate 1 is a person approving the page. Gate 2 is every task done and every requirement tested. Gate 3 is the archive itself.
- **Tier**: how much a change carries. Quick is three files and no behaviour change; standard is five files; full adds guardrails.
- **Statuses**: draft, approved, in-progress, done, archived, always in that order.

## About the Devin tabs

Each step shows a Claude Code transcript. The Devin CLI tab says the request is the same: Devin reads `.agents/skills/` and `AGENTS.md` natively, so the words you say and the files you get do not change. Word-for-word Devin transcripts will be added when a session is available.

## The six steps

1. [Install the skills](01-install.md), one script.
2. [Set up the project](02-init.md): the agent asks four questions and writes the constitution.
3. [Start a change](03-new.md): the agent writes the one page that says why and what, and you approve it.
4. [Plan it](04-plan.md): requirements with scenarios, a design, tasks.
5. [Implement a task](05-implement.md): one task, tests that name the requirement, a commit with trailers.
6. [Verify and archive](06-verify-archive.md): the Gate 2 checklist with evidence, then the merge into a living capability.

Every transcript comes from a real run, with the date stated. The newcomer's answers were scripted so the run could be repeated; the agent's words are its own. Allow about thirty minutes in all.

## When you are done

You will have a `specs/` folder with a one-page constitution, one capability describing what the tool does, one archived change, and an index that shows all of it. Then read [the method](../method.md), which explains every rule you just followed.
