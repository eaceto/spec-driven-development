# 001: Tasks

## Setup

- [x] T01 Initialise the Go module (`go.mod`, `module sdd-trial`, `go 1.26`) with no dependencies [setup]

## Implementation

- [x] T02 Write `main.go`: `run(stdout, stderr io.Writer) int` prints `Hello, World!\n` and returns 0; `main` exits with its result [REQ-001-01, REQ-001-02]
- [x] T03 Write tests for output, empty standard error and exit status, in-process and via subprocess [REQ-001-01, REQ-001-02]
- [x] T04 Write a test asserting `go.mod` has no `require` directives [REQ-001-03]

## Verification

- [x] T05 Tests exist for every requirement ID above; `go test ./...` passes and `go vet ./...` is clean [all]
- [x] T06 Add `README.md` explaining how to run and test the program [all]
