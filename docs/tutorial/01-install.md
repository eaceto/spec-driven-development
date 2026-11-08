# 1. Install the skills

The skills are files. Installing them copies six folders into the places agents look, and nothing else changes on your machine.

## Clone once, install anywhere

```
git clone https://github.com/eaceto/spec-driven-development.git
mkdir notes && cd notes && git init
../spec-driven-development/install.sh .
```

The script reports what it did:

```
validator: none yet; sdd-init will write it with sdd_version 0.1.0, then rerun install.sh to set the validator key
CLAUDE.md: created, pointing to AGENTS.md
skills copied into /…/notes: sdd-archive sdd-implement sdd-init sdd-new sdd-plan sdd-verify
locations: .agents/skills .claude/skills
next: in your agent, run sdd-init (new project) or sdd-new (project already initialised)
```

## What is now in the folder

```
.agents/skills/sdd-*/      read by Devin CLI and other agents following the standard
.claude/skills/sdd-*/      read by Claude Code
CLAUDE.md                  one line, pointing to AGENTS.md, which the next step creates
```

The constitution and the validator key arrive in the next step, when `sdd-init` creates `specs/`. Running `install.sh .` again afterwards copies the validator into `specs/` and sets the key.

## Open your agent

=== "Claude Code"

    ```
    cd notes
    claude
    ```

    The skills appear under `/sdd-init`, `/sdd-new` and so on, and Claude Code also triggers them from plain language.

=== "Devin CLI"

    ```
    cd notes
    devin
    ```

    Devin reads `.agents/skills/` and `AGENTS.md` on its own. Ask for what you want in plain language.

Next: [2. Set up the project](02-init.md).
