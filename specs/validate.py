#!/usr/bin/env python3
"""Validate a specs/ tree against the spec-driven development method.

    python3 specs/validate.py            check the whole tree
    python3 specs/validate.py 014        check change 014 only
    python3 specs/validate.py --rules    list the rules and the requirements they enforce

Exit codes: 0 no violations, 1 violations found, 2 usage error.
Standard library only. Python 3.9 or later. Every rule names the requirement
of the method it enforces, so a violation tells you both what is wrong and why
the rule exists. Rules are registered once in the RULES list; adding one means
adding one function.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, Iterator, List, Optional, Sequence, Set, Tuple

VERSION = "0.1.0"

# Limits, each with the requirement it serves.
CONSTITUTION_MAX_LINES = 80  # REQ-001-13: a constitution fits on one page
SKILL_MAX_LINES = 150  # REQ-002-01
RECENT_COMMITS = 10  # REQ-001-23

STATUSES = ["draft", "approved", "in-progress", "done", "archived"]
TIER_FILES: Dict[str, Set[str]] = {
    "quick": {"spec.md", "tasks.md", "checklist.md"},
    "standard": {"spec.md", "tasks.md", "checklist.md", "requirements.md", "design.md"},
    "full": {"spec.md", "tasks.md", "checklist.md", "requirements.md", "design.md", "guardrails.md"},
}
SPECS_ENTRIES = {"constitution.md", "INDEX.md", "templates", "capabilities", "changes", "archive"}
SPECS_OPTIONAL = {"validate.py"}
CHANGE_FM_KEYS = ["id", "title", "status", "tier", "owner", "capabilities", "ticket", "docs",
                  "approved_by", "approved_at", "created", "updated"]
CONSTITUTION_FM_KEYS = ["extends", "version", "owner", "numbering", "sdd_version"]
CONSTITUTION_SECTIONS = ["Purpose", "Principles", "Definitions", "Amendments"]
SPEC_SECTIONS = ["Why it matters", "What should be done", "Scope", "Success criteria"]
SPEC_OPTIONAL_SECTION = "Constraints specific to this change"
CAPABILITY_SECTIONS = ["Purpose", "Requirements", "Retired", "History"]
REQUIREMENTS_TRAILING_SECTIONS = ["Modified requirements", "Removed requirements", "Not testable"]
INDEX_SECTIONS = ["Active changes", "Capabilities", "Archived changes"]
SKILL_SECTIONS = ["When to use", "Preconditions", "Steps", "Refuse when", "Done when"]
VENDOR_PATHS = [".claude", ".devin", ".agents"]
VENDOR_NAMES = re.compile(r"\b(claude|devin|cursor|copilot|codex|windsurf)\b", re.IGNORECASE)

CHANGE_DIR_RE = re.compile(r"^(\d{3})-[a-z0-9]+(?:_[a-z0-9]+)*$")
REQ_HEADING_RE = re.compile(r"^### (REQ-(\d{3})-(\d{2,})): (.+?)\s*$")
REQ_ID_RE = re.compile(r"REQ-\d{3}-\d{2,}")
SCENARIO_RE = re.compile(r"^#### Scenario: .+")
BULLET_RE = re.compile(r"^- (GIVEN|WHEN|THEN|AND)\b")
H2_RE = re.compile(r"^## (.+?)\s*$")
H3_RE = re.compile(r"^### (.+?)\s*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TASK_RE = re.compile(r"^- \[([ xX])\] (T\d+)\b")
CHECK_RE = re.compile(r"^- \[([ xX])\] ")
GATE_RE = re.compile(r"^## Gate (\d)\b")
TRAILER_RE = re.compile(r"^Change: (\d{3})\s*$", re.MULTILINE)
LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)")
REFERENCE_RE = re.compile(r"^(?:(?P<repo>[A-Za-z0-9._-]+):)?(?P<change>\d{3})(?:/(?P<req>REQ-\d{2,}))?$")


# ---------------------------------------------------------------------------
# Frontmatter: the subset of YAML the templates use, and nothing more.

def parse_frontmatter(text: str) -> Tuple[Optional[Dict[str, object]], str, Optional[str]]:
    """Return (fields, body, error). Fields hold strings or lists; nested keys join with a dot."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, text, "missing frontmatter"
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        return None, text, "unterminated frontmatter"
    fields: Dict[str, object] = {}
    parent: Optional[str] = None
    for raw in lines[1:end]:
        line = _strip_comment(raw)
        if not line.strip():
            continue
        if ":" not in line:
            return None, "\n".join(lines[end + 1:]), f"frontmatter line without a colon: {raw.strip()}"
        key, _, value = line.strip().partition(":")
        key, parsed = key.strip(), _parse_value(value.strip())
        if line.startswith("  ") and parent is not None:
            fields[f"{parent}.{key}"] = parsed
        else:
            fields[key] = parsed
            parent = key if parsed == "" else None
    return fields, "\n".join(lines[end + 1:]), None


