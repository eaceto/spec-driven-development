# Agents

The skills are written in the open Agent Skills format: a directory holding a `SKILL.md`, read by any agent that supports the standard. The install script places them where each agent looks.

## Tested

| Agent | Reads skills from | Entry file | Status |
|---|---|---|---|
| Claude Code | `.claude/skills/` | `CLAUDE.md`, which points to `AGENTS.md` | Tested: full lifecycle and refusal paths, 8 November 2026 |
| Devin CLI | `.agents/skills/` | `AGENTS.md` | Tested: full lifecycle, 8 November 2026 |

## Untested, expected to work

Any agent that reads `.agents/skills/` under the Agent Skills standard should find the six skills without further setup. We have not run them. If you do, tell us what happened and the row moves up.

| Agent | Reads skills from | Status |
|---|---|---|
| OpenAI Codex | `.agents/skills/` | Untested |
| Cursor | `.agents/skills/` or `.cursor/skills/` | Untested |
| GitHub Copilot | `.agents/skills/` or `.github/skills/` | Untested |
| Others following the standard | `.agents/skills/` | Untested |

## What every agent needs

Two files at the project root, both created for you:

- `AGENTS.md`, written by `sdd-init`, holds the loading rule and the lifecycle rules. Most agents read it on their own.
- A pointer file for agents that read their own entry file instead. The install script creates `CLAUDE.md` pointing to `AGENTS.md`.

The loading rule is the part that matters most: constitution, index, the one change in play, and only the capabilities that change lists. An agent that loads every spec burns its context and starts improvising.

## Without an agent

Every skill is a procedure a person can follow by hand. Open the skill page, follow its Steps section, and check yourself against its Refuse when section. The validator checks the result either way.
