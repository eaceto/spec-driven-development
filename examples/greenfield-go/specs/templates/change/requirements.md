# NNN: Requirements

<!-- This file is written for people and agents alike. Every requirement must be testable.
     Format: one SHALL statement per requirement, at least one scenario.
     IDs: REQ-NNN-xx where NNN is this change. IDs are never reused.
     Group requirements under the capability they belong to. -->

## Capability: capability-id

### REQ-NNN-01: Title
When <trigger>, the <subject> SHALL <behaviour>.
Ref: <!-- optional: ticket or document link for this one requirement -->

#### Scenario: Name
- GIVEN <precondition>
- WHEN <action>
- THEN <observable result>

### REQ-NNN-02: Title
The <subject> SHALL <behaviour>.

#### Scenario: Name
- GIVEN
- WHEN
- THEN

## Modified requirements

<!-- Existing requirements this change rewrites. Keep the original ID. Write the full new text.
     The archive step replaces the text in the capability spec and appends this change to "Changed in". -->

### REQ-MMM-03: Title
Changed in: NNN

When <trigger>, the <subject> SHALL <new behaviour>.

#### Scenario: Name
- GIVEN
- WHEN
- THEN

## Removed requirements

<!-- Existing requirements this change retires. The archive step moves them to the capability's Retired list. -->

- REQ-MMM-04: reason, and what replaces it if anything.

## Not testable

<!-- Rare. A requirement listed here is exempt from the test coverage gate, with the reason. -->
