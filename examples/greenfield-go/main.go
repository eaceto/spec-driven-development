// Command sdd-trial prints a greeting.
package main

import (
	"fmt"
	"io"
	"os"
)

const greeting = "Hello, World!"

// run writes the greeting to stdout and returns the process exit status.
func run(stdout, stderr io.Writer) int {
	fmt.Fprintln(stdout, greeting)
	return 0
}

func main() {
	os.Exit(run(os.Stdout, os.Stderr))
}
