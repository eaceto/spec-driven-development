# 5. Implement a task

One task per request. The agent reads the task's requirement and scenarios, checks the task against them before writing anything, implements it with tests that name the requirement, commits with the trailers, ticks the task and stops. You say when to continue.

## What to say

> Implement the next task of change 001.

Then, when it stops:

> Continue with the next task.

## What happens

=== "Claude Code"

    Transcript from a fresh Claude Code session on 8 November 2026, lightly trimmed.

    > **Agent:** Status is in-progress, so I may proceed. The first unticked task is T01, marked setup, so it may cite no requirement id. Before writing: T01 asks for the `notes` script with a dispatcher and usage on an unknown subcommand, plus the test scaffold. The usage behaviour is not in any requirement, but the design records it as a decision and it contradicts nothing in the requirements. No gap, so I implemented.
    >
    > Implemented the script with an empty command table that later tasks register into, and a test helper that runs the script as a subprocess in a temporary directory, with three smoke tests. `python3 -m unittest`: 3 tests, OK.
    >
    > Commit, setup task so `Change:` only:
    > ```
    > Set up the notes script and test scaffold
    >
    > Change: 001
    > ```
    > Ticked T01 and committed the tick. Next unticked task: T02, `notes add`, REQ-001-01. Stopping here as the skill says.
    >
    > **You:** Continue with the next task.
    >
    > **Agent:** First unticked task is T02, citing REQ-001-01. I re-read its three scenarios and the design decisions that bear on it: refuse text that cannot be one line, join several arguments with single spaces, repair a missing trailing newline before appending. Nothing contradicts the requirement, so I implemented.
    >
    > Added `cmd_add` and six tests, every one named `test_req_001_01_…`: the three scenarios, plus the three design decisions with a comment citing each. `python3 -m unittest`: 9 tests, OK.
    >
    > Commit with both trailers:
    > ```
    > Add notes add: append one line to notes.txt
    >
    > Change: 001
    > Requirements: REQ-001-01
    > ```
    > Ticked T02. Ids now covered: REQ-001-01, six tests name it. Next unticked task: T03, `notes list`, REQ-001-02. Stopping here.

=== "Devin CLI"

    The same two requests. A transcript from the owner's Devin run is being added.

## What the history looks like

```
Tick T02: notes add implemented and tested          Change: 001
Add notes add: append one line to notes.txt         Change: 001  Requirements: REQ-001-01
Tick T01: notes script and test scaffold in place   Change: 001
Set up the notes script and test scaffold           Change: 001
```

Two commits per task: the work, and the tick. The work commit says which requirements it covers. Later, `git log --grep "REQ-001-01"` answers which commits delivered that requirement, and the Gate 2 check counts a requirement as tested because a test names it:

```python
class AddNoteTests(NotesTestCase):
    """REQ-001-01: Add a note."""

    def test_req_001_01_append_to_existing_notes_adds_one_line(self): ...
    def test_req_001_01_first_note_creates_the_file(self): ...
    def test_req_001_01_text_with_newline_is_refused_and_file_unchanged(self): ...
```

## The stop is the point

The agent stops after every task unless you say otherwise. That pause is where you look at the diff, run the tool, and catch a wrong turn while it is one commit wide. Had the task needed behaviour no requirement describes, the skill would have stopped without writing code and named the gap; the fix is a reviewed edit of `requirements.md`, never a quiet workaround.

For the remaining tasks, say "continue until every task is done". The agent goes task by task, with the same two commits each, and stops at the end.

Next: 6. Verify and archive.
