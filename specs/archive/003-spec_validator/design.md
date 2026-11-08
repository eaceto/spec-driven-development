# 003: Design

## Approach

One Python file, read top to bottom in one sitting. It parses the `specs/` tree into plain data: the constitution, the index, every change with its frontmatter and files, every capability with its requirement blocks. A registry of rules then runs over that data. Each rule is a small function that yields violations and is registered once with an id, the requirement ids it enforces and a one-line description. The command line, the report and the exit code wrap the registry and nothing else.

The skills gain a `validator` key to call. Where a skill today says "check by reading", the validator does the same check mechanically and names the requirement it enforces, so a person reading the report learns the method while fixing the file.

## Decisions

### Decision: Rules as a registry, not a procedure
- Chosen: a list of rule records, each with id, requirement ids, description and check function. `--rules` prints the list. Coverage of change 001 is a property of the list, checked by a test.
- Alternatives considered: one long validate function; one module per rule.
- Why: adding a rule is adding one entry. The listing doubles as documentation and as the proof for Gate 2 that every structural requirement has a check. One file keeps installation to a copy.
- Requirements affected: REQ-003-04, REQ-003-19

### Decision: Minimal frontmatter parser instead of a YAML library
- Chosen: parse `key: value`, `key: [a, b]` and quoted strings; nothing else.
- Alternatives considered: PyYAML as a dependency; frontmatter as JSON.
- Why: the templates use only that subset, and a dependency would turn "copy one file" into "install a package" on every machine and CI image. Anything the parser does not understand is itself a violation, which keeps frontmatter simple.
- Requirements affected: REQ-003-01, REQ-003-09

### Decision: Test coverage means the id appears in a test file
- Chosen: a requirement counts as tested when its id appears in a file outside `specs/` whose path contains `test`, case-insensitive.
- Alternatives considered: parsing test frameworks; a coverage manifest maintained by hand.
- Why: it works for every language and framework, costs nothing to adopt, and matches what `sdd-implement` already asks for. It is a floor, not a proof. The gate is honest about that: the rule says "referenced", not "verified".
- Requirements affected: REQ-003-13

### Decision: Git checks are best effort
- Chosen: when `git` is on the path and the project is a repository, check backward status moves against `HEAD` and trailers on the last ten commits. Otherwise skip and say so in the summary.
- Alternatives considered: always require git; a separate command for git checks.
- Why: forward-only transitions and trailers are requirements of change 001, and git is where the evidence is. Making the whole validator depend on git would break it in archives and tarballs.
- Requirements affected: REQ-003-13, REQ-003-16

### Decision: Constitution length limit is eighty lines
- Chosen: a violation above eighty lines.
- Alternatives considered: no limit; a word count; a warning only.
- Why: "fits on one page" needs a number to be checkable. Eighty lines is a printed page in Markdown and twice this repository's own constitution. A warning would be ignored, which is the failure the method exists to prevent.
- Requirements affected: REQ-003-15

### Decision: The validator lives in `specs/` and amends REQ-001-01
- Chosen: `specs/validate.py`, with the layout requirement amended through the modified-requirement flow rather than an edit to change 001.
- Alternatives considered: a `tools/` folder at the project root; shipping the validator inside a skill directory.
- Why: it belongs with the specs it checks, and a root folder would collide with conventions in adopting projects. Using the modified-requirement flow exercises the archive merge on a real amendment before anyone else relies on it. It fixes the order of archiving: 001 first, then 003.
- Requirements affected: REQ-003-05, REQ-001-01

### Decision: Tests build fixtures from the templates
- Chosen: tests generate a minimal valid project in a temporary directory from `specs/templates/`, then break one thing per test.
- Alternatives considered: checked-in fixture trees; testing against this repository only.
- Why: fixtures built from the templates fail when the templates and the validator drift apart, which is exactly the failure to catch. One broken thing per test keeps failures readable.
- Requirements affected: REQ-003-19

## Interfaces and data

- Command: `python3 specs/validate.py [NNN] [--rules] [--root DIR]`. Exit 0, 1 or 2.
- Violation line: `<path>: <rule-id> (<REQ-ids>): <message>`. Summary line: `<n> violations, <files> files, <rules> rules` plus `git checks skipped` when applicable.
- Constitution frontmatter key: `validator: python3 specs/validate.py`, written by `install.sh`.
- Internal records: `Change(dir, id, frontmatter, files, requirements, modified, removed, not_testable)`, `Capability(dir, id, frontmatter, requirements, retired)`, `Rule(id, reqs, description, check)`.
- Test layout: `tests/test_validate.py`, standard `unittest`, fixtures in `tempfile` directories.

## Risks

- The validator and the skills disagree on a rule. Mitigation: the skills say "check by reading" for the same rules the validator names by requirement id, and the method document is the shared source. The test that lists rules against change 001 catches a missing rule.
- Adopters find the checks too strict for a brownfield start. Mitigation: a capability map of purpose-only specs passes, and a change in draft with only `spec.md` passes. Strictness arrives with status, not with existence.
- Line and count limits become bikeshedding. Mitigation: each limit is one constant at the top of the file with the requirement it serves.

## Open questions

None.
