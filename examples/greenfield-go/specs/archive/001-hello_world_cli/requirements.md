# 001: Requirements

## Capability: greeting

### REQ-001-01: Print the greeting
When the program is run, the program SHALL write exactly `Hello, World!` followed by a single newline to standard output.

#### Scenario: Run with no arguments
- GIVEN the repository root
- WHEN `go run .` is executed
- THEN standard output is exactly `Hello, World!\n`

### REQ-001-02: Exit cleanly
When the program is run, the program SHALL exit with status 0 and write nothing to standard error.

#### Scenario: Clean exit
- GIVEN the repository root
- WHEN `go run .` is executed
- THEN the exit status is 0
- AND standard error is empty

### REQ-001-03: Standard library only
The program SHALL depend on the Go standard library only.

#### Scenario: No third-party modules
- GIVEN the repository's `go.mod`
- WHEN its contents are inspected
- THEN it declares no `require` directives

## Modified requirements

None. The `greeting` capability is new.

## Removed requirements

None.

## Not testable

None.
