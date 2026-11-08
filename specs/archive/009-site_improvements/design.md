# 009: Design

## Approach

Content edits in place, two new authored pages, three small hook changes, and theme keys. The hook gains a prompt per skill and an id-to-capability map read from `specs/capabilities/` at build time, so the links never go stale. Removing the product names is a search across docs and README with a test that keeps them out.

## Decisions

### Decision: Footnote, not re-capture
- Chosen: one admonition on step 2 explaining that the transcripts predate the validator install and what the lines would say today.
- Alternatives considered: re-running four agent sessions.
- Why: the owner's call; the runs remain exactly what happened.
- Requirements affected: REQ-009-02

### Decision: Collapsed blocks keep the files but shorten the read
- Chosen: `??? note` details blocks for reproduced files on steps 3 and 4.
- Why: the transcript is the lesson; the files are evidence for those who want them.
- Requirements affected: none beyond the word limit

### Decision: Favicon is a hand-written SVG
- Chosen: a small inline SVG in `docs/assets/favicon.svg`; the logo is a Material icon.
- Why: no design dependency, no binary file.
- Requirements affected: REQ-009-09

## Interfaces and data

- Hook: `SKILL_PROMPTS` dict; `capability_of(req_id)` built from `specs/capabilities/*/spec.md` headings; rules table cells become links to `https://github.com/eaceto/spec-driven-development/blob/main/specs/capabilities/<id>/spec.md`.
- New pages: `docs/adopting.md`, `docs/questions.md`.

## Risks

- Removing the origin paragraph loses credit to the ideas the method borrowed. Mitigation: one sentence says the method was shaped by studying existing tools, naming none.

## Open questions

None.
