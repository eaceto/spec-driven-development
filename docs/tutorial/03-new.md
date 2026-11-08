# 3. Start a change

You describe what you want. The agent asks what the description leaves open, writes one page that says why it matters and what should be done, and stops. Approving that page is your decision, not the agent's.

## What to say

> Start a change: I want `notes add "some text"` to append a line to a file called notes.txt in the current directory, and `notes list` to print every saved note with a number in front.

## What happens

=== "Claude Code"

    Transcript from a fresh Claude Code session on 8 November 2026. The newcomer's answers were scripted; the agent's words are its own, lightly trimmed.

    > **Agent:** Before I write the spec, five short questions. Answer briefly; I'll skip anything you've covered.
    >
    > 1. Who feels this problem today, and what does it cost them? The request says what the commands do, not who needs them or why.
    > 2. When the work is done, what will be observably true that is not true today? In particular: do the numbers in `notes list` start at 1, and should notes survive after the terminal is closed?
    > 3. What might a reader assume is included that is not? For example editing, deleting, searching or syncing notes.
    > 4. Which capabilities does this touch? The Capabilities table in `specs/INDEX.md` is empty, so there is nothing to pick from. Is this a new capability, and what should it be called?
    > 5. Which tier fits? This adds behaviour, so I'd suggest standard unless you want guardrails of your own.
    >
    > **You:**
    >
    > 1. Me. I lose small notes in chat windows and on sticky notes, and I want one place in the terminal I can trust.
    > 2. `notes add` appends a line to notes.txt, `notes list` prints the notes numbered from 1, and a note is still there after I close the terminal because it lives in the file.
    > 3. Editing or deleting notes, searching, tags, syncing between machines.
    > 4. A new one, call it notes.
    > 5. Standard.
    >
    > **Agent:** `notes` is not in the index, so I'll list it anyway; it will be created as a capability when this change is archived. Tier is standard: the change adds behaviour, so requirements will be added. Numbering is sequential and both `specs/changes/` and `specs/archive/` are empty, so this is 001. The owner field is a team, so I'm using the constitution's owner, `notes-team`. Creating the directory with `spec.md` only, and adding the index row.
    >
    > The constitution has no `validator` key, so I checked by reading: the directory holds exactly `spec.md`; number 001 is unique; the sections are in order; Out has four entries; the frontmatter has every field with `status: draft`.
    >
    > Done. The change lives at `specs/changes/001-add_and_list_notes/spec.md` and is listed as draft in the index.
    >
    > What happens next is Gate 1, which is a human step: the owner of each listed capability reviews `spec.md`, and the approver sets `status: approved`, `approved_by` and `approved_at`. Only after that does `sdd-plan` write requirements, design and tasks. I have not written any of those and have not committed anything.

=== "Devin CLI"

    The same request and the same five questions. A transcript from the owner's Devin run is being added.

## The page it wrote

```markdown
# 001: Add and list notes from the terminal

## Why it matters

Small notes get lost. Today they end up in chat windows and on sticky notes,
with no single place to look for them later. An idea, a reminder or a reference
written down in passing cannot be found when it is needed, and has to be
remembered or rewritten. If nothing is done, there is still no one place in the
terminal to keep such notes and trust that they stay.

## What should be done

A command-line tool called `notes` keeps short notes in a plain text file,
`notes.txt`, in the current directory. `notes add "some text"` saves the text as
a new note. `notes list` prints every saved note with a number in front,
counting from 1. Because the notes live in the file, they are still there after
the terminal is closed and opened again.

## Scope

### In
- `notes add "some text"` appends one line containing the text to `notes.txt`.
- `notes list` prints every saved note, each with a number in front, from 1.
- Notes persist in `notes.txt` between terminal sessions.

### Out
- Editing or deleting notes. Searching. Tags. Syncing between machines.

## Success criteria

- After `notes add "some text"`, `notes.txt` has one more line, and it is `some text`.
- `notes list` prints each note on its own line, numbered from 1.
- In a new terminal in the same directory, `notes list` still prints them.
```

Read it as the person who asked for the tool. Why comes before what. Out says what a reader might assume. Every success criterion is something you could check by hand.

## Your two steps

**Claim the number.** Commit `spec.md` alone, so that in a team nobody else takes 001 on another branch:

```
git add specs/changes/001-add_and_list_notes/spec.md specs/INDEX.md
git commit -m "Claim change 001: add and list notes

Change: 001"
```

**Approve.** This is Gate 1 and it is yours. Open `spec.md`, set three fields in the frontmatter, and commit:

```yaml
status: approved
approved_by: notes-team
approved_at: 2026-11-08
```

```
git commit -am "Approve change 001

Change: 001"
```

In a team, the approval is a pull request containing only this page, reviewed by the owner of the `notes` capability. Here you are both.

Next: [4. Plan it](04-plan.md).
