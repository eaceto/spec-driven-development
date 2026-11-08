---
id: "004"
title: Teaching site on GitHub Pages
status: done
tier: standard
owner: maintainers
capabilities: [website, ci]
ticket:
docs:
approved_by: Ezequiel Aceto
approved_at: 2026-11-08
created: 2026-11-08
updated: 2026-11-08
---

# 004: Teaching site on GitHub Pages

## Why it matters

Today the method lives in a repository. To learn it, a person clones, finds `docs/method.md` in a file tree, and reads reference prose with no guided path. The first fifteen minutes decide whether a developer adopts a method or closes the tab, and a file tree is the wrong place to spend them. In an organisation with many teams, most people who need the method will never clone this repository at all. They will be sent a link.

The documentation of existing tools shows the two failure modes to avoid. Marketing pages explain why without ever showing a change going through. Reference pages list every command without a path through them. Neither lets a reader feel the method work once, which is the moment adoption actually happens. The method has four capabilities, six skills and a validator, and none of it teaches itself.

## What should be done

Publish a site from this repository to its GitHub Pages address, built with MkDocs Material by a GitHub Actions workflow on every push to the main branch. The site serves developers first and team leads second, in UK English, under the plain title "Spec-driven development".

Its home page answers three questions in order. What spec-driven development is and why the method exists, in a few paragraphs with the state diagram. How to make a first change in fifteen minutes, as a guided tutorial that runs from installing the skills to archiving the change, built on transcripts from fresh real runs and shown with content tabs for Claude Code and Devin CLI, with other agents that follow the skills standard listed as untested. Where to find the reference: the method document included as it stands, the skills pulled in from their own files, the templates annotated, and the validator's rules listed with the requirements they enforce.

The repository's existing content is the source of truth. The site includes `docs/method.md` and the skill files rather than rewriting them, so there is one copy of every rule. The trial project becomes `examples/greenfield-go`, committed as the skills produced it, and the tutorial points at it. Two entry pages, one for developers and one for team leads, lead into the same material from different questions.

Alongside the deploy workflow, a second workflow runs the validator and the test suite on every pull request, so this repository is the first where the method is enforced in continuous integration.

## Scope

### In

- MkDocs Material configuration and a GitHub Actions workflow deploying to the project's GitHub Pages address on push to main
- Home page: what and why, the fifteen-minute tutorial, the reference map
- Tutorial pages with transcripts captured from fresh runs of each skill, with Claude Code and Devin CLI tabs
- A page listing agents: tested, and untested but expected to work through the skills standard
- Entry pages for developers and for team leads
- The method document, skills and templates included from their files, not copied
- A validator page generated from `--rules`
- `examples/greenfield-go`, the trial project, with its history told as a narrative page
- A second workflow running `python3 specs/validate.py` and the test suite on pull requests
- UK English throughout, Mermaid for diagrams, pinned build dependencies

### Out

- A brownfield example. It is its own change.
- Role pages for product owners or analysts. Developers and leads first.
- Translations, a custom domain, analytics or any tracking.
- Versioned documentation per release.
- Rewriting the method document or the skills for the web. If a sentence is unclear on the site, it is fixed at the source.
- A name for the method other than the category it belongs to.

## Success criteria

- A push to main builds and deploys the site without manual steps, and the build fails on a broken internal link.
- One person who has not used the method reaches an archived first change by following the site alone, in fifteen minutes or less, with the time and sticking points recorded.
- The tutorial's transcripts come from real runs, with the agent and date stated on the page.
- No rule of the method appears on the site in words that differ from `docs/method.md` or the skill files; the site includes those files.
- `examples/greenfield-go` passes the validator with zero violations, and the pull request workflow runs the validator and the tests.
- Every page except the included reference files reads in under five minutes, and the home page states which agents are tested and which are not.

## Constraints specific to this change

- Site content lives under `docs/`; nothing is moved out of `specs/` or `skills/` to serve the site.
- Build dependencies are pinned and used only in continuous integration; nothing is required to read the repository offline.
- UK spelling, in prose and in page titles.
