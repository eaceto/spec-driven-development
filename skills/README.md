# Skills

Six skills, one per step of the lifecycle. Each is a directory holding a `SKILL.md` in the open Agent Skills format. The same text is read by agents and by people: following the Steps section by hand is doing the method.

| Skill | Acts when | Leaves the change |
|---|---|---|
| `sdd-init` | the project has no `specs/` | no change yet |
| `sdd-new` | someone describes work | draft |
| `sdd-plan` | status is approved | in-progress |
| `sdd-implement` | status is in-progress | in-progress, one more task ticked |
| `sdd-verify` | status is in-progress | done, or unchanged with a report |
| `sdd-archive` | status is done | archived, requirements merged into capabilities |

Gate 1, from draft to approved, is the only transition a person performs by hand.

## Format

- Frontmatter: `name` matching the directory, `description` saying what the skill does and when to use it, `metadata.version` and `metadata.sdd_version`.
- Body sections, in this order: When to use, Preconditions, Steps, Refuse when, Done when.
- Limit: 150 lines including frontmatter. A skill that needs more is doing two jobs.
- Vendor-neutral bodies: no tool-specific path, command or product name. Those belong in `install.sh` and `docs/method.md`.
- Templates: a skill reads `specs/templates/` from the project it runs in. `sdd-init` is the exception. The install step bundles the templates into its copy, so it can create that folder in a project that has none.
- Validator: when the constitution frontmatter has a `validator` key, a skill runs that command before reporting. Otherwise it performs the structural checks it depends on by reading the files, and says that no validator was found.

## Install

From a checkout of this repository, `./install.sh /path/to/project`. See the Agents section of `docs/method.md`.

## Writing or changing a skill

Every skill change goes through a change spec in `specs/changes/`, like everything else here. The requirements that define these skills live in change 002 until it is archived into the `skills` capability.
