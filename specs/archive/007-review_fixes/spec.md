---
id: "007"
title: Fixes from the 0.2.0 review
status: archived
tier: standard
owner: maintainers
capabilities: [website, skills, validator, spec-layout]
ticket:
docs:
approved_by: Ezequiel Aceto
approved_at: 2026-11-08
created: 2026-11-08
updated: 2026-11-08
---

# 007: Fixes from the 0.2.0 review

## Why it matters

The review at 0.2.0 found four things that text alone cannot fix. The tutorial's transcripts describe a project that exists only in a temporary folder on one machine; when that folder goes, the site points at nothing. The skills carry a `version` field that nothing reads and that drifted within a day. The coverage rule accepts a requirement id in a comment, so a green gate can mean less than it looks. And the method documents a ticket-numbering variant that the validator rejects, which is a promise the tool breaks. Enterprises with a tracker will meet that one first.

## What should be done

- Commit the tutorial's notes project as `examples/notes-python`, exactly as the skills produced it, with a narrative page like the Go example's, and link it from the tutorial.
- Remove `metadata.version` from the skills; `sdd_version` is the one number anyone reads. Amend the requirements that demand it and the validator rule that checks it.
- Make the coverage rule ignore ids that appear only on comment lines, and amend its requirement to say so.
- Make the validator report a block-style frontmatter list with a message naming the `[a, b]` form.
- Support `numbering: ticket`: a change directory may be `KEY-123-name_of_change` when the constitution says so, and the validator, the skills and the templates agree. Remove the domain-grouping variant from the method until someone needs it.
- Re-run the five refusal paths as fresh agent runs so that artefacts exist, and record them in the manual test log.

## Scope

### In

- `examples/notes-python` and its page; tutorial links to it
- Skill frontmatter, the skills README, the build hook and tests for the version field
- The validator's coverage search, the frontmatter parser diagnostic, ticket numbering in the dirname and id rules, with tests
- `sdd-new` and the method for ticket numbering; the method for the removed variant
- Fresh refusal-path runs recorded in `tests/manual/skills-runs.md`

### Out

- Devin transcripts. Still pending a Devin session.
- Domain grouping of capabilities. Removed from the document, not implemented.
- Any change to the lifecycle, the gates or the file set of a change.

## Success criteria

- `python3 specs/validate.py --root examples/notes-python` reports zero violations and the tutorial links to the folder.
- No skill carries `metadata.version`; the validator, hook and tests pass without it.
- A requirement id that appears only in a comment line of a test file does not count as covered, and the suite proves it.
- A `capabilities:` block list produces a violation that names the `[a, b]` form.
- With `numbering: ticket` in the constitution, a directory `ABC-123-name_of_change` passes the validator and `ABC-123` is its id; with `numbering: sequential` it is a violation.
- The five refusal paths have observed results in the manual test log.
