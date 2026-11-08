# 002: Design

## Approach

Six skills, one per lifecycle step, each a self-contained `SKILL.md` in the open Agent Skills format. A skill is a procedure: when to use it, what must be true before it runs, numbered steps, when to refuse, and how to tell it is finished. The same text serves an agent and a person, which is how we keep the method teachable: reading the skills is reading the method.

Skills carry judgement and sequencing. Mechanical checks belong to the validator in change 003. Until it exists, each skill performs the handful of structural checks it depends on by reading files, so behaviour is identical with or without the validator and the validator only makes the checks faster and stricter.

Templates are not bundled with the skills. A skill reads `specs/templates/` from the project it runs in, which `sdd-init` copies there. One source of truth per project, and a project can adjust a template without forking a skill.

## Decisions

### Decision: Six skills, not nine
- Chosen: init, new, plan, implement, verify, archive.
- Alternatives considered: separate clarify, design and tasks skills as spec-kit has; a single `sdd` skill with sub-commands.
- Why: six names that are state transitions teach the lifecycle by themselves. Clarify is a step inside new, and design and tasks are steps inside plan because they are never done separately. A single skill with sub-commands hides the lifecycle and makes the description used for triggering too broad.
- Requirements affected: REQ-002-06, REQ-002-09, REQ-002-11

### Decision: Self-contained skills, templates from the project
- Chosen: each `SKILL.md` holds every rule it needs; templates are read from the project's `specs/templates/`.
- Alternatives considered: a shared reference file installed beside the skills; templates bundled inside each skill directory.
- Why: the Agent Skills format resolves files relative to the skill's own directory, so cross-skill references are not portable. Bundled templates would drift from the project's copy. `sdd-init` is the one exception: the install step bundles the templates into its installed copy, because it runs before the project has any. The cost is some repetition of frontmatter field lists across skills, bounded by the 150-line limit.
- Requirements affected: REQ-002-01, REQ-002-05

### Decision: Copy on install, not symlink
- Chosen: the install step copies skill directories into `.agents/skills/` and `.claude/skills/` and records the version in the constitution.
- Alternatives considered: symlinks to a single copy; a git submodule; a package manager.
- Why: symlinks fail on some Windows setups and in some CI checkouts. A submodule couples the project to this repository's history. Copying is dumb and works everywhere, and the version in the constitution is what makes an upgrade visible. The install step is a dependency-free shell script; third-party skill installers that follow the standard can be used instead.
- Requirements affected: REQ-002-04

### Decision: Gate 1 is the only manual transition
- Chosen: `sdd-new` sets draft, a person sets approved, `sdd-plan` sets in-progress, `sdd-verify` sets done, `sdd-archive` sets archived.
- Alternatives considered: a skill that performs approval; leaving all status edits to people.
- Why: approval is a human decision and the audit fields must name a person. Every other transition follows from work being complete, which a skill can check. This is the principle that the lifecycle is enforced, not remembered.
- Requirements affected: REQ-002-06, REQ-002-11, REQ-002-15, REQ-002-16

### Decision: One task per implement invocation
- Chosen: `sdd-implement` does the first unticked task and stops, unless asked to continue.
- Alternatives considered: run all tasks; run a phase.
- Why: one task is one reviewable commit with a `Requirements:` trailer, and the stop between tasks is where contradictions surface before they compound. Kiro's run-all mode exists, and its users report over-building; the opt-in continue keeps that choice with the person.
- Requirements affected: REQ-002-13, REQ-002-14

### Decision: Evidence for behavioural requirements lives in the checklist
- Chosen: recorded runs of each skill on Devin CLI and Claude Code are summarised as evidence lines under the Gate 2 items in this change's `checklist.md`.
- Alternatives considered: an `evidence/` folder in the change; a separate test report.
- Why: REQ-001-04 fixes the files a change may contain, and the checklist is already where Gate 2 is decided. Structural requirements are covered by the validator in 003; behavioural ones by recorded runs.
- Requirements affected: REQ-002-07 through REQ-002-18

## Interfaces and data

- `skills/<name>/SKILL.md` frontmatter: `name`, `description`, `metadata.version`, `metadata.sdd_version`.
- Body sections in order: When to use, Preconditions, Steps, Refuse when, Done when.
- `install.sh <target-project> [version]`: copies `skills/*` to both locations and sets `sdd_version` in `<target>/specs/constitution.md`.
- Validator hook: an optional `validator` key in the constitution frontmatter holds the command to run. Skills run it when present and report its output; absent means no validator. Change 003 sets the key when it installs the validator.

## Risks

- Skill bodies drift from the method document. Mitigation: 003's validator checks the structural rules in both; the method document is the human reference and the skills cite requirement IDs from 001 where they enforce one.
- Agents ignore the refuse conditions under pressure from a user. Mitigation: refusals are the first check in every Steps list and name the gate, so a person sees exactly what to do instead.
- The two-location install becomes three or four as agents are added. Mitigation: the install script holds the list in one place.

## Open questions

None. The validator's path and command are decided in change 003; the hook here is written to tolerate absence.
