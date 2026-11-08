# 001: Tasks

## Setup

- [x] T01 Create the `notes` script at the project root with a `#!/usr/bin/env python3` shebang and the executable bit, a `main()` that dispatches on the first argument, and a usage message on stderr with exit status 2 for a missing or unknown subcommand. Create an empty `tests/__init__.py` and a `tests/test_notes.py` holding a helper that runs the script as a subprocess in a temporary directory, so `python3 -m unittest` from the project root finds and runs the tests. [setup]

## Implementation

- [x] T02 Implement `notes add <text...>`: join the arguments after `add` with single spaces; if the text is empty or contains a newline, print an error to stderr, write nothing and exit 1; otherwise append the text plus `\n` to `notes.txt` in the current directory, creating the file if absent and adding a `\n` first if the file does not already end with one. Tests: appending to an existing file adds exactly one line equal to the text; the first add creates the file with one line; text with a newline is refused and the file is unchanged. [REQ-001-01]
- [x] T03 Implement `notes list`: read `notes.txt` from the current directory as UTF-8 with `errors="replace"`, and print each line as `N. text` with N counting from 1; when the file is missing or empty, print nothing and exit 0. Tests: three saved notes produce exactly three numbered lines in file order; a missing file and an empty file both produce no output and exit 0. [REQ-001-02]
- [x] T04 Make persistence hold across runs: the script opens `notes.txt` afresh on every invocation and keeps nothing between runs. Test: run `notes add "Buy milk"` in one subprocess, let it exit, then run `notes list` in a second subprocess in the same directory and check that stdout contains `1. Buy milk`. [REQ-001-03]

## Verification

- [x] T05 Tests exist for every requirement ID above, each test names the IDs it covers, and `python3 -m unittest` run from the project root passes [all]
- [x] T06 Documentation updated: a `README.md` at the project root shows how to run `notes add` and `notes list`, says that notes live in `notes.txt` in the current directory, and shows how to run the tests [all]