def _strip_comment(line: str) -> str:
    idx = line.find(" #")
    return line if idx < 0 else line[:idx]


def _parse_value(value: str) -> object:
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        return [] if not inner else [_unquote(x.strip()) for x in inner.split(",")]
    return _unquote(value)


def _unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_reference(ref: str) -> Optional[Dict[str, Optional[str]]]:
    """Parse `repo:014/REQ-03`, `repo:014`, `014/REQ-03` or `014`. REQ-001-15."""
    m = REFERENCE_RE.match(ref.strip())
    return None if not m else {"repo": m.group("repo"), "change": m.group("change"), "req": m.group("req")}


# ---------------------------------------------------------------------------
# Model

@dataclass
class Violation:
    path: str
    rule: str
    reqs: Sequence[str]
    message: str

    def format(self) -> str:
        return f"{self.path}: {self.rule} ({', '.join(self.reqs)}): {self.message}"


@dataclass
class Requirement:
    id: str
    change: str
    title: str
    line: int
    section: str = ""  # "capability:<id>", "modified", or "" when outside both
    statements: List[str] = field(default_factory=list)
    scenarios: List[List[str]] = field(default_factory=list)
    origin: Optional[str] = None
    changed_in: List[str] = field(default_factory=list)


@dataclass
class Change:
    path: Path
    rel: str
    dirname: str
    location: str  # "changes" or "archive"
    num: Optional[str]
    fm: Dict[str, object]
    fm_error: Optional[str]
    files: Set[str]
    spec_lines: List[str]
    requirements: List[Requirement]
    capability_sections: List[str]
    req_sections: List[str]
    removed_ids: List[str]
    not_testable_ids: Set[str]
    tasks: List[Tuple[bool, str]]
    gates: Dict[int, List[bool]]

    @property
    def status(self) -> str:
        return str(self.fm.get("status", ""))

    @property
    def tier(self) -> str:
        return str(self.fm.get("tier", ""))

    @property
    def capabilities(self) -> List[str]:
        value = self.fm.get("capabilities", [])
        return [str(v) for v in value] if isinstance(value, list) else []

    def added(self) -> List[Requirement]:
        return [r for r in self.requirements if r.section.startswith("capability:")]

    def modified(self) -> List[Requirement]:
        return [r for r in self.requirements if r.section == "modified"]


@dataclass
class Capability:
    path: Path
    rel: str
    dirname: str
    fm: Dict[str, object]
    fm_error: Optional[str]
    sections: List[str]
    requirements: List[Requirement]
    retired_ids: List[str]
    has_spec: bool


