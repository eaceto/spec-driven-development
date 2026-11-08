"""Self-tests for specs/validate.py.

Every test names the requirement ids it covers, from change 003 (the validator)
and change 001 (the rules it enforces). Fixtures are built from specs/templates/
so that drift between the templates and the validator shows up here.

Run: python3 -m unittest discover tests
"""
import ast
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "specs" / "validate.py"
TEMPLATES = ROOT / "specs" / "templates"
TODAY = "2026-11-08"


def load_validator():
    spec = importlib.util.spec_from_file_location("sdd_validate", VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # dataclasses resolve annotations through sys.modules
    spec.loader.exec_module(module)
    return module


V = load_validator()
GIT = shutil.which("git") is not None


def req_block(rid, origin=None, changed_in=None, scenario=True, bullets=("GIVEN", "WHEN", "THEN")):
    lines = [f"### {rid}: Title"]
    if origin:
        lines.append(f"Origin: {origin}")
    if changed_in:
        lines.append(f"Changed in: {changed_in}")
    lines += ["", "The system SHALL do the thing.", ""]
    if scenario:
        lines += ["#### Scenario: Name"] + [f"- {b} something" for b in bullets] + [""]
    return "\n".join(lines) + "\n"


def with_req(text, block):
    """Insert a requirement block into the capability section of a requirements file."""
    return text.replace("## Modified requirements", block + "## Modified requirements", 1)


def tick_gates(text, up_to):
    out, gate = [], None
    for line in text.splitlines():
        m = re.match(r"^## Gate (\d)", line)
        if m:
            gate = int(m.group(1))
        if gate is not None and gate <= up_to and line.startswith("- [ ]"):
            line = "- [x]" + line[5:]
        out.append(line)
    return "\n".join(out) + "\n"


class Record:
    def __init__(self, **kw):
        self.__dict__.update(kw)


class Fixture:
    """A minimal valid project built from the templates."""

    def __init__(self):
        self.root = Path(tempfile.mkdtemp(prefix="sdd-fixture-"))
        self.specs = self.root / "specs"
        for d in ("capabilities", "changes", "archive"):
            (self.specs / d).mkdir(parents=True)
        shutil.copytree(TEMPLATES, self.specs / "templates")
        constitution = (TEMPLATES / "constitution.md").read_text()
        constitution = re.sub(r"^owner:.*$", "owner: team-x", constitution, count=1, flags=re.M)
        (self.specs / "constitution.md").write_text(constitution)
        (self.root / "AGENTS.md").write_text((TEMPLATES / "AGENTS.md").read_text())
        self.changes = []
        self.caps = []
        self.write_index()

    def cleanup(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def set_numbering(self, mode):
        c = self.specs / "constitution.md"
        c.write_text(re.sub(r"^numbering:.*$", f"numbering: {mode}", c.read_text(), count=1, flags=re.M))

    # -- changes --------------------------------------------------------
    def add_change(self, num="014", name="sample_change", status="in-progress", tier="standard",
                   caps=("auth",), location="changes", approved=None, extra_requirements=""):
        approved = (status != "draft") if approved is None else approved
        dirname = f"{num}-{name}"
        d = self.specs / location / dirname
        d.mkdir()
        template = (TEMPLATES / "change" / "spec.md").read_text()
        tpl_fm, tpl_body, _ = V.parse_frontmatter(template)
        values = {"id": f'"{num}"', "title": "Sample change", "status": status, "tier": tier, "owner": "team-x",
                  "capabilities": "[" + ", ".join(caps) + "]", "ticket": "", "docs": "",
                  "approved_by": "someone" if approved else "", "approved_at": TODAY if approved else "",
                  "created": TODAY, "updated": TODAY}
        fm = "\n".join(["---"] + [f"{k}: {values[k]}" for k in tpl_fm] + ["---"])
        body = tpl_body.replace("NNN: Change title", f"{num}: Sample change")
        body = re.sub(r"^-$", "- item", body, flags=re.M)
        (d / "spec.md").write_text(fm + "\n" + body)
        planned = status != "draft"
        if planned:
            if tier != "quick":
                requirements = (TEMPLATES / "change" / "requirements.md").read_text()
                requirements = requirements.replace("NNN", num).replace("capability-id", caps[0])
                requirements = requirements.replace("## Modified requirements", extra_requirements + "## Modified requirements", 1)
                (d / "requirements.md").write_text(requirements)
                (d / "design.md").write_text((TEMPLATES / "change" / "design.md").read_text().replace("NNN", num))
            if tier == "full":
                (d / "guardrails.md").write_text((TEMPLATES / "change" / "guardrails.md").read_text().replace("NNN", num))
            tasks = (TEMPLATES / "change" / "tasks.md").read_text().replace("NNN", num)
            if status in ("done", "archived"):
                tasks = tasks.replace("- [ ]", "- [x]")
            (d / "tasks.md").write_text(tasks)
            checklist = (TEMPLATES / "change" / "checklist.md").read_text().replace("NNN", num)
            gate = {"approved": 1, "in-progress": 1, "done": 2, "archived": 3}[status]
            (d / "checklist.md").write_text(tick_gates(checklist, gate))
        rec = Record(num=num, dirname=dirname, title="Sample change", status=status, tier=tier, owner="team-x",
                     caps=list(caps), updated=TODAY, location=location, path=d)
        self.changes.append(rec)
        self.write_index()
        return rec

    def change_ids(self, num):
        """Requirement ids the template gives an added change."""
        return [f"REQ-{num}-01", f"REQ-{num}-02"]

    def add_tests_mentioning(self, ids):
        tests = self.root / "tests"
        tests.mkdir(exist_ok=True)
        names = "\n".join(f"def test_{i.replace('-', '_')}():\n    pass\n" for i in ids)
        (tests / "test_fixture.py").write_text(names)

    # -- capabilities ---------------------------------------------------
    def add_capability(self, cid="auth", blocks=(), retired=()):
        d = self.specs / "capabilities" / cid
        d.mkdir()
        text = (TEMPLATES / "capability.md").read_text()
        text = re.sub(r"^id:.*$", f"id: {cid}", text, count=1, flags=re.M)
        text = re.sub(r"^title:.*$", f"title: {cid.title()}", text, count=1, flags=re.M)
        text = re.sub(r"^owner:.*$", "owner: team-x", text, count=1, flags=re.M)
        text = re.sub(r"^updated:.*$", f"updated: {TODAY}", text, count=1, flags=re.M)
        text = text.replace("## Retired", "".join(blocks) + "\n## Retired")
        text = text.replace("## History", "".join(f"- {rid}, removed by change 099: reason.\n" for rid in retired) + "\n## History")
        (d / "spec.md").write_text(text)
        rec = Record(id=cid, title=cid.title(), owner="team-x", count=len(blocks), updated=TODAY, path=d)
        self.caps.append(rec)
        self.write_index()
        return rec

    # -- index ----------------------------------------------------------
    def write_index(self):
        text = (TEMPLATES / "INDEX.md").read_text()
        head, cap_heading, rest = text.partition("## Capabilities")
        caps_part, arch_heading, archived_part = rest.partition("## Archived changes")
        active = "".join(
            f"| {c.num} | [{c.title}](changes/{c.dirname}/spec.md) | {c.status} | {c.tier} | {c.owner} | | {', '.join(c.caps)} | {c.updated} |\n"
            for c in self.changes if c.location == "changes")
        caps = "".join(f"| {k.id} | [{k.title}](capabilities/{k.id}/spec.md) | {k.owner} | {k.count} | {k.updated} |\n" for k in self.caps)
        archived = sum(1 for c in self.changes if c.location == "archive")
        head = head.replace("|---|---|---|---|---|---|---|---|\n", "|---|---|---|---|---|---|---|---|\n" + active, 1)
        caps_part = caps_part.replace("|---|---|---|---|---|\n", "|---|---|---|---|---|\n" + caps, 1)
        archived_part = archived_part.replace("0 archived.", f"{archived} archived.")
        (self.specs / "INDEX.md").write_text(head + cap_heading + caps_part + arch_heading + archived_part)

    # -- git ------------------------------------------------------------
    def git(self, *args):
        return subprocess.run(["git", *args], cwd=str(self.root), capture_output=True, text=True, check=True).stdout

    def git_init_and_commit(self, message="Initial"):
        self.git("init", "-q")
        self.git("config", "user.email", "t@example.com")
        self.git("config", "user.name", "Tests")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", message)


class ValidatorCase(unittest.TestCase):
    def setUp(self):
        self.fx = Fixture()
        self.addCleanup(self.fx.cleanup)

    def run_validator(self, change=None, root=None):
        violations, stats = V.validate(root or self.fx.root, change)
        return violations

    def assert_clean(self, violations=None):
        violations = self.run_validator() if violations is None else violations
        self.assertEqual([], [v.format() for v in violations])

    def assert_violation(self, violations, rule=None, req=None, path=None, text=None):
        matches = [v for v in violations
                   if (rule is None or v.rule == rule) and (req is None or req in v.reqs)
                   and (path is None or path in v.path) and (text is None or text in v.message)]
        self.assertTrue(matches, f"no violation matching rule={rule} req={req} path={path} text={text} in:\n"
                        + "\n".join(v.format() for v in violations))
        return matches

    def assert_no_violation(self, violations, rule):
        self.assertEqual([], [v.format() for v in violations if v.rule == rule])


class TestFileAndCli(ValidatorCase):
    def test_imports_are_standard_library_REQ_003_01(self):
        tree = ast.parse(VALIDATOR.read_text())
        modules = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                modules.add(node.module.split(".")[0])
        allowed = set(getattr(sys, "stdlib_module_names", {"__future__", "argparse", "dataclasses", "pathlib", "re",
                                                             "subprocess", "sys", "typing"}))
        self.assertTrue(modules <= allowed, modules - allowed)

    def test_syntax_and_apis_are_python_3_9_compatible_REQ_003_01(self):
        source = VALIDATOR.read_text()
        ast.parse(source, feature_version=(3, 9))  # rejects syntax introduced after 3.9
        newer_apis = ["zip(strict", "removeprefix(", "removesuffix(", "slots=True", "kw_only", "TypeAlias",
                      "stdlib_module_names", "pairwise(", "bisect(", "ExceptionGroup", "tomllib"]
        for api in newer_apis:
            self.assertNotIn(api, source, f"{api} needs a Python newer than 3.9")

    def run_cli(self, *args, root=None):
        return subprocess.run([sys.executable, "-B", str(VALIDATOR), "--root", str(root or self.fx.root), *args],
                              capture_output=True, text=True)

    def test_exit_codes_REQ_003_02(self):
        self.fx.add_change()
        self.assertEqual(0, self.run_cli().returncode)
        self.assertEqual(2, self.run_cli("abc").returncode)
        self.assertEqual(2, self.run_cli("999").returncode)
        broken = self.fx.add_change("015", "broken_change", extra_requirements=req_block("REQ-015-03", scenario=False))
        self.assertEqual(1, self.run_cli().returncode)
        self.assertEqual(1, self.run_cli("015").returncode)
        self.assertIn(f"{broken.dirname}/requirements.md", self.run_cli("015").stdout)
        self.assertEqual(0, self.run_cli("014").returncode, "single-change mode checks that change alone")

    def test_report_format_REQ_003_03(self):
        self.fx.add_change(extra_requirements=req_block("REQ-014-03", scenario=False))
        out = self.run_cli().stdout.splitlines()
        self.assertRegex(out[0], r"^specs/changes/014-sample_change/requirements\.md: requirement-grammar \(REQ-001-08\): REQ-014-03: no scenario$")
        self.assertRegex(out[-1], r"^1 violations, \d+ files, \d+ rules")

    def test_rules_are_listed_and_cover_change_001_REQ_003_04(self):
        out = self.run_cli("--rules").stdout
        ids = [r.id for r in V.RULES]
        self.assertEqual(len(ids), len(set(ids)), "rule ids are unique")
        for r in V.RULES:
            self.assertIn(r.id, out)
            self.assertTrue(r.description)
        named = {req for r in V.RULES for req in r.reqs}
        for n in range(1, 24):
            rid = f"REQ-001-{n:02d}"
            if rid in ("REQ-001-12", "REQ-001-15"):
                continue
            self.assertIn(rid, named, f"{rid} has no rule")
            self.assertIn(rid, out)

    def test_cross_repository_reference_REQ_001_15(self):
        self.assertEqual({"repo": "payments-api", "change": "014", "req": "REQ-03"}, V.parse_reference("payments-api:014/REQ-03"))
        self.assertEqual({"repo": None, "change": "014", "req": None}, V.parse_reference("014"))
        self.assertIsNone(V.parse_reference("payments-api/14"))


class TestLayoutNamingTiers(ValidatorCase):
    def test_layout_REQ_003_05_REQ_001_01(self):
        self.assert_clean()
        shutil.copy(VALIDATOR, self.fx.specs / "validate.py")
        self.assert_no_violation(self.run_validator(), "layout-entries")
        (self.fx.specs / "notes.md").write_text("stray\n")
        self.assert_violation(self.run_validator(), "layout-entries", "REQ-001-01", path="specs/notes.md")
        shutil.rmtree(self.fx.specs / "templates")
        self.assert_violation(self.run_validator(), "layout-entries", "REQ-001-01", text="missing templates")

    def test_change_dirname_REQ_003_06_REQ_001_02(self):
        self.assert_no_violation(self.run_validator(), "change-dirname")
        (self.fx.specs / "changes" / "12-Passwordless-Login").mkdir()
        self.assert_violation(self.run_validator(), "change-dirname", "REQ-001-02", path="12-Passwordless-Login")
        (self.fx.specs / "changes" / "stray.md").write_text("x\n")
        self.assert_violation(self.run_validator(), "layout-entries", "REQ-001-02", path="specs/changes/stray.md")

    def test_change_id_matches_prefix_REQ_003_06_REQ_001_02_REQ_001_07(self):
        ch = self.fx.add_change()
        self.assert_no_violation(self.run_validator(), "change-id")
        spec = ch.path / "spec.md"
        spec.write_text(spec.read_text().replace('id: "014"', 'id: "015"'))
        self.assert_violation(self.run_validator(), "change-id", "REQ-001-02")
        self.assert_violation(self.run_validator(), "change-id", "REQ-001-07")

    def test_ticket_numbering_REQ_007_03_REQ_001_02(self):
        self.fx.set_numbering("ticket")
        ch = self.fx.add_change("ABC-123", "passwordless_login")
        self.fx.add_tests_mentioning(self.fx.change_ids("ABC-123"))
        self.assert_clean()
        self.assertIn("REQ-ABC-123-01", (ch.path / "requirements.md").read_text())
        self.fx.set_numbering("sequential")
        self.assert_violation(self.run_validator(), "change-dirname", "REQ-001-02", path="ABC-123-passwordless_login")
        self.assertEqual({"repo": "payments-api", "change": "ABC-123", "req": "REQ-01"}, V.parse_reference("payments-api:ABC-123/REQ-01"))

    def test_number_collision_REQ_003_06_REQ_001_03_REQ_001_18(self):
        self.fx.add_change("012", "first")
        self.assert_no_violation(self.run_validator(), "change-number-unique")
        self.fx.add_change("012", "second", status="archived", location="archive")
        found = self.assert_violation(self.run_validator(), "change-number-unique", "REQ-001-18")
        self.assert_violation(found, req="REQ-001-03")
        self.assertEqual(2, len(found), "both directories are named")

    def test_tier_files_REQ_003_07_REQ_001_04_REQ_001_05(self):
        ch = self.fx.add_change()
        self.assert_no_violation(self.run_validator(), "change-files")
        (ch.path / "design.md").unlink()
        self.assert_violation(self.run_validator(), "change-files", "REQ-001-04", text="lacks design.md")
        quick = self.fx.add_change("015", "quick_one", tier="quick")
        self.assert_no_violation([v for v in self.run_validator() if "015" in v.path], "change-files")
        (quick.path / "requirements.md").write_text("# 015: Requirements\n")
        found = self.assert_violation(self.run_validator(), "change-files", "REQ-001-05", path="015-quick_one/requirements.md")
        self.assert_violation(found, req="REQ-001-04")
        full = self.fx.add_change("016", "full_one", tier="full")
        self.assert_no_violation([v for v in self.run_validator() if "016" in v.path], "change-files")
        (full.path / "extra.md").write_text("x\n")
        self.assert_violation(self.run_validator(), "change-files", "REQ-001-04", path="016-full_one/extra.md")


class TestSpecFile(ValidatorCase):
    def test_section_order_REQ_003_08_REQ_001_06(self):
        ch = self.fx.add_change()
        self.assert_no_violation(self.run_validator(), "spec-order")
        spec = ch.path / "spec.md"
        text = spec.read_text()
        swapped = text.replace("## Why it matters", "## TEMP").replace("## What should be done", "## Why it matters").replace("## TEMP", "## What should be done")
        spec.write_text(swapped)
        self.assert_violation(self.run_validator(), "spec-order", "REQ-001-06", text="sections are")
        spec.write_text(re.sub(r"(### Out\n(?:.*\n)*?)- item\n", r"\1", text, count=1))
        self.assert_violation(self.run_validator(), "spec-order", "REQ-001-06", text="non-goal")

    def test_frontmatter_REQ_003_09_REQ_001_07_REQ_001_16_REQ_001_17_REQ_001_12(self):
        ch = self.fx.add_change()
        spec = ch.path / "spec.md"
        base = spec.read_text()
        self.assert_no_violation(self.run_validator(), "spec-frontmatter")
        # REQ-001-12: optional links are accepted, empty or filled, including a Ref line on a requirement
        spec.write_text(base.replace("ticket: ", "ticket: https://tracker.example/ABC-123").replace("docs: ", "docs: https://wiki.example/page"))
        req = ch.path / "requirements.md"
        req.write_text(with_req(req.read_text(), req_block("REQ-014-03").replace("The system SHALL do the thing.", "The system SHALL do the thing.\nRef: https://wiki.example/req")))
        self.assert_no_violation(self.run_validator(), "spec-frontmatter")
        self.assert_no_violation(self.run_validator(), "requirement-grammar")
        spec.write_text(base.replace("approved_by: someone", "approved_by: "))
        self.assert_violation(self.run_validator(), "spec-frontmatter", "REQ-001-17")
        spec.write_text(base.replace("status: in-progress", "status: pending"))
        self.assert_violation(self.run_validator(), "spec-frontmatter", "REQ-001-16")
        spec.write_text(base.replace(f"created: {TODAY}", "created: 8 Nov 2026"))
        self.assert_violation(self.run_validator(), "spec-frontmatter", "REQ-001-07", text="created")
        spec.write_text(base.replace("owner: team-x\n", ""))
        self.assert_violation(self.run_validator(), "spec-frontmatter", "REQ-001-07", text="missing field owner")

    def test_block_style_list_is_reported_REQ_007_02(self):
        ch = self.fx.add_change()
        spec = ch.path / "spec.md"
        spec.write_text(spec.read_text().replace("capabilities: [auth]", "capabilities:\n  - auth"))
        self.assert_violation(self.run_validator(), "spec-frontmatter", "REQ-007-02", text="capabilities: [a, b]")


class TestRequirements(ValidatorCase):
    def test_grammar_REQ_003_10_REQ_001_08(self):
        ch = self.fx.add_change()
        self.assert_no_violation(self.run_validator(), "requirement-grammar")
        req = ch.path / "requirements.md"
        base = req.read_text()
        req.write_text(with_req(base, req_block("REQ-014-03", scenario=False)))
        self.assert_violation(self.run_validator(), "requirement-grammar", "REQ-001-08", text="REQ-014-03: no scenario")
        req.write_text(with_req(base, req_block("REQ-014-03", bullets=("GIVEN", "WHEN", "AND", "THEN", "AND"))))
        self.assert_no_violation(self.run_validator(), "requirement-grammar")
        req.write_text(with_req(base, req_block("REQ-014-03", bullets=("GIVEN", "THEN"))))
        self.assert_violation(self.run_validator(), "requirement-grammar", "REQ-001-08", text="missing WHEN")
        req.write_text(with_req(base, req_block("REQ-099-03")))
        self.assert_violation(self.run_validator(), "requirement-grammar", "REQ-001-08", text="numbered REQ-014-xx")
        req.write_text(base.replace("Changed in: 014", "Changed in: 013").replace("REQ-MMM-03", "REQ-013-03"))
        self.assert_violation(self.run_validator(), "requirement-grammar", "REQ-001-08", text="Changed in: 014")
        req.write_text(with_req(base, req_block("REQ-014-01")))
        self.assert_violation(self.run_validator(), "requirement-grammar", "REQ-001-10", text="appears twice")
        req.write_text(with_req(base, req_block("REQ-014-03").replace("The system SHALL do the thing.", "The system does the thing.")))
        self.assert_violation(self.run_validator(), "requirement-grammar", "REQ-001-08", text="one SHALL statement")

    def test_grouping_REQ_003_11_REQ_001_09(self):
        ch = self.fx.add_change()
        self.assert_no_violation(self.run_validator(), "requirement-grouping")
        req = ch.path / "requirements.md"
        base = req.read_text()
        req.write_text(base.replace("## Capability: auth", "## Capability: billing"))
        self.assert_violation(self.run_validator(), "requirement-grouping", "REQ-001-09", text="billing")
        req.write_text(base.replace("## Not testable", "## Untestable"))
        self.assert_violation(self.run_validator(), "requirement-grouping", "REQ-001-09", text="Not testable")
        req.write_text(req_block("REQ-014-09") + base)
        self.assert_violation(self.run_validator(), "requirement-grouping", "REQ-001-09", text="REQ-014-09: outside")

    def test_new_ids_are_not_reused_REQ_003_10_REQ_001_10(self):
        self.fx.add_capability("auth", blocks=[req_block("REQ-014-01", origin="014")])
        self.fx.add_change()
        self.assert_violation(self.run_validator(), "requirement-id-new", "REQ-001-10", text="REQ-014-01 already exists")


class TestCapabilities(ValidatorCase):
    def test_structure_REQ_003_12_REQ_001_11(self):
        cap = self.fx.add_capability("auth", blocks=[req_block("REQ-003-02", origin="003")])
        self.assert_clean()
        spec = cap.path / "spec.md"
        base = spec.read_text()
        spec.write_text(base.replace("Origin: 003\n", ""))
        self.assert_violation(self.run_validator(), "capability-structure", "REQ-001-11", text="no Origin")
        spec.write_text(base.replace("## Retired", "## Removed"))
        self.assert_violation(self.run_validator(), "capability-structure", "REQ-001-11", text="sections are")
        spec.write_text(base.replace("id: auth", "id: identity"))
        self.assert_violation(self.run_validator(), "capability-structure", "REQ-001-11", text="directory says auth")
        (cap.path / "spec.md").unlink()
        self.assert_violation(self.run_validator(), "capability-structure", "REQ-001-11", text="no spec.md")

    def test_ids_unique_across_capabilities_REQ_003_12_REQ_001_10(self):
        self.fx.add_capability("a", blocks=[req_block("REQ-003-02", origin="003")])
        self.assert_no_violation(self.run_validator(), "requirement-id-unique")
        self.fx.add_capability("b", retired=["REQ-003-02"])
        self.assert_violation(self.run_validator(), "requirement-id-unique", "REQ-001-10", text="retired here but active in a")
        self.fx.add_capability("c", blocks=[req_block("REQ-003-02", origin="003")])
        self.assert_violation(self.run_validator(), "requirement-id-unique", "REQ-001-10", text="also active in a")


class TestStatus(ValidatorCase):
    def test_draft_holds_spec_only_REQ_003_13_REQ_001_19(self):
        ch = self.fx.add_change(status="draft")
        self.assert_clean()
        (ch.path / "design.md").write_text("# 014: Design\n")
        self.assert_violation(self.run_validator(), "status-draft", "REQ-001-19", path="014-sample_change/design.md")

    def test_done_requires_tasks_gate_and_coverage_REQ_003_13_REQ_001_20(self):
        ch = self.fx.add_change(status="done")
        self.fx.add_tests_mentioning(self.fx.change_ids("014"))
        self.assert_clean()
        tasks = ch.path / "tasks.md"
        tasks.write_text(tasks.read_text().replace("- [x] T02", "- [ ] T02"))
        self.assert_violation(self.run_validator(), "status-done", "REQ-001-20", text="T02 is not ticked")
        tasks.write_text(tasks.read_text().replace("- [ ] T02", "- [x] T02"))
        checklist = ch.path / "checklist.md"
        checklist.write_text(checklist.read_text().replace("- [x] Every task in tasks.md is ticked", "- [ ] Every task in tasks.md is ticked"))
        self.assert_violation(self.run_validator(), "status-done", "REQ-001-20", text="Gate 2 items not ticked")
        checklist.write_text(checklist.read_text().replace("- [ ] Every task", "- [x] Every task"))
        req = ch.path / "requirements.md"
        req.write_text(with_req(req.read_text(), req_block("REQ-014-03")))
        self.assert_violation(self.run_validator(), "status-done", "REQ-001-20", text="REQ-014-03: no test references it")
        req.write_text(req.read_text().replace("## Not testable\n", "## Not testable\n\n- REQ-014-03: needs a person.\n"))
        self.assert_no_violation(self.run_validator(), "status-done")

    def test_exemptions_are_explicit_REQ_008_01_REQ_003_13(self):
        ch = self.fx.add_change(status="done")
        self.fx.add_tests_mentioning(self.fx.change_ids("014"))
        req = ch.path / "requirements.md"
        base = with_req(req.read_text(), req_block("REQ-014-03"))
        req.write_text(base.replace("## Not testable\n", "## Not testable\n\nREQ-014-03 is hard to test.\n"))
        found = self.run_validator()
        self.assert_violation(found, "exemption-form", "REQ-008-01", text="- REQ-014-03: reason")
        self.assert_violation(found, "status-done", "REQ-001-20", text="REQ-014-03")
        req.write_text(base.replace("## Not testable\n", "## Not testable\n\n- REQ-014-03: needs a person to judge readability.\n"))
        self.assert_no_violation(self.run_validator(), "exemption-form")
        self.assert_no_violation(self.run_validator(), "status-done")

    def test_id_only_in_a_comment_does_not_count_REQ_003_13_REQ_001_20(self):
        ch = self.fx.add_change(status="done")
        ids = self.fx.change_ids("014")
        self.fx.add_tests_mentioning(ids)
        self.assert_clean()
        (self.fx.root / "tests" / "test_comment.py").write_text("# REQ-014-03 is mentioned here only in a comment\n")
        req = ch.path / "requirements.md"
        req.write_text(with_req(req.read_text(), req_block("REQ-014-03")))
        self.assert_violation(self.run_validator(), "status-done", "REQ-001-20", text="REQ-014-03: no test references it")
        (self.fx.root / "tests" / "test_comment.py").write_text("def test_REQ_014_03(): pass\n")
        self.assert_no_violation(self.run_validator(), "status-done")

    def test_archived_requires_location_merge_and_gate3_REQ_003_13_REQ_001_21(self):
        ch = self.fx.add_change(status="archived", location="archive")
        self.fx.add_tests_mentioning(self.fx.change_ids("014"))
        self.assert_violation(self.run_validator(), "status-archived", "REQ-001-21", text="REQ-014-01: not found in any capability")
        self.fx.add_capability("auth", blocks=[req_block(rid, origin="014") for rid in self.fx.change_ids("014")])
        self.assert_clean()
        spec = ch.path / "spec.md"
        base = spec.read_text()
        spec.write_text(base.replace("status: archived", "status: done"))
        self.assert_violation(self.run_validator(), "status-archived", "REQ-001-21", text="under specs/archive/ but status is done")
        spec.write_text(base)
        checklist = ch.path / "checklist.md"
        checklist.write_text(checklist.read_text().replace("- [x] INDEX.md is regenerated", "- [ ] INDEX.md is regenerated"))
        self.assert_violation(self.run_validator(), "status-archived", "REQ-001-21", text="Gate 3 items not ticked")
        by_hand = self.fx.add_change("015", "by_hand", status="archived", location="changes")
        self.fx.add_tests_mentioning(self.fx.change_ids("014") + self.fx.change_ids("015"))
        self.assert_violation(self.run_validator(), "status-archived", "REQ-001-21", path="015-by_hand", text="still under specs/changes/")

    def test_archived_modified_and_removed_REQ_003_13_REQ_001_21(self):
        self.fx.add_capability("auth", blocks=[req_block("REQ-010-01", origin="010"), req_block("REQ-010-02", origin="010"),
                                               req_block("REQ-014-01", origin="014"), req_block("REQ-014-02", origin="014")])
        modified = req_block("REQ-010-01", changed_in="014")
        extra = f"\n## Modified requirements\n\n{modified}\n## Removed requirements\n\n- REQ-010-02: obsolete.\n\n## Not testable\n"
        ch = self.fx.add_change(status="archived", location="archive")
        req = ch.path / "requirements.md"
        text = req.read_text()
        text = text[:text.index("## Modified requirements")] + extra.lstrip("\n")
        req.write_text(text)
        self.fx.add_tests_mentioning(["REQ-014-01", "REQ-014-02", "REQ-010-01"])
        found = self.run_validator()
        self.assert_violation(found, "status-archived", "REQ-001-21", text="REQ-010-01: capability copy lacks 'Changed in: 014'")
        self.assert_violation(found, "status-archived", "REQ-001-21", text="REQ-010-02: removed here but not under Retired")

    @unittest.skipUnless(GIT, "git not available")
    def test_backward_transition_REQ_003_13_REQ_001_16(self):
        ch = self.fx.add_change(status="done")
        self.fx.add_tests_mentioning(self.fx.change_ids("014"))
        self.fx.git_init_and_commit("Done\n\nChange: 014")
        self.assert_no_violation(self.run_validator(), "status-forward")
        spec = ch.path / "spec.md"
        spec.write_text(spec.read_text().replace("status: done", "status: in-progress"))
        self.assert_violation(self.run_validator(), "status-forward", "REQ-001-16", text="from done to in-progress")


class TestIndexConstitutionAgents(ValidatorCase):
    def test_index_REQ_003_14_REQ_001_14(self):
        ch = self.fx.add_change()
        self.fx.add_capability("auth", blocks=[req_block("REQ-003-01", origin="003")])
        self.assert_clean()
        index = self.fx.specs / "INDEX.md"
        base = index.read_text()
        index.write_text(base.replace("| in-progress |", "| approved |"))
        self.assert_violation(self.run_validator(), "index", "REQ-001-14", path="specs/INDEX.md", text="change 014: status")
        index.write_text(base.replace("| 1 |", "| 3 |"))
        self.assert_violation(self.run_validator(), "index", "REQ-001-14", text="capability auth: 3 requirements")
        index.write_text(base.replace("0 archived", "2 archived"))
        self.assert_violation(self.run_validator(), "index", "REQ-001-14", text="archived count")
        index.write_text("\n".join(l for l in base.splitlines() if not l.startswith("| 014 |")) + "\n")
        self.assert_violation(self.run_validator(), "index", "REQ-001-14", text="change 014 has no row")
        index.write_text(base.replace("## Capabilities", "## Things"))
        self.assert_violation(self.run_validator(), "index", "REQ-001-14", text="missing section 'Capabilities'")

    def test_constitution_REQ_003_15_REQ_001_13(self):
        self.assert_clean()
        const = self.fx.specs / "constitution.md"
        base = const.read_text()
        const.write_text(base + "\n".join(f"- filler line {i}" for i in range(120)) + "\n")
        self.assert_violation(self.run_validator(), "constitution", "REQ-001-13", text="lines")
        const.write_text(base.replace("numbering: sequential", "numbering_scheme: sequential"))
        self.assert_violation(self.run_validator(), "constitution", "REQ-001-13", text="missing field numbering")
        const.write_text(base.replace("## Definitions", "## Glossary"))
        self.assert_violation(self.run_validator(), "constitution", "REQ-001-13", text="sections are")

    def test_agents_file_REQ_003_15_REQ_001_22(self):
        self.assert_clean()
        agents = self.fx.root / "AGENTS.md"
        agents.write_text("# Agents\n\nRead everything.\n")
        self.assert_violation(self.run_validator(), "agents-file", "REQ-001-22", text="specs/INDEX.md")
        agents.unlink()
        self.assert_violation(self.run_validator(), "agents-file", "REQ-001-22", text="missing")


class TestGitAndSkills(ValidatorCase):
    @unittest.skipUnless(GIT, "git not available")
    def test_commit_trailers_REQ_003_16_REQ_001_23(self):
        ch = self.fx.add_change()
        self.fx.git_init_and_commit("Start change\n\nChange: 014")
        self.assert_no_violation(self.run_validator(), "commit-trailers")
        (ch.path / "tasks.md").write_text((ch.path / "tasks.md").read_text() + "\n- [ ] T99 Extra [setup]\n")
        self.fx.git("add", "-A")
        self.fx.git("commit", "-q", "-m", "Tick a task without the trailer")
        found = self.assert_violation(self.run_validator(), "commit-trailers", "REQ-001-23", text="touches change 014")
        self.assertTrue(found[0].path.startswith("commit "))

    @unittest.skipUnless(GIT, "git not available")
    def test_nested_project_skips_git_checks_REQ_003_13_REQ_003_16(self):
        self.fx.add_change(status="done")
        self.fx.add_tests_mentioning(self.fx.change_ids("014"))
        self.fx.git_init_and_commit("Done\n\nChange: 014")
        nested = self.fx.root / "examples" / "inner"
        nested.mkdir(parents=True)
        shutil.copytree(self.fx.specs, nested / "specs")
        (nested / "AGENTS.md").write_text((self.fx.root / "AGENTS.md").read_text())
        violations, stats = V.validate(nested)
        self.assertFalse(stats["git"], "a project nested in another repository has no history of its own")
        self.assert_no_violation(violations, "commit-trailers")

    def test_refusal_wording_present_REQ_008_02(self):
        plan = (ROOT / "skills/sdd-plan/SKILL.md").read_text()
        impl = (ROOT / "skills/sdd-implement/SKILL.md").read_text()
        init = (ROOT / "skills/sdd-init/SKILL.md").read_text()
        self.assertIn("approver confirms it", plan)
        self.assertIn("cites an ID that no requirement defines", impl)
        self.assertIn("exists and is not empty", init)

    def test_skills_REQ_003_17_REQ_002_01_REQ_002_02_REQ_002_03(self):
        skills = self.fx.root / "skills"
        shutil.copytree(ROOT / "skills" / "sdd-new", skills / "sdd-new")
        self.assert_no_violation(self.run_validator(), "skills")
        skill = skills / "sdd-new" / "SKILL.md"
        base = skill.read_text()
        skill.write_text(base.replace("## Steps", "## How"))
        self.assert_violation(self.run_validator(), "skills", "REQ-002-02", text="sections are")
        skill.write_text(base + "\nAlso copy this into .claude/skills when done.\n")
        self.assert_violation(self.run_validator(), "skills", "REQ-002-03", text=".claude")
        skill.write_text(base + "\nWorks best with Devin.\n")
        self.assert_violation(self.run_validator(), "skills", "REQ-002-03", text="names Devin")
        skill.write_text(base + "\n" * 160)
        self.assert_violation(self.run_validator(), "skills", "REQ-002-01", text="lines, limit 150")
        skill.write_text(base.replace("name: sdd-new", "name: sdd-start"))
        self.assert_violation(self.run_validator(), "skills", "REQ-002-01", text="name is 'sdd-start'")
        skill.write_text(re.sub(r"^  sdd_version: .*\n", "", base, flags=re.M))
        self.assert_violation(self.run_validator(), "skills", "REQ-002-01", text="missing metadata.sdd_version")


class TestInstallAndMeta(ValidatorCase):
    def test_install_copies_validator_and_sets_key_REQ_003_18(self):
        result = subprocess.run(["sh", str(ROOT / "install.sh"), str(self.fx.root)], capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertTrue((self.fx.specs / "validate.py").is_file())
        self.assertIn("validator: python3 specs/validate.py", (self.fx.specs / "constitution.md").read_text())
        self.assertTrue((self.fx.root / ".agents" / "skills" / "sdd-init" / "templates" / "constitution.md").is_file())
        self.assert_clean()

    def test_this_file_names_every_requirement_REQ_003_19(self):
        source = Path(__file__).read_text()
        normalised = source.replace("_", "-")  # test names cannot contain hyphens, so REQ_003_01 counts as REQ-003-01
        for n in range(1, 21):
            self.assertIn(f"REQ-003-{n:02d}", normalised)
        for n in range(1, 24):
            self.assertIn(f"REQ-001-{n:02d}", normalised)
        for req in {req for r in V.RULES for req in r.reqs}:
            self.assertIn(req, normalised)
        names = {r.id for r in V.RULES}
        for rule_id in names:
            self.assertIn(f'"{rule_id}"', source, f"no test mentions rule {rule_id}")

    def test_empty_layout_folders_are_tracked_REQ_001_01(self):
        # Git drops empty directories, so a fresh clone must still see all six entries under specs/.
        tracked = subprocess.run(["git", "ls-files", "specs"], cwd=ROOT, capture_output=True, text=True).stdout.split()
        for folder in ("capabilities", "changes", "archive"):
            self.assertIn(f"specs/{folder}/.gitkeep", tracked, f"specs/{folder} would vanish from a clone")

    def test_this_repository_is_clean_REQ_003_20(self):
        violations, stats = V.validate(ROOT)
        self.assertEqual([], [v.format() for v in violations])
        self.assertTrue(stats["rules"] >= 21)


if __name__ == "__main__":
    unittest.main()
