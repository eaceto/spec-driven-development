# Example: a greenfield Go project

The folder [`examples/greenfield-go`](https://github.com/eaceto/spec-driven-development/tree/main/examples/greenfield-go) is a real run of the method, kept exactly as the skills produced it on 8 November 2026 with Claude Code. Nothing in it was tidied afterwards, so its `specs/templates/` folder is a snapshot of the templates as they were that day; the current ones are in [`specs/templates`](https://github.com/eaceto/spec-driven-development/tree/main/specs/templates) at the repository root. It took thirty minutes from an empty folder to an archived capability, including a Go module and its tests.

## What happened, in order

**Adopt.** The developer ran `install.sh` into an empty folder, opened the agent and asked it to set up spec-driven development. The `sdd-init` skill asked four questions: what the project is for, who owns the constitution, how changes are numbered, and which rules the team already follows. The answers were a trial sandbox, one owner, sequential numbering, and no rules yet. The skill created `specs/`, a one-page constitution, an empty index, the templates and `AGENTS.md`.

**Start a change.** Asked for a hello world command-line tool in Go, `sdd-new` wrote `specs/changes/001-hello_world_cli/spec.md`: why it matters, what should be done, scope with a non-goal, success criteria. The developer approved it by setting the three approval fields.

**Plan.** `sdd-plan` wrote three requirements under a capability called `greeting`, each with a SHALL statement and a scenario:

- REQ-001-01, print exactly `Hello, World!` and a newline
- REQ-001-02, exit with status 0 and nothing on standard error
- REQ-001-03, depend on the Go standard library only

Then a design with its decisions, six tasks citing those requirement ids, and the checklist with Gate 1 ticked.

**Implement.** `sdd-implement` took one task at a time. Each produced two commits: the work, with a `Requirements:` trailer naming the ids it covered, and the tick. The tests name the requirement ids they check, which is what later lets the gate count coverage.

**Verify.** `sdd-verify` went through Gate 2 with evidence for every item and moved the change to done.

**Archive.** `sdd-archive` created `specs/capabilities/greeting/spec.md` with the three requirements, each marked `Origin: 001`, moved the change to `specs/archive/`, and regenerated the index.

## The commit history

```
Adopt spec-driven development
001: Spec and plan for hello world CLI in Go
Initialise Go module                                  Change: 001
Print the greeting from a testable run function       Change: 001  Requirements: REQ-001-01, REQ-001-02
001: Tick T01 … 001: Tick T06
Test the real entry point in a subprocess             Change: 001  Requirements: REQ-001-01, REQ-001-02
Test that go.mod declares no dependencies             Change: 001  Requirements: REQ-001-03
Add README with run and test instructions             Change: 001
001: Pass Gate 2, mark done                           Change: 001
001: Archive hello world CLI, add greeting capability Change: 001
```

Every commit that belongs to the change carries its `Change:` trailer. The implementation commits also carry `Requirements:`, so `git log --grep` answers which commits delivered a requirement.

## What to look at

- [`specs/capabilities/greeting/spec.md`](https://github.com/eaceto/spec-driven-development/blob/main/examples/greenfield-go/specs/capabilities/greeting/spec.md): a living capability after one change. Purpose, three requirements with origin, an empty Retired list, one history line.
- [`specs/archive/001-hello_world_cli/`](https://github.com/eaceto/spec-driven-development/tree/main/examples/greenfield-go/specs/archive/001-hello_world_cli): the five files of a standard-tier change, with every gate ticked.
- [`specs/INDEX.md`](https://github.com/eaceto/spec-driven-development/blob/main/examples/greenfield-go/specs/INDEX.md): no active changes, one capability, one archived change.
- [`main_test.go`](https://github.com/eaceto/spec-driven-development/blob/main/examples/greenfield-go/main_test.go): tests that name the requirement ids.

## Two honest notes

The first commit held the spec and the plan together, although the method asks for `spec.md` alone to be committed first so the number is claimed. The skills say so; the agent committed only at the end. The capability row in the index linked the id column instead of the title. That ambiguity in the skills was fixed the same day. Both are the kind of thing a real run teaches and a rehearsed one hides.

The folder passes the validator with zero violations:

```
python3 specs/validate.py --root examples/greenfield-go
```
