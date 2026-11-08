# notes

A small command-line tool that keeps short notes in a plain text file.

## Usage

Add a note:

    ./notes add "Buy milk"

List the notes, numbered from 1:

    ./notes list
    1. Buy milk

Notes live in `notes.txt` in the current directory, one note per line.
Running `notes` from another directory uses that directory's `notes.txt`,
so change into the directory where you keep your notes first.

## Tests

From the project root:

    python3 -m unittest
