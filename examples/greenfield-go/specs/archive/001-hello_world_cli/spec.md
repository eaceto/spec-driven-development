---
id: "001"
title: Hello world CLI in Go
status: archived
tier: standard
owner: ezequiel.aceto
capabilities: [greeting]
ticket:
docs:
approved_by: ezequiel.aceto
approved_at: 2026-11-08
created: 2026-11-08
updated: 2026-11-08
---

# 001: Hello world CLI in Go

## Why it matters

This sandbox exists to try spec-driven development end to end, but it holds no code, so nothing can yet be planned, implemented, verified or archived. Its owner has no small, well-understood piece of behaviour to push through the lifecycle. If we do nothing, the process stays untested and any problems with it show up later on a real project, where they cost more.

## What should be done

The repository contains a Go command-line program. Running it prints the greeting `Hello, World!` and exits successfully. It is small enough that attention stays on the process rather than the code.

## Scope

### In

- A Go module at the repository root with a runnable `main` package.
- The program writes `Hello, World!` followed by a newline to standard output.
- An automated test that checks the output.

### Out

- Command-line arguments, flags or a customisable name. The greeting is fixed.
- An HTTP server or any other interface besides the command line.
- Release builds, packaging, installers or CI pipelines.
- Localisation of the greeting.

## Success criteria

- `go run .` at the repository root prints exactly `Hello, World!` and a newline to standard output, and nothing to standard error.
- The program exits with status 0.
- `go test ./...` passes, and at least one test asserts the exact output.
- `go vet ./...` reports no issues.

## Constraints specific to this change

- Standard library only; no third-party dependencies.