@dataclass
class Project:
    root: Path
    specs: Path
    constitution_fm: Optional[Dict[str, object]] = None
    constitution_error: Optional[str] = None
    constitution_sections: List[str] = field(default_factory=list)
    constitution_lines: int = 0
    index_text: Optional[str] = None
    changes: List[Change] = field(default_factory=list)
    capabilities: List[Capability] = field(default_factory=list)
    stray_entries: List[str] = field(default_factory=list)  # visible non-directories in changes/ or archive/
    git: bool = False
    git_prefix: str = ""
    files_read: int = 0
    _corpus: Optional[str] = None

    def active_ids(self) -> Dict[str, Tuple[Capability, Requirement]]:
        out: Dict[str, Tuple[Capability, Requirement]] = {}
        for cap in self.capabilities:
            for r in cap.requirements:
                out.setdefault(r.id, (cap, r))
        return out

    def retired_ids(self) -> Dict[str, Capability]:
        return {rid: cap for cap in self.capabilities for rid in cap.retired_ids}

    def test_corpus(self) -> str:
        """Text of every file outside specs/ whose path contains 'test'. REQ-001-20 counts a requirement as tested when its id appears here."""
        if self._corpus is None:
            parts: List[str] = []
            for p in sorted(self.root.rglob("*")):
                rel = p.relative_to(self.root)
                if any(part.startswith(".") or part in ("specs", "node_modules") for part in rel.parts):
                    continue
                if p.is_file() and "test" in str(rel).lower():
                    try:
                        parts.append(p.read_text(encoding="utf-8", errors="ignore"))
                    except OSError:
                        continue
            self._corpus = "\n".join(parts)
        return self._corpus

    # Git helpers, best effort: None when git or the repository is unavailable.
    def git_run(self, *args: str) -> Optional[str]:
        try:
            done = subprocess.run(["git", *args], cwd=str(self.root), capture_output=True, text=True, timeout=20)
        except (OSError, subprocess.TimeoutExpired):
            return None
        return done.stdout if done.returncode == 0 else None

    def git_previous_status(self, change: Change) -> Optional[str]:
        for location in ("changes", "archive"):
            text = self.git_run("show", f"HEAD:{self.git_prefix}specs/{location}/{change.dirname}/spec.md")
            if text is not None:
                fm, _, _ = parse_frontmatter(text)
                return str(fm.get("status", "")) if fm else None
        return None

    def recent_commits(self) -> List[Tuple[str, str, List[str]]]:
        """(sha, message, touched paths relative to the repository root) for the last RECENT_COMMITS non-merge commits."""
        out: List[Tuple[str, str, List[str]]] = []
        shas = self.git_run("log", f"-n{RECENT_COMMITS}", "--no-merges", "--format=%H")
        for sha in (shas or "").split():
            show = self.git_run("show", "--format=%B%x00", "--name-only", sha)
            if show is None:
                continue
            message, _, files = show.partition("\x00")
            out.append((sha, message, [f for f in files.split("\n") if f.strip()]))
        return out


# ---------------------------------------------------------------------------
# Loading

