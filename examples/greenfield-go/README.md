# sdd-trial

A sandbox for trying spec-driven development. It holds a Go command-line program that prints a greeting.

## Run

Requires Go 1.26 or later.

```sh
go run .
```

Prints `Hello, World!` and exits with status 0. It takes no arguments.

## Test

```sh
go test ./...
go vet ./...
```

## Specs

Specs live in `specs/`. Start with `specs/constitution.md` and `specs/INDEX.md`; `AGENTS.md` describes how work moves through a change.
