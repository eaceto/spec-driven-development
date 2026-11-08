# 007: Design

## Approach

Four small, independent fixes and one evidence task, each with its test. The example is a copy of the tutorial scratch project minus the installed skills. The version field is removed everywhere it is read: skill frontmatter, the validator's skills rule, the build hook, the skills README and the tests. The coverage search drops comment-only lines before searching for ids. The frontmatter parser recognises a dash-item line following a key with an empty value and reports it. Ticket numbering is a second directory pattern enabled by the constitution's `numbering` key, which the validator already reads for other reasons.

## Decisions

### Decision: Comment lines are excluded by shape, not by language
- Chosen: a line whose first non-blank characters are `#`, `//`, `/*`, `*`, `--` or `<!--` is a comment line for coverage purposes.
- Alternatives considered: parsing each language; counting ids only inside functions named test.
- Why: the method is language-neutral and the validator has no parsers. The shapes above cover the comment syntax of every mainstream language; docstrings remain counted, which is acceptable because a docstring sits inside a test.
- Requirements affected: REQ-003-13

### Decision: Ticket keys are `[A-Z][A-Z0-9]+-[0-9]+`
- Chosen: one pattern, upper-case project key, dash, digits, matching Jira, Linear and most trackers.
- Alternatives considered: a configurable regular expression in the constitution.
- Why: one pattern keeps the configuration at its three keys. A tracker with another shape is a later variant with evidence of need.
- Requirements affected: REQ-007-03, REQ-001-02

### Decision: The example keeps no git history
- Chosen: copy the working tree, as for the Go example, and tell the history on the page.
- Why: consistency with the first example, and the transcripts already show the commits.
- Requirements affected: REQ-007-01

### Decision: Domain grouping is removed, not deferred in place
- Chosen: delete the variant paragraph from the method; a future change adds it back with its validator support if asked for.
- Why: a documented variant the tool rejects is a broken promise; a removed one is an honest absence.
- Requirements affected: none; method text only

## Interfaces and data

- Constitution `numbering: ticket` enables `CHANGE_DIR_TICKET_RE`; the change's `num` becomes the key, and the index, claim and trailer rules use it unchanged.
- Hook and tests stop reading `metadata.version`.
- `tests/manual/skills-runs.md` gains observed rows for the five refusal paths.

## Risks

- Adopters on ticket numbering lose the ordering the sequential prefix gives; the index sorts by key. Accepted.
- Removing `version` from skills already installed elsewhere is harmless: nothing reads it.

## Open questions

None.
