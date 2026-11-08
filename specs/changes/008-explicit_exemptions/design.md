# 008: Design

## Approach

The requirements parser records two sets from the Not testable section: ids that start a bullet with trailing text, which are exempt, and every other id found in the section, which a new rule reports. The status-done rule uses only the first set. Three sentences land in three skills.

## Decisions

### Decision: Exempt means own bullet, id first, then a reason
- Chosen: a line matching `- REQ-…` followed by at least one word.
- Alternatives considered: any bullet mentioning the id; a frontmatter list of exemptions.
- Why: one visible shape a reviewer can scan, and no new field. The existing archives already use it.
- Requirements affected: REQ-008-01, REQ-003-13

## Interfaces and data

- `Change.not_testable_ids`: exempt ids only. New `Change.not_testable_mentions`: the rest.
- Rule `exemption-form`, REQ-008-01, change-scoped.

## Risks

- An archived change with an id in prose under Not testable would now fail. Checked: none in this repository does, after 007's note was reworded.

## Open questions

None.
