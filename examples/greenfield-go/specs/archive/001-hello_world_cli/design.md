# 001: Design

## Approach

A single Go module at the repository root with one `main` package. `main.go` holds a small `run(stdout, stderr io.Writer) int` function that writes the greeting and returns the exit status; `main` calls `os.Exit(run(os.Stdout, os.Stderr))`. Keeping the logic in `run` lets tests check output, standard error and exit status in-process, without shelling out.

A second test re-executes the test binary as the real program (the `os.Args[0]` subprocess pattern) so the actual `main` path, including the exit status, is exercised end to end. A third test reads `go.mod` and asserts it has no `require` directives.

## Decisions

### Decision: Testable `run` function instead of logic in `main`
- Chosen: `main` delegates to `run(stdout, stderr io.Writer) int`.
- Alternatives considered: print directly from `main` and test only by building and executing the binary; capture `os.Stdout` with a pipe inside the test.
- Why: injecting writers is the idiomatic Go way to test command output, is fast and deterministic, and needs no temporary binaries. The subprocess test still covers the real entry point.
- Requirements affected: REQ-001-01, REQ-001-02

### Decision: Module path `sdd-trial`
- Chosen: `module sdd-trial`, `go 1.26` (the installed toolchain).
- Alternatives considered: a hosting path such as `github.com/<user>/sdd-trial`.
- Why: the repository has no remote and nothing imports it; a short local path avoids guessing a host. It can be renamed later without affecting behaviour.
- Requirements affected: REQ-001-03

## Interfaces and data

- Command line: `go run .` (or the built binary). No arguments, no flags, no input.
- Standard output: `Hello, World!\n`.
- Standard error: empty.
- Exit status: 0.
- Files added: `go.mod`, `main.go`, `main_test.go`, `README.md`.

## Risks

- A trailing-newline or whitespace mismatch would fail the exact-output criterion. The tests compare bytes exactly, so this is caught at `go test`.
- Someone later adding a dependency would break REQ-001-03 silently. The `go.mod` test catches it.

## Open questions

None.
