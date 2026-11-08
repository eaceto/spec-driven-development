# 001: Requirements

## Capability: notes

### REQ-001-01: Add a note
When `notes add <text>` is run, the `notes` command SHALL append one line containing exactly the text to `notes.txt` in the current directory, creating the file if it does not exist.

#### Scenario: Append to existing notes
- GIVEN `notes.txt` in the current directory holds two lines
- WHEN `notes add "Buy milk"` is run
- THEN `notes.txt` holds three lines, the last line is `Buy milk`, and the exit status is 0

#### Scenario: First note creates the file
- GIVEN no `notes.txt` exists in the current directory
- WHEN `notes add "Buy milk"` is run
- THEN `notes.txt` exists in the current directory and holds exactly one line, `Buy milk`

#### Scenario: Text that would span more than one line is refused
- GIVEN `notes.txt` in the current directory holds two lines
- WHEN `notes add` is run with text that contains a newline character
- THEN `notes.txt` still holds the same two lines, an error is printed to stderr, and the exit status is not 0

### REQ-001-02: List notes with numbers
When `notes list` is run, the `notes` command SHALL print every line of `notes.txt` in the current directory to stdout, one note per line, in file order, each prefixed with its position counting from 1 in the form `N. text`.

#### Scenario: Three saved notes
- GIVEN `notes.txt` in the current directory holds the lines `Buy milk`, `Call the dentist` and `Read chapter 4`
- WHEN `notes list` is run
- THEN stdout is exactly the three lines `1. Buy milk`, `2. Call the dentist` and `3. Read chapter 4`, and the exit status is 0

#### Scenario: No notes yet
- GIVEN no `notes.txt` exists in the current directory, or it is empty
- WHEN `notes list` is run
- THEN nothing is printed to stdout and the exit status is 0

### REQ-001-03: Notes persist between runs
The `notes` command SHALL keep every added note in `notes.txt` in the current directory so that a later, separate run of `notes list` in the same directory prints it.

#### Scenario: Note added in one run is listed in the next
- GIVEN `notes add "Buy milk"` has run in a directory and that process has exited
- WHEN a new process runs `notes list` in the same directory
- THEN stdout contains the line `1. Buy milk`

## Modified requirements

None. The `notes` capability has no spec yet; this is the first change to touch it.

## Removed requirements

None.

## Not testable

None. Every requirement above is checked by running the script and inspecting `notes.txt` or its output.
