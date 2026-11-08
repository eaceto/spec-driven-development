package main

import (
	"bytes"
	"os"
	"os/exec"
	"strings"
	"testing"
)

// REQ-001-01: standard output is exactly "Hello, World!\n".
func TestRun_REQ_001_01_PrintsGreeting(t *testing.T) {
	var stdout, stderr bytes.Buffer
	run(&stdout, &stderr)
	if got, want := stdout.String(), "Hello, World!\n"; got != want {
		t.Errorf("stdout = %q, want %q", got, want)
	}
}

// REQ-001-02: exit status is 0 and standard error is empty.
func TestRun_REQ_001_02_ExitsCleanly(t *testing.T) {
	var stdout, stderr bytes.Buffer
	if code := run(&stdout, &stderr); code != 0 {
		t.Errorf("exit status = %d, want 0", code)
	}
	if stderr.Len() != 0 {
		t.Errorf("stderr = %q, want empty", stderr.String())
	}
}

// TestMainProcess runs main as the real program when re-executed by
// TestMain_REQ_001_01_REQ_001_02_Subprocess.
func TestMainProcess(t *testing.T) {
	if os.Getenv("SDD_TRIAL_RUN_MAIN") != "1" {
		t.Skip("helper process for the subprocess test")
	}
	main()
}

// REQ-001-01, REQ-001-02: the real program prints exactly "Hello, World!\n",
// writes nothing to standard error and exits with status 0.
func TestMain_REQ_001_01_REQ_001_02_Subprocess(t *testing.T) {
	cmd := exec.Command(os.Args[0], "-test.run=^TestMainProcess$")
	cmd.Env = append(os.Environ(), "SDD_TRIAL_RUN_MAIN=1")
	var stdout, stderr bytes.Buffer
	cmd.Stdout, cmd.Stderr = &stdout, &stderr
	if err := cmd.Run(); err != nil {
		t.Fatalf("exit: %v (want status 0)", err)
	}
	if got, want := stdout.String(), "Hello, World!\n"; got != want {
		t.Errorf("stdout = %q, want %q", got, want)
	}
	if stderr.Len() != 0 {
		t.Errorf("stderr = %q, want empty", stderr.String())
	}
}

// REQ-001-03: go.mod declares no require directives, so the program uses the
// standard library only.
func TestGoMod_REQ_001_03_NoDependencies(t *testing.T) {
	data, err := os.ReadFile("go.mod")
	if err != nil {
		t.Fatal(err)
	}
	for i, line := range strings.Split(string(data), "\n") {
		if f := strings.Fields(line); len(f) > 0 && f[0] == "require" {
			t.Errorf("go.mod:%d: unexpected dependency: %s", i+1, strings.TrimSpace(line))
		}
	}
}
