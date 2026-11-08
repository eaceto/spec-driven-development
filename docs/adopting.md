# Adopting an existing project

Do not write specs for the whole codebase. Nobody will read them, nobody owns them, and they will be wrong within a month. Adopt from the edges: write the constitution from what already exists, map the capabilities with a purpose each and no requirements, then spec the next change you were going to make anyway.

## What `sdd-init` does on an existing codebase

This is what happened on 8 November 2026 when a fresh agent ran `sdd-init` on the tutorial's notes tool with its `specs/` folder removed: a Python script, its tests and a README, nothing else.

**Mode.** It found source code and a README, so it treated the folder as an existing project and asked one question, who owns the constitution.

**Constitution.** It read the README and derived three principles, each quoting the sentence it came from: notes live in `notes.txt` in the current directory, one per line; the tool acts on the current directory's file; tests run with `python3 -m unittest` from the project root. One definition: a note is one line of `notes.txt`. It invented nothing. A principle that cannot be traced to existing material is left out, and the skill says so.

**Capability map.** One capability, `notes`, from the single module, with a one-paragraph purpose and empty Requirements, Retired and History sections. Zero requirements, by rule. Requirements enter through changes, when someone touches that capability for a reason.

**Entry file.** `AGENTS.md` with the loading rule, so the next agent reads the constitution, the index and one change, and not the whole repository.

## What to do next

1. Read the constitution it wrote. Cut any principle you would not defend in a review. Add the ones your team repeats aloud but never wrote down.
2. Look at the capability map. Rename what is misnamed, add owners, merge or split where the modules lie about the domains. Still no requirements.
3. Start the next change with `sdd-new`. Its page records the as-is behaviour of the area it touches, and its requirements become the first ones in that capability when it archives.
4. Repeat. After a few changes, the capabilities people care about are specified, and the ones nobody touched are not, which is the right order.

## In a large organisation

Each repository adopts on its own schedule with its own constitution, extending the organisation's. A thin central repository holds the shared constitution, the pinned version of templates and skills, and an aggregated index. Cross-team work is a tracker epic with one change per repository. The [method](method.md#many-repositories) describes the layout.
