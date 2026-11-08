# Example: the tutorial's notes tool

The folder [`examples/notes-python`](https://github.com/eaceto/spec-driven-development/tree/main/examples/notes-python) is the project the [tutorial](../tutorial/index.md) builds, kept exactly as six fresh Claude Code sessions produced it on 8 November 2026. The transcripts on the tutorial pages are of this run. Its `specs/templates/` folder is a snapshot from that day; the current templates are at the repository root.

## What is in it

A single Python 3 script, `notes`, standard library only. `notes add "text"` appends a line to `notes.txt` in the current directory; `notes list` prints the notes numbered from 1. Fifteen tests in `tests/test_notes.py` drive the script as a subprocess, and every test is named after the requirement it checks.

```
specs/
  constitution.md                 owner notes-team, no principles yet
  INDEX.md                        no active changes, 1 capability, 1 archived
  capabilities/notes/spec.md      three requirements, Origin 001
  archive/001-add_and_list_notes/ the five files, every gate ticked
```

## The history, as the commits tell it

```
Adopt spec-driven development
Claim change 001: add and list notes                 Change: 001
Approve change 001                                   Change: 001
Plan change 001: requirements, design and tasks      Change: 001
Set up the notes script and test scaffold            Change: 001
Tick T01 …
Add notes add: append one line to notes.txt          Change: 001  Requirements: REQ-001-01
Tick T02 …
Add notes list: print each note as N. text           Change: 001  Requirements: REQ-001-02
Tick T03 …
Test that notes persist across separate runs         Change: 001  Requirements: REQ-001-03
Tick T04 …
Tick T05: every requirement ID has a named test      Change: 001  Requirements: REQ-001-01, REQ-001-02, REQ-001-03
Add README: how to add and list notes                Change: 001  Requirements: REQ-001-01, REQ-001-02, REQ-001-03
Tick T06 …
Change 001 passes Gate 2: done                       Change: 001
Archive change 001: notes capability created         Change: 001
```

The claim and the approval are separate human commits, which the Go example lacked. Every other commit is the skills' own.

## What to compare with the Go example

Two languages, two agents' worth of decisions, the same shape: one capability, one archived change, requirement ids in test names, trailers on every commit. The method does not care what the code is written in.

```
python3 specs/validate.py --root examples/notes-python
0 violations, 8 files, 21 rules; git checks skipped
```
