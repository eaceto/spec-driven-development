---
id: "009"
title: Site improvements from the first review
status: archived
tier: standard
owner: maintainers
capabilities: [website]
ticket:
docs:
approved_by: Ezequiel Aceto
approved_at: 2026-11-08
created: 2026-11-08
updated: 2026-11-08
---

# 009: Site improvements from the first review

## Why it matters

A review of the live site as a first-time visitor found that the first screen assumes the reader knows what an agent is, gives no reason to adopt the method before the button, and names no prerequisites or realistic time. The tutorial uses the word gate before explaining it, repeats an unfinished-looking note six times, reproduces whole files where a transcript should be the spine, and never shows the one thing that teaches gates best: a refusal. An evaluator finds no page on adopting an existing codebase and no answers to the questions people actually ask. And the site names three other products and judges them, which the owner does not want.

## What should be done

The home page defines agents in its first paragraph, gives the reason to adopt in three sentences above the call to action, and states prerequisites and a realistic total time beside it. The tutorial overview carries a one-line glossary of the vocabulary the steps use and one note on Devin; the step tabs say only that the request is the same. Step 3 shows the recorded refusal of planning a draft. Long reproductions on steps 3 and 4 collapse into expandable blocks. A footnote explains the "checked by reading" lines once. Two new pages: adopting an existing project, built from the recorded brownfield run; and questions people ask, answered in a few sentences each with links into the method. Every mention of other products disappears from the site and the README, replaced by one sentence that names nobody. The skills pages open with what to say to the agent. The validator rules table links requirement ids to their capability specs. The method page gets an on-this-page list. Example pages carry no hard-coded validator counts. The site has a logo icon and a favicon.

## Scope

### In

- Home, tutorial overview and steps, two new pages, what-and-why, method, README, example pages, build hook, theme configuration, tests

### Out

- Re-capturing transcripts with the validator installed. A footnote explains the lines.
- A comparison with other products, in any form.
- A brownfield example project. The adoption page uses the recorded run.
- Translation, custom domain, analytics.

## Success criteria

- No page on the site, and not the README, names spec-kit, Kiro or OpenSpec; a test enforces it.
- A first-time visitor reading only the home page learns what an agent is, why to adopt, what to install and how long it takes.
- Tutorial steps stay under 700 words of prose outside collapsed blocks, and step 3 contains a verbatim refusal.
- The adoption and questions pages exist, are in the navigation, and read in under five minutes each.
- Strict build, validator and suite green.
