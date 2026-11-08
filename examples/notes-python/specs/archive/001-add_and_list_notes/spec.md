---
id: "001"
title: Add and list notes from the terminal
status: archived
tier: standard
owner: notes-team
capabilities: [notes]
ticket:
docs:
approved_by: notes-team
approved_at: 2026-11-08
created: 2026-11-08
updated: 2026-11-08
---

# 001: Add and list notes from the terminal

## Why it matters

Small notes get lost. Today they end up in chat windows and on sticky notes, with no single place to look for them later. The person who feels this is the user of this tool: an idea, a reminder or a reference written down in passing cannot be found when it is needed, and has to be remembered or rewritten. If nothing is done, there is still no one place in the terminal to keep such notes and trust that they stay.

## What should be done

A command-line tool called `notes` keeps short notes in a plain text file, `notes.txt`, in the current directory. `notes add "some text"` saves the text as a new note. `notes list` prints every saved note with a number in front, counting from 1. Because the notes live in the file, they are still there after the terminal is closed and opened again.

## Scope

### In

- `notes add "some text"` appends one line containing the text to `notes.txt` in the current directory.
- `notes list` prints every saved note from `notes.txt`, each with a number in front, starting at 1.
- Notes persist in `notes.txt` between terminal sessions.

### Out

- Editing or deleting notes.
- Searching notes.
- Tags.
- Syncing notes between machines.

## Success criteria

- After `notes add "some text"`, `notes.txt` in the current directory has one more line, and that line is `some text`.
- `notes list` prints each saved note on its own line with a number in front, numbered from 1.
- After closing the terminal and opening a new one in the same directory, `notes list` still prints the notes added before, because they live in `notes.txt`.

## Constraints specific to this change

- Notes are stored as plain text in `notes.txt` in the current directory, one note per line.
