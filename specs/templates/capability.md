---
id: capability-id            # kebab-case, matches the folder name
title: Capability title
owner:                        # team accountable for this capability
updated: YYYY-MM-DD           # set by the archive step
---

# Capability title

## Purpose

<!-- Why this capability exists and who depends on it. Two to five sentences. Written once, rarely changed. -->

## Requirements

<!-- Only the archive step writes here. Requirements keep the ID they were born with.
     "Origin" is the change that introduced the requirement. "Changed in" lists later changes that modified it. -->

### REQ-NNN-01: Title
Origin: NNN

When <trigger>, the <subject> SHALL <behaviour>.

#### Scenario: Name
- GIVEN <precondition>
- WHEN <action>
- THEN <observable result>

## Retired

<!-- IDs are never reused. A removed requirement is listed here with the change that removed it and why. -->

- REQ-NNN-02, removed by change MMM: reason.

## History

<!-- One line per archived change that touched this capability. -->

- NNN (YYYY-MM-DD): change title
