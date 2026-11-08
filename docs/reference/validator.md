# The validator

`specs/validate.py` checks the mechanical rules of the method and names the requirement behind each one. It is one Python 3 file with no dependencies. The install script copies it into a project and sets `validator: python3 specs/validate.py` in the constitution, so the skills run it before they report.

## Commands

```
python3 specs/validate.py            check the whole specs/ tree
python3 specs/validate.py 014        check change 014 alone
python3 specs/validate.py --rules    list the rules and the requirements they enforce
```

Exit codes: 0 clean, 1 violations found, 2 usage error.

## What a violation looks like

```
specs/changes/014-passwordless_login/requirements.md: requirement-grammar (REQ-001-08): REQ-014-03: no scenario
1 violations, 12 files, 21 rules
```

Path, rule, the requirement the rule enforces, and what to fix. The requirement id is a link into the method: REQ-001-08 is the requirement grammar, so the message tells you both what is wrong and why the rule exists.

## What it checks

Layout, change naming and numbering, the files each tier requires, the order of `spec.md`, frontmatter fields and dates, requirement grammar and grouping, capability specs, status consistency including test coverage and archive merges, the index against the file system, the constitution, the agent entry file, commit trailers when git is available, and the skills when a project ships them. The complete list, generated from the validator itself, is on the [rules page](validator-rules.md).

## What it does not check

Whether a test proves its scenario. The coverage rule counts a requirement as tested when its id appears in a test file; that is the floor a machine can check, and judgement is the reviewer's.

Whether a purpose is well written, a scenario is meaningful or a design decision is sound. Those remain with people and the skills' refuse-when sections.

## In continuous integration

This repository runs the validator and its test suite on every pull request. The workflow is three steps: check out, `python3 specs/validate.py`, `python3 -m unittest discover tests`. Copy it into your project and the method is enforced where it matters.
