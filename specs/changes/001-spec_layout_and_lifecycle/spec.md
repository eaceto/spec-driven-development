---
id: "001"
title: Spec layout and lifecycle
status: draft
tier: standard
owner: maintainers
capabilities: [spec-layout, lifecycle]
ticket:
docs:
approved_by:
approved_at:
created: 2026-11-08
updated: 2026-11-08
---

# 001: Spec layout and lifecycle

## Why it matters

Teams that adopt spec-driven development with today's tools stop within months. The reasons repeat across GitHub's spec-kit, Amazon's Kiro and OpenSpec: specs go stale because nothing updates them after the code ships, the folder becomes unreadable past a few dozen entries, small changes carry the same ceremony as large ones, and nobody can say who approved what. The specs then describe a system that no longer exists, and people go back to writing code first.

If the layout and lifecycle are not right from the first commit, every skill, template and guide built on top inherits the problem. This change comes first because everything else depends on it.

## What should be done

Define the one structure every project using this method follows: where specs live, how a change is named, which files it contains at each tier, how requirements are written and identified, which states a change passes through, what each gate requires, how finished changes become living capability specs, how ownership and approval work, and how a reader or an agent finds the one spec they need without loading everything.

Deliver it as templates, a reference document, the constitution of this repository, and this change itself as the first worked example.

## Scope

### In

- Directory layout under `specs/`
- Change directory naming and the claim rule for teams
- Tiers and the files each tier requires
- The fixed order of `spec.md`
- Requirement notation and ID rules
- States, gates and what the archive step does
- Capability spec structure and ownership
- Optional links to a ticket system and a document system
- Constitution structure and hierarchy across an organisation
- Index content and the loading rule for people and agents
- Cross-repository identity
- Commit and pull request traceability

### Out

- The skills that automate the lifecycle. They are the next change.
- The validator that enforces the rules. A later change.
- Role-based guides for developers, leads and product owners. A later change.
- The aggregated index across repositories. A later change.
- Any integration with a specific tracker, wiki or agent product.

## Success criteria

- A developer who has never seen the method can create a correct change directory from the templates in under fifteen minutes using only `docs/method.md`.
- Every rule in `docs/method.md` is stated in one sentence and backed by a requirement in this change.
- This repository's own `specs/` folder follows the layout, and this change passes its own checklist.
- An agent given `AGENTS.md` loads the constitution, the index and one change, and nothing else, when asked to work on that change.

## Constraints specific to this change

- No rule may require a specific vendor. Jira, Confluence, Devin and Claude Code appear only as examples.
- No template may exceed one screen of guidance comments. Templates teach by shape, not by essay.
