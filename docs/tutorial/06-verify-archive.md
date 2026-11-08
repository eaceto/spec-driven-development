# 6. Verify and archive

Two requests close the change. Verify walks the Gate 2 checklist with evidence and moves the change to done only if everything passes. Archive merges the requirements into a living capability spec, moves the change to the archive, and regenerates the index. After this, the capability is the description of what your tool does.

## What to say

> Verify change 001.

Then:

> Archive change 001.

## Verify

=== "Claude Code"

    Transcript from a fresh Claude Code session on 8 November 2026, lightly trimmed.

    > **Agent:** Status is in-progress, so the gate applies. I gathered evidence: the tasks file, each requirement id searched for in the tests, the Not testable and Open questions sections, the constitution's principles, the README, a manual run of the script in a temporary directory, and `python3 -m unittest`: 15 tests, OK.
    >
    > | Gate 2 item | Verdict | Evidence |
    > |---|---|---|
    > | Every success criterion in spec.md is met | pass | Each criterion has a named test and a manual run: `./notes add "some text"` then one line in the file; `./notes list` printed `1. some text`; add and list in two separate processes. |
    > | Every task in tasks.md is ticked | pass | Six of six, no unticked lines. |
    > | Every requirement id is referenced by a test, or listed as not testable | pass | REQ-001-01 in six test names, REQ-001-02 in four, REQ-001-03 in two. Not testable says none. |
    > | No open questions remain in design.md | pass | The section reads none and points to the decisions that answered them. |
    > | Constitution principles checked, none violated | pass | The constitution has no principles yet, so none applied. |
    > | Documentation updated | pass | README shows add, list, where notes live, and how to run the tests. |
    >
    > Every item passes. Ticked the Gate 2 items, set `status: done` in `spec.md` and the index, and committed `Change 001 passes Gate 2: done`. Next step: `sdd-archive`.

=== "Devin CLI"

    The same request. A transcript from the owner's Devin run is being added.

Had one item failed, nothing would have changed and the report would say what makes it pass. The gate is the point.

## Archive

=== "Claude Code"

    > **Agent:** Consistency checks: status is done; the one capability section in `requirements.md`, `notes`, matches the frontmatter; nothing modified or removed; neither `specs/capabilities/` nor `specs/archive/` has anything yet, so this is the project's first archive.
    >
    > Created `specs/capabilities/notes/spec.md` from the template: id `notes`, title Notes, owner `notes-team`, a two-sentence purpose taken from the change's Why and What. Copied the three requirements in with `Origin: 001` under each heading. Retired is empty. History: `001 (2026-11-08): Add and list notes from the terminal`.
    >
    > Moved `specs/changes/001-add_and_list_notes` to `specs/archive/` with `git mv`, set `status: archived`, ticked the Gate 3 items, and regenerated `specs/INDEX.md` from the file system: no active changes, one capability with three requirements, one archived change.
    >
    > Checked by reading: each requirement id appears in exactly one capability spec; the archive directory exists; the index matches the file system. Committed `Archive change 001: notes capability created from its requirements`.
    >
    > The purpose of `notes` was derived from the change; the owner should refine it.

=== "Devin CLI"

    The same request. A transcript from the owner's Devin run is being added.

## What you have now

```
specs/
  constitution.md
  INDEX.md                      no active changes, 1 capability, 1 archived
  capabilities/notes/spec.md    three requirements with Origin: 001, one history line
  archive/001-add_and_list_notes/   the five files, every gate ticked
  changes/                      empty, ready for 002
```

The capability spec is the living truth. The next change that touches notes will list `notes` in its frontmatter, its owner will review the one page, and when it archives, its requirements join these three, modify them in place with a `Changed in` line, or retire them by id. The archive is history. Nobody loads it unless they ask.

The whole run, from an empty folder to here, took the agent about twenty minutes of wall-clock time across six sessions, with the newcomer's part being four answers, five answers, one approval and a handful of commits. The validator reports zero violations on the result:

```
python3 specs/validate.py --root .
0 violations, 7 files, 21 rules
```

You have done the method once. Now read [what every rule you followed is for](../method.md).
