---
id: ci
title: Ci
owner: maintainers
updated: 2026-11-08
---

# Ci

## Purpose

Continuous integration for this repository: the validator, the test suite and a strict site build run on every pull request and push to main, and the site deploys from main. Exists so that the method is enforced where the changes arrive.

## Requirements

### REQ-004-13: Checks on pull requests
Origin: 004

A GitHub Actions workflow SHALL run the validator, the test suite and a strict site build on every pull request and every push to main, and SHALL fail when any of them fails.

#### Scenario: Failing validator
- GIVEN a pull request that leaves a change directory misnamed
- WHEN the workflow runs
- THEN the checks fail and name the validator step

## Retired

## History
- 004 (2026-11-08): Teaching site on GitHub Pages