def _read(project: Project, path: Path) -> Optional[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    project.files_read += 1
    return text


def _visible(path: Path) -> List[Path]:
    return sorted(p for p in path.iterdir() if not p.name.startswith(".")) if path.is_dir() else []


def _h2_sections(lines: Sequence[str]) -> List[Tuple[str, int, int]]:
    """(name, first line index after heading, end index) for each level-two heading."""
    heads = [(m.group(1), i) for i, line in enumerate(lines) for m in [H2_RE.match(line)] if m]
    return [(name, i + 1, heads[k + 1][1] if k + 1 < len(heads) else len(lines)) for k, (name, i) in enumerate(heads)]


def parse_requirement_blocks(lines: Sequence[str], lo: int, hi: int, section: str) -> List[Requirement]:
    blocks: List[Requirement] = []
    i = lo
    while i < hi:
        m = REQ_HEADING_RE.match(lines[i])
        if not m:
            i += 1
            continue
        req = Requirement(id=m.group(1), change=m.group(2), title=m.group(4), line=i + 1, section=section)
        scenario: Optional[List[str]] = None
        j = i + 1
        while j < hi and not lines[j].startswith("### ") and not lines[j].startswith("## "):
            line = lines[j]
            if SCENARIO_RE.match(line):
                scenario = []
                req.scenarios.append(scenario)
            elif scenario is not None:
                b = BULLET_RE.match(line)
                if b:
                    scenario.append(b.group(1))
            else:
                s = line.strip()
                if s.startswith("Origin:"):
                    req.origin = s.split(":", 1)[1].strip()
                elif s.startswith("Changed in:"):
                    req.changed_in = [x.strip() for x in s.split(":", 1)[1].split(",") if x.strip()]
                elif s and not s.startswith("Ref:"):
                    req.statements.append(s)
            j += 1
        blocks.append(req)
        i = j
    return blocks


def parse_requirements_doc(text: str) -> Tuple[List[Requirement], List[str], List[str], List[str], Set[str]]:
    """Return (requirements, capability section ids, all section names, removed ids, not-testable ids)."""
    lines = text.splitlines()
    sections = _h2_sections(lines)
    reqs: List[Requirement] = []
    caps: List[str] = []
    removed: List[str] = []
    not_testable: Set[str] = set()
    first = sections[0][1] - 1 if sections else len(lines)
    reqs.extend(parse_requirement_blocks(lines, 0, first, ""))
    for name, lo, hi in sections:
        if name.startswith("Capability:"):
            cap = name.split(":", 1)[1].strip()
            caps.append(cap)
            reqs.extend(parse_requirement_blocks(lines, lo, hi, f"capability:{cap}"))
        elif name == "Modified requirements":
            reqs.extend(parse_requirement_blocks(lines, lo, hi, "modified"))
        elif name == "Removed requirements":
            removed.extend(REQ_ID_RE.findall("\n".join(l for l in lines[lo:hi] if l.startswith("- "))))
        elif name == "Not testable":
            not_testable.update(REQ_ID_RE.findall("\n".join(lines[lo:hi])))
        else:
            reqs.extend(parse_requirement_blocks(lines, lo, hi, ""))
    return reqs, caps, [s[0] for s in sections], removed, not_testable


def parse_tasks(text: str) -> List[Tuple[bool, str]]:
    return [(m.group(1) != " ", m.group(2)) for line in text.splitlines() for m in [TASK_RE.match(line)] if m]


def parse_checklist(text: str) -> Dict[int, List[bool]]:
    gates: Dict[int, List[bool]] = {}
    current: Optional[int] = None
    for line in text.splitlines():
        g = GATE_RE.match(line)
        if g:
            current = int(g.group(1))
            gates.setdefault(current, [])
        elif current is not None and CHECK_RE.match(line):
            gates[current].append(line[3] != " ")
    return gates


def load_change(project: Project, path: Path, location: str) -> Change:
    rel = f"specs/{location}/{path.name}"
    m = CHANGE_DIR_RE.match(path.name)
    files = {p.name for p in _visible(path)}
    fm: Dict[str, object] = {}
    fm_error: Optional[str] = None
    spec_lines: List[str] = []
    spec_text = _read(project, path / "spec.md") if "spec.md" in files else None
    if spec_text is not None:
        parsed, body, fm_error = parse_frontmatter(spec_text)
        fm = parsed or {}
        spec_lines = body.splitlines()
    reqs, caps, sections, removed, not_testable = [], [], [], [], set()
    if "requirements.md" in files:
        text = _read(project, path / "requirements.md")
        if text is not None:
            reqs, caps, sections, removed, not_testable = parse_requirements_doc(text)
    tasks = parse_tasks(_read(project, path / "tasks.md") or "") if "tasks.md" in files else []
    gates = parse_checklist(_read(project, path / "checklist.md") or "") if "checklist.md" in files else {}
    return Change(path, rel, path.name, location, m.group(1) if m else None, fm, fm_error, files, spec_lines,
                  reqs, caps, sections, removed, not_testable, tasks, gates)


def load_capability(project: Project, path: Path) -> Capability:
    rel = f"specs/capabilities/{path.name}"
    spec = path / "spec.md"
    text = _read(project, spec) if spec.is_file() else None
    if text is None:
        return Capability(path, rel, path.name, {}, None, [], [], [], False)
    fm, body, err = parse_frontmatter(text)
    lines = body.splitlines()
    sections = _h2_sections(lines)
    reqs: List[Requirement] = []
    retired: List[str] = []
    for name, lo, hi in sections:
        if name == "Requirements":
            reqs = parse_requirement_blocks(lines, lo, hi, "capability")
        elif name == "Retired":
            retired = REQ_ID_RE.findall("\n".join(l for l in lines[lo:hi] if l.startswith("- ")))
    return Capability(path, rel, path.name, fm or {}, err, [s[0] for s in sections], reqs, retired, True)


def load_project(root: Path) -> Project:
    project = Project(root=root, specs=root / "specs")
    if not project.specs.is_dir():
        return project
    text = _read(project, project.specs / "constitution.md")
    if text is not None:
        project.constitution_fm, body, project.constitution_error = parse_frontmatter(text)
        project.constitution_sections = [s[0] for s in _h2_sections(body.splitlines())]
        project.constitution_lines = len(text.splitlines())
    project.index_text = _read(project, project.specs / "INDEX.md")
    for location in ("changes", "archive"):
        for entry in _visible(project.specs / location):
            if entry.is_dir():
                project.changes.append(load_change(project, entry, location))
            else:
                project.stray_entries.append(f"specs/{location}/{entry.name}")
    for entry in _visible(project.specs / "capabilities"):
        if entry.is_dir():
            project.capabilities.append(load_capability(project, entry))
    top = project.git_run("rev-parse", "--show-toplevel")
    if top:
        project.git = True
        try:
            prefix = root.resolve().relative_to(Path(top.strip()).resolve())
            project.git_prefix = "" if str(prefix) == "." else f"{prefix.as_posix()}/"
        except ValueError:
            project.git = False
    return project


# ---------------------------------------------------------------------------
# Rules. Each is registered once with the requirements it enforces.

CheckFn = Callable[..., Iterator[Violation]]


@dataclass
class Rule:
    id: str
    reqs: Sequence[str]
    description: str
    scope: str  # "project", "change" or "capability"
    check: CheckFn


RULES: List[Rule] = []


def rule(rule_id: str, reqs: Sequence[str], description: str, scope: str = "project") -> Callable[[CheckFn], CheckFn]:
    def register(fn: CheckFn) -> CheckFn:
        RULES.append(Rule(rule_id, list(reqs), description, scope, fn))
        return fn
    return register


# ---------------------------------------------------------------------------
# Running

def validate(root: Path, change: Optional[str] = None) -> Tuple[List[Violation], Dict[str, object]]:
    project = load_project(root)
    stats: Dict[str, object] = {"files": 0, "rules": 0, "git": False, "missing_change": False}
    if not project.specs.is_dir():
        return [Violation("specs", "layout-root", ["REQ-001-01"], "no specs/ directory here")], stats
    if change is not None and not any(c.num == change for c in project.changes):
        stats["missing_change"] = True
        return [], stats
    violations: List[Violation] = []
    for r in RULES:
        if change is not None and r.scope != "change":
            continue
        stats["rules"] = int(stats["rules"]) + 1
        if r.scope == "project":
            violations.extend(r.check(project))
        elif r.scope == "change":
            for ch in project.changes:
                if change is None or ch.num == change:
                    violations.extend(r.check(project, ch))
        elif r.scope == "capability":
            for cap in project.capabilities:
                violations.extend(r.check(project, cap))
    stats["files"] = project.files_read
    stats["git"] = project.git
    return violations, stats


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="validate.py", description=__doc__.split("\n\n")[0])
    parser.add_argument("change", nargs="?", help="three-digit change number to check alone")
    parser.add_argument("--rules", action="store_true", help="list the rules and exit")
    parser.add_argument("--root", default=".", help="project root (default: current directory)")
    parser.add_argument("--version", action="version", version=VERSION)
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code) if isinstance(exc.code, int) else 2
    if args.rules:
        for r in RULES:
            print(f"{r.id:<24} {', '.join(r.reqs):<40} {r.description}")
        return 0
    if args.change is not None and not re.fullmatch(r"\d{3}", args.change):
        print(f"usage error: change must be three digits, got {args.change!r}", file=sys.stderr)
        return 2
    violations, stats = validate(Path(args.root), args.change)
    if stats.get("missing_change"):
        print(f"usage error: no change {args.change} under specs/changes/ or specs/archive/", file=sys.stderr)
        return 2
    for v in sorted(violations, key=lambda v: (v.path, v.rule, v.message)):
        print(v.format())
    note = "" if stats.get("git") else "; git checks skipped"
    print(f"{len(violations)} violations, {stats['files']} files, {stats['rules']} rules{note}")
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
