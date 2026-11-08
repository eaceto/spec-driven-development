"""Tests for the notes script (change 001).

The script is run as a subprocess inside a fresh temporary directory, as
design.md decides, so every test step is a separate process with its own
notes.txt. Each test names the requirement IDs it covers in its name or in
its docstring.
"""

import os
import pathlib
import subprocess
import sys
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parent.parent / "notes"


def run_notes(cwd, *args):
    """Run the notes script with the given arguments inside cwd.

    Returns the CompletedProcess with stdout and stderr captured as text.
    """
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=cwd,
        capture_output=True,
        text=True,
    )


class NotesTestCase(unittest.TestCase):
    """Base class: a fresh temporary directory per test."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.dir = pathlib.Path(self._tmp.name)
        self.notes_file = self.dir / "notes.txt"

    def notes(self, *args):
        return run_notes(self.dir, *args)


class ScriptSetupTests(NotesTestCase):
    """Setup task T01, no requirement ID.

    Checks the scaffold itself: the script is executable, has a python3
    shebang, and a missing or unknown subcommand prints usage to stderr
    and exits 2 (design.md, "Unknown or missing subcommand prints usage
    and exits 2").
    """

    def test_script_is_executable_with_python3_shebang(self):
        self.assertTrue(os.access(SCRIPT, os.X_OK), f"{SCRIPT} is not executable")
        with open(SCRIPT, encoding="utf-8") as f:
            self.assertEqual(f.readline().rstrip("\n"), "#!/usr/bin/env python3")

    def test_no_subcommand_prints_usage_and_exits_2(self):
        result = self.notes()
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("usage: notes add <text> | notes list", result.stderr)

    def test_unknown_subcommand_prints_usage_and_exits_2(self):
        result = self.notes("frobnicate")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("usage: notes add <text> | notes list", result.stderr)


class AddNoteTests(NotesTestCase):
    """REQ-001-01: Add a note.

    `notes add <text>` appends one line containing exactly the text to
    notes.txt in the current directory, creating the file if it does not
    exist, and refuses text that cannot be one line.
    """

    def test_req_001_01_append_to_existing_notes_adds_one_line(self):
        self.notes_file.write_text("Call the dentist\nRead chapter 4\n", encoding="utf-8")
        result = self.notes("add", "Buy milk")
        self.assertEqual(result.returncode, 0)
        lines = self.notes_file.read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(lines), 3)
        self.assertEqual(lines[-1], "Buy milk")

    def test_req_001_01_first_note_creates_the_file(self):
        self.assertFalse(self.notes_file.exists())
        result = self.notes("add", "Buy milk")
        self.assertEqual(result.returncode, 0)
        self.assertTrue(self.notes_file.exists())
        self.assertEqual(self.notes_file.read_text(encoding="utf-8"), "Buy milk\n")

    def test_req_001_01_text_with_newline_is_refused_and_file_unchanged(self):
        before = "Call the dentist\nRead chapter 4\n"
        self.notes_file.write_text(before, encoding="utf-8")
        result = self.notes("add", "Buy milk\nand eggs")
        self.assertNotEqual(result.returncode, 0)
        self.assertNotEqual(result.stderr, "")
        self.assertEqual(self.notes_file.read_text(encoding="utf-8"), before)

    def test_req_001_01_empty_text_is_refused_and_nothing_written(self):
        # design.md: "`add` refuses text that cannot be one line"
        result = self.notes("add")
        self.assertEqual(result.returncode, 1)
        self.assertNotEqual(result.stderr, "")
        self.assertFalse(self.notes_file.exists())

    def test_req_001_01_arguments_are_joined_with_single_spaces(self):
        # design.md: "Arguments after `add` are joined with single spaces"
        result = self.notes("add", "Buy", "milk")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(self.notes_file.read_text(encoding="utf-8"), "Buy milk\n")

    def test_req_001_01_missing_trailing_newline_is_repaired_before_append(self):
        # design.md risk: a hand-edited file whose last line has no newline
        self.notes_file.write_text("Call the dentist", encoding="utf-8")
        result = self.notes("add", "Buy milk")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(
            self.notes_file.read_text(encoding="utf-8"),
            "Call the dentist\nBuy milk\n",
        )


class ListNotesTests(NotesTestCase):
    """REQ-001-02: List notes with numbers.

    `notes list` prints every line of notes.txt in the current directory
    to stdout, in file order, each prefixed with its 1-based position in
    the form `N. text`. A missing or empty file prints nothing.
    """

    def test_req_001_02_three_saved_notes_are_numbered_in_file_order(self):
        self.notes_file.write_text(
            "Buy milk\nCall the dentist\nRead chapter 4\n", encoding="utf-8"
        )
        result = self.notes("list")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(
            result.stdout, "1. Buy milk\n2. Call the dentist\n3. Read chapter 4\n"
        )
        self.assertEqual(result.stderr, "")

    def test_req_001_02_missing_file_prints_nothing_and_exits_0(self):
        self.assertFalse(self.notes_file.exists())
        result = self.notes("list")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertFalse(self.notes_file.exists(), "list must never create notes.txt")

    def test_req_001_02_empty_file_prints_nothing_and_exits_0(self):
        self.notes_file.write_text("", encoding="utf-8")
        result = self.notes("list")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")

    def test_req_001_02_invalid_utf8_still_lists_every_line(self):
        # design.md risk: a hand-edited file with bytes that are not UTF-8
        self.notes_file.write_bytes(b"Buy milk\nCaf\xe9\nRead chapter 4\n")
        result = self.notes("list")
        self.assertEqual(result.returncode, 0)
        lines = result.stdout.splitlines()
        self.assertEqual(len(lines), 3)
        self.assertEqual(lines[0], "1. Buy milk")
        self.assertTrue(lines[1].startswith("2. Caf"))
        self.assertEqual(lines[2], "3. Read chapter 4")


class PersistenceTests(NotesTestCase):
    """REQ-001-03: Notes persist between runs.

    Every added note stays in notes.txt in the current directory, so a
    later, separate run of `notes list` in the same directory prints it.
    Each call to self.notes() is its own process, so nothing can survive
    in memory between the add and the list.
    """

    def test_req_001_03_note_added_in_one_run_is_listed_in_the_next(self):
        add = self.notes("add", "Buy milk")
        self.assertEqual(add.returncode, 0)
        # The add process has exited; a new process lists the same directory.
        result = self.notes("list")
        self.assertEqual(result.returncode, 0)
        self.assertIn("1. Buy milk", result.stdout.splitlines())

    def test_req_001_03_notes_accumulate_across_separate_runs(self):
        for text in ("Buy milk", "Call the dentist", "Read chapter 4"):
            self.assertEqual(self.notes("add", text).returncode, 0)
        result = self.notes("list")
        self.assertEqual(
            result.stdout, "1. Buy milk\n2. Call the dentist\n3. Read chapter 4\n"
        )


if __name__ == "__main__":
    unittest.main()
