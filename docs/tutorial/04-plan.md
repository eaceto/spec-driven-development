# 4. Plan it

Now that the one page is approved, the agent turns it into requirements with scenarios, a design with its decisions, and an ordered list of tasks. This is the step the agent does mostly alone; your part is to read what it wrote.

## What to say

> Plan change 001.

## What happens

=== "Claude Code"

    Transcript from a fresh Claude Code session on 8 November 2026, lightly trimmed. One decision was supplied in advance so the run could be repeated: a single Python 3 script named `notes`, standard library only, tests under `tests/` run by `python3 -m unittest`.

    > **Agent:** Following the skill's preconditions I loaded `spec.md`, the constitution, the index, the change templates and `AGENTS.md`. The change lists the capability `notes`, which has no spec yet; that is normal before a first archive, so there was nothing more to load.
    >
    > Status is approved, so I may proceed. Tier is standard, so the full set of files applies: requirements, design, tasks, checklist.
    >
    > Requirements. From "What should be done" and the three success criteria I derived three requirements under `## Capability: notes`: add a note, list notes with numbers from 1, and notes persist between separate runs. The spec's constraint "one note per line" gave the first requirement a third scenario: text containing a newline is refused and nothing is written. Every requirement stays within the capability the frontmatter lists, so there was no reason to stop.
    >
    > Design. Planning raised four questions the spec does not answer: the exact list format, what `list` prints when there are no notes, what `add` does with text containing a newline, and whether `add` takes one argument or several. The skill says to resolve open questions now where I can, so I answered each as a recorded decision. I also recorded that an unknown subcommand prints usage and exits 2, marked explicitly as not a requirement, because the approved spec does not ask for it and widening the scope would restart Gate 1.
    >
    > Tasks. Six, in order: a setup task for the script skeleton and the test helper, one task per requirement, then tests for every id and a README.
    >
    > Checklist. From the template. I ticked the two Gate 1 items the frontmatter proves and left the rest for a person.
    >
    > Set `status: in-progress` in `spec.md` and in the index row. The constitution has no `validator` key, so I checked by reading: the directory holds exactly the five standard files; the requirements have three, two and one scenarios; every task cites a requirement id, `[all]` or `[setup]`; the one capability section matches the frontmatter.
    >
    > Change 001 is planned: 3 requirements under capability `notes`, 6 tasks. Nothing was implemented and nothing committed. The next step is `sdd-implement`, which takes the first unticked task.

=== "Devin CLI"

    Same request. Devin reads `.agents/skills/` and `AGENTS.md` natively, so the words and the files are the same.

??? note "What it wrote: one requirement and the task list"
    One of the three requirements, as written:

    ```markdown
    ### REQ-001-01: Add a note
    When `notes add <text>` is run, the `notes` command SHALL append one line
    containing exactly the text to `notes.txt` in the current directory, creating
    the file if it does not exist.

    #### Scenario: Append to existing notes
    - GIVEN `notes.txt` in the current directory holds two lines
    - WHEN `notes add "Buy milk"` is run
    - THEN `notes.txt` holds three lines, the last line is `Buy milk`, and the exit status is 0

    #### Scenario: Text that would span more than one line is refused
    - GIVEN `notes.txt` in the current directory holds two lines
    - WHEN `notes add` is run with text that contains a newline character
    - THEN `notes.txt` still holds the same two lines, an error is printed to stderr, and the exit status is not 0
    ```

    The tasks, abridged:

    ```markdown
    - [ ] T01 Create the `notes` script, a `main()` that dispatches on the first argument,
          and a test helper that runs the script in a temporary directory. [setup]
    - [ ] T02 Implement `notes add <text...>` … [REQ-001-01]
    - [ ] T03 Implement `notes list` … [REQ-001-02]
    - [ ] T04 Make persistence hold across runs … [REQ-001-03]
    - [ ] T05 Tests exist for every requirement ID; `python3 -m unittest` passes [all]
    - [ ] T06 README shows how to run `notes add`, `notes list` and the tests [all]
    ```

    Every task cites the requirement ids it satisfies. That is what later lets a commit, a test and a requirement be matched without anyone remembering.

## What to read, and why

Read the requirements as the person who will accept the work. Each SHALL statement is one sentence you could check. Each scenario is a test waiting to be written. If one is wrong, now is the cheap moment to say so: edit `requirements.md` before any code exists.

Read the design's decisions as the person who will maintain the code. The agent chose `N. text` for the list format and chose to refuse multi-line notes. If you would have chosen differently, change the decision now.

Notice what the agent did not do. It found behaviours the spec never mentioned, such as what happens on an unknown subcommand, and recorded them as design decisions rather than adding requirements. Adding requirements would have widened the approved scope, and the skill refuses to do that.

## Your step

Commit the plan:

```
git add specs && git commit -m "Plan change 001: requirements, design and tasks

Change: 001"
```

Next: [5. Implement a task](05-implement.md).
