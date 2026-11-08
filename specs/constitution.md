---
extends: none
version: 1.0.0
owner: maintainers
numbering: sequential
sdd_version: 0.1.0
validator: python3 specs/validate.py
---

# Constitution

## Purpose

This repository teaches and equips spec-driven development. Everything in it exists so that a developer, a team or an organisation can adopt the method in an afternoon and still be using it a year later.

## Principles

Each principle is a rule we can state in one sentence, followed by why it exists.

1. **Purpose before mechanism.** Every spec opens with why it matters and what should be done, before any how. A spec whose purpose cannot be stated is not ready.
2. **One structure.** Where a rule will do, we do not offer an option. Options are the tax every new reader pays.
3. **Teachable in a sentence.** A rule we cannot state in one sentence is cut or split. If the method needs a workshop, it has failed.
4. **Tool-agnostic.** Specs are plain Markdown. Nothing in the method may require a specific vendor, tracker, wiki or agent. Vendors appear only in examples.
5. **The lifecycle is enforced, not remembered.** Status changes happen through gates and skills, never by editing a field by hand. The archive step merges requirements into capabilities; a human does not.
6. **Small context.** A constitution fits on one page. An agent or a person loads the constitution, the index and one change. Never everything.
7. **We eat our own cooking.** Every change to this repository goes through its own spec, in this repository's `specs/` folder.
8. **Variants are visible and optional.** A documented variant is marked as such and is never the default path.

## Definitions

- **Change**: a numbered unit of work under `specs/changes/`. It has a purpose, requirements, a design, tasks and a checklist.
- **Capability**: a living description of how the system behaves today, under `specs/capabilities/`. It is updated only by archiving changes.
- **Requirement**: one SHALL statement with at least one scenario and a stable ID.
- **Gate**: a condition that must hold before a change moves to the next status.
- **Owner**: the team accountable for a capability or a change.

## Amendments

Changes to this constitution are made through a change spec that lists `constitution` among its capabilities and are reviewed by the owner above.

| Version | Date | Change | Summary |
|---|---|---|---|
| 1.0.0 | 2026-11-08 | 001 | Initial constitution |
