# 001: Design

## Approach

The tool is one executable Python 3 script, `notes`, at the project root, using only the standard library. Its `main()` reads `sys.argv`: the first argument picks the subcommand, `add` or `list`; anything else prints a one-line usage message to stderr and exits with status 2.

`add` joins the arguments after `add` with single spaces, checks that the text is not empty and contains no newline, and appends the text followed by `\n` to `notes.txt` in the current working directory, creating the file if it is missing. `list` reads `notes.txt` from the current working directory if it exists, splits it into lines, and prints each line as `N. text` with N counting from 1; a missing or empty file prints nothing.

Nothing is cached between runs. Every invocation opens the file afresh, which is what makes notes survive closing the terminal.

Tests live in `tests/test_notes.py` and run the script as a subprocess inside a temporary directory, then check the contents of `notes.txt` and the process output. An empty `tests/__init__.py` lets `python3 -m unittest` discover them from the project root.

## Decisions

### Decision: One Python 3 script, standard library only
- Chosen: a single executable script named `notes` (no `.py` extension, `#!/usr/bin/env python3` shebang), using only the Python standard library; tests in `tests/test_notes.py`, run by `python3 -m unittest`.
- Alternatives considered: a shell script; a Python package with a console-script entry point installed through `pip`.
- Why: this is the project's stated technology choice. A single file is enough for two subcommands, needs no install step, and the standard library covers argument handling, file I/O and tests.
- Requirements affected: REQ-001-01, REQ-001-02, REQ-001-03

### Decision: Storage is one note per line in UTF-8 plain text
- Chosen: `notes.txt` in the current directory, UTF-8, one note per line, each line terminated by `\n`.
- Alternatives considered: JSON file; SQLite database.
- Why: the spec constrains storage to plain text in `notes.txt`, one note per line. Plain text can be read and edited with any editor, and line-per-note makes `wc -l` and the success criteria trivially checkable.
- Requirements affected: REQ-001-01, REQ-001-02, REQ-001-03

### Decision: List output is `N. text`, and an empty list prints nothing
- Chosen: each note printed as its 1-based number, a dot, a space and the text, for example `1. Buy milk`. When there is no `notes.txt` or it is empty, `list` prints nothing and exits 0.
- Alternatives considered: `N) text`; `[N] text`; right-aligned numbers; a "No notes yet" message for the empty case.
- Why: the spec asks for "a number in front" and the dot form is how people number lists by hand. Printing nothing for an empty list keeps the output pipe-friendly and avoids a message that would look like a note.
- Requirements affected: REQ-001-02

### Decision: `add` refuses text that cannot be one line
- Chosen: `notes add` with empty text, or text containing a newline, writes nothing, prints an error to stderr and exits with status 1.
- Alternatives considered: replace newlines with spaces; write the text as-is and let the note span lines.
- Why: the spec constraint says one note per line. Writing a multi-line text would break that for every later `list`; silently rewriting the text would store something other than what the user typed. Refusing is the only option that keeps both the invariant and the user's words.
- Requirements affected: REQ-001-01

### Decision: Arguments after `add` are joined with single spaces
- Chosen: `notes add buy milk` and `notes add "buy milk"` both store `buy milk`.
- Alternatives considered: accept exactly one argument and treat more as a usage error.
- Why: forgetting the quotes is the most common slip at a shell prompt, and joining with spaces gives the result the user meant. The quoted form from the spec behaves identically.
- Requirements affected: REQ-001-01

### Decision: Tests drive the script as a subprocess
- Chosen: tests call `subprocess.run([sys.executable, <path to notes>, ...], cwd=<temporary directory>)` and inspect `notes.txt`, stdout, stderr and the exit status.
- Alternatives considered: load the script as a module with `importlib` and call `main()` directly.
- Why: the script has no `.py` extension, so importing it needs extra machinery. Running it the way a user does also proves REQ-001-03 directly, since every test step is a separate process with no shared memory.
- Requirements affected: REQ-001-01, REQ-001-02, REQ-001-03

### Decision: Unknown or missing subcommand prints usage and exits 2
- Chosen: `notes` with no arguments, or with a subcommand other than `add` or `list`, prints `usage: notes add <text> | notes list` to stderr and exits with status 2.
- Alternatives considered: treat a bare `notes` as `notes list`; print nothing and exit 0.
- Why: a tool should say how to use it when it is called wrongly. This is not written as a requirement because the approved spec does not ask for it; it is the minimum any command-line tool needs and it adds no behaviour the spec rules out.
- Requirements affected: none directly; keeps REQ-001-01 and REQ-001-02 from being triggered by mistyped commands.

## Interfaces and data

Command line, as seen by the user:

| Invocation | Effect | Exit status |
|---|---|---|
| `notes add <text...>` | Appends the text, joined with single spaces, as one line to `./notes.txt` | 0, or 1 if the text is empty or contains a newline |
| `notes list` | Prints each line of `./notes.txt` as `N. text`, counting from 1 | 0 |
| anything else | Prints a usage line to stderr | 2 |

File `notes.txt`, in the current working directory of the process:

- UTF-8 plain text, one note per line, each line terminated by `\n`.
- Created by `add` on first use. Never created by `list`.
- Read in full by `list` on every run. A missing file means no notes.

Tests:

- `tests/__init__.py`, empty, so that `python3 -m unittest` run from the project root discovers the `tests` package.
- `tests/test_notes.py`, with a helper that runs the script in a fresh temporary directory. Each test names the requirement IDs it covers in its docstring or name.

No existing interface or data is altered; everything above is new.

## Risks

- A hand-edited `notes.txt` whose last line has no trailing newline would make the next `add` glue its text onto that line. We would notice because `list` shows two notes merged into one. Mitigation: before appending, if the file is non-empty and does not end with `\n`, write a `\n` first.
- `notes.txt` is relative to the current directory, so running `notes list` from another directory shows a different, possibly empty, list. This is what the spec asks for. Mitigation: the README states it plainly.
- A hand-edited `notes.txt` containing bytes that are not valid UTF-8 would make `list` fail with a decoding error. Mitigation: open the file with `errors="replace"` so `list` always prints something for every line.
- Two terminals running `notes add` at the same moment could interleave. Each add is a single short append, which local filesystems treat as one write in practice, and locking is out of scope for this change.

## Open questions

None. The questions that came up while planning, which are the list output format, what `list` prints when there are no notes, what `add` does with text containing a newline, and whether `add` takes one argument or several, are answered under Decisions.
