# 001: Design

## Approach

The method is delivered as files, not software. Templates give every change the same shape. A one-page constitution and a generated index keep the context small. The lifecycle is a set of gates expressed as checklists, so it can be followed by hand on day one and enforced by skills and a validator later without changing the files.

This change was authored in one pass, with design and tasks written alongside the spec. That violates REQ-001-19. It is a deliberate bootstrap exception: the process it defines did not exist yet. Every later change follows the gates.

## Decisions

### Decision: Changes plus living capabilities, merged on archive
- Chosen: numbered change directories feed living capability specs through a mandatory archive step.
- Alternatives considered: change specs only, as spec-kit and Kiro do; capability specs only.
- Why: change-only models drift the moment code ships, and capability-only models have nowhere to put a unit of work. OpenSpec proves the merge model works, and its users show the merge must be mandatory or it is skipped.
- Requirements affected: REQ-001-11, REQ-001-21

### Decision: Requirements in one file, grouped by capability
- Chosen: `requirements.md` holds all requirements of a change under `## Capability:` headings. The archive step derives the per-capability merge from those headings.
- Alternatives considered: one delta file per capability inside the change, as OpenSpec does.
- Why: one file is easier to write and review, and the user of this method asked for a requirements file. The cost is that path-based code ownership cannot see which capabilities a change touches at Gate 1, so the frontmatter list carries that, and a small CI check can request reviewers from it. Path-based ownership still protects the capability specs themselves at Gate 3.
- Requirements affected: REQ-001-09, REQ-001-17

### Decision: Modified requirements keep their ID
- Chosen: modification keeps the ID and adds a "Changed in" line. Only additions mint new IDs.
- Alternatives considered: every modification mints a new ID that supersedes the old one.
- Why: tests, commits and tickets cite requirement IDs. Renumbering on every change breaks those references. History is preserved in the archive and the capability's History section.
- Requirements affected: REQ-001-10

### Decision: Configuration lives in the constitution frontmatter
- Chosen: three keys, `extends`, `numbering`, `sdd_version`, in `constitution.md`.
- Alternatives considered: a separate config file at the repository root or inside `specs/`.
- Why: one fewer file to teach, and the constitution is already the one file every reader and agent loads. The location of `specs/` is fixed, so the configuration does not need to be found before the specs are.
- Requirements affected: REQ-001-13

### Decision: Five states, three gates
- Chosen: draft, approved, in-progress, done, archived, with gates at approval, done and archive.
- Alternatives considered: a proposed state between draft and approved; a verified state between done and archived.
- Why: five states fit on a card and three gates fit in a sentence. Review happens inside Gate 1 and verification inside Gate 2, so the extra states add vocabulary without adding control.
- Requirements affected: REQ-001-16, REQ-001-17, REQ-001-20, REQ-001-21

### Decision: Minimal audit fields
- Chosen: `approved_by` and `approved_at` in the change frontmatter, set at Gate 1.
- Alternatives considered: a signed approval record per gate; relying on pull request history alone.
- Why: the stated need is who approved and when. Pull request history has it, but platforms differ and histories get squashed. Two fields are cheap now and painful to add later.
- Requirements affected: REQ-001-07, REQ-001-17

### Decision: Optional, generic external links
- Chosen: `ticket` and `docs` in frontmatter, `Ref:` on requirements, all optional, all plain links.
- Alternatives considered: tracker-specific fields; two-way status sync with the tracker.
- Why: the method must work in organisations with any tracker or none. The rule of truth in the method document prevents duplication: the spec holds intent, the tracker holds schedule, the wiki holds background.
- Requirements affected: REQ-001-12

## Interfaces and data

- Frontmatter schemas for change, capability and constitution, as shown in `specs/templates/`.
- Requirement block grammar: heading `### REQ-NNN-xx: Title`, one SHALL sentence, optional `Ref:`, one or more `#### Scenario:` blocks with GIVEN, WHEN, THEN bullets.
- Index table columns, as shown in `specs/INDEX.md`.

## Risks

- Teams skip the archive step and capabilities go stale. Mitigation: the archive skill does the merge, the validator refuses archived status with unmerged requirements, and the index shows done-but-not-archived changes.
- Constitutions grow past one page. Mitigation: the validator warns on length, and the method document says why it matters.
- Claim rule is forgotten and numbers collide. Mitigation: the validator flags duplicates, and the renumber rule is mechanical.

## Open questions

None. Questions about skills, validator and role guides belong to later changes.
