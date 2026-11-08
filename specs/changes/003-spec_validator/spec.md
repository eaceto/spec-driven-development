---
id: "003"
title: Spec validator
status: done
tier: standard
owner: maintainers
capabilities: [validator, spec-layout]
ticket:
docs:
approved_by: Ezequiel Aceto
approved_at: 2026-11-08
created: 2026-11-08
updated: 2026-11-08
---

# 003: Spec validator

## Why it matters

The method has rules that are mechanical: a directory is named correctly or it is not, a requirement has a scenario or it does not, a change marked archived has its requirements in a capability or it does not. Today nothing checks them. People check by reading, agents check by reading, and both get tired and skip. That is how every existing spec-driven tool loses its users: the rules exist, nobody enforces them, specs drift, and within months the folder describes a system that no longer exists.

The cost falls on three groups. Teams discover drift late, when a spec contradicts the code in a review nobody can resolve. Agents spend judgement on structure instead of on the work, and they improvise when a file is malformed. Changes 001 and 002 of this repository cannot pass Gate 2, because their requirements are structural and have no tests until something executes them.

## What should be done

Provide one validator: a single Python 3 file with no dependencies beyond the standard library, installed into a project at `specs/validate.py` and run as `python3 specs/validate.py` through the constitution's `validator` key, which the install step sets. Run with no arguments it checks the whole `specs/` tree and exits non-zero on any violation, reporting each violation with the file, the rule and the requirement ID the rule comes from. Run with a change number it checks that change alone.

It checks what change 001 fixed: layout, change naming and numbering, tier and required files, the fixed order of `spec.md`, frontmatter fields, requirement grammar and IDs, grouping by capability, status values and forward-only transitions, unmerged requirements on archived changes, and whether the index matches the file system. In this repository it also checks what change 002 fixed for skills: line limits, section order, frontmatter and vendor-neutral bodies.

Allowing `specs/validate.py` means `specs/` has seven entries, not six. This change amends REQ-001-01 accordingly, through the modified-requirement flow, and is archived after change 001 so the amendment lands on the `spec-layout` capability.

## Scope

### In

- `specs/validate.py`: the validator, standard library only, readable in one sitting
- Checks for every structural requirement of change 001, each reporting the requirement ID it enforces
- Checks for the structural requirements of change 002 when a `skills/` directory is present
- Whole-tree and single-change modes, non-zero exit on violations, human-readable report
- Installation by `install.sh`, which also sets the `validator` key in the constitution
- Amendment of REQ-001-01 to allow `specs/validate.py`
- Tests for the validator itself, so that the tests of change 001 are the validator's own tests

### Out

- Judgement checks: whether a purpose is well written, whether a scenario is meaningful, whether a design decision is sound. Those remain with people and skills.
- Fixing violations automatically.
- Continuous integration workflow files for specific platforms. A later change documents them.
- Checking code or tests of the project beyond searching them for requirement IDs.
- Validating the organisation constitution hierarchy across repositories.

## Success criteria

- Running the validator on this repository after the amendment reports zero violations.
- Every structural requirement of change 001 is referenced by at least one check, and every check names the requirement it enforces in its output.
- Introducing any one of these faults makes the validator exit non-zero and name the file: a misnamed change directory, a duplicate number, a missing required file for the tier, a requirement without a scenario, a capability section absent from the frontmatter, a status set to archived with requirements not in any capability, an index row that disagrees with a frontmatter.
- Running on the trial project at the current state reports zero violations, or only violations that are genuine.
- The file runs on Python 3.9 or later with no installation step beyond copying it.

## Constraints specific to this change

- Standard library only. No build step, no package, no configuration file.
- Scenario bullets may include AND lines after GIVEN, WHEN or THEN, since real scenarios need them.
- Rules are data: each check is listed once with its requirement ID, so adding a rule means adding one entry, not restructuring the file.
