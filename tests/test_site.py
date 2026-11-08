"""Tests for the teaching site (change 004): configuration, generated pages, reading time, UK spelling.

They need no MkDocs install: the hook's render functions are plain Python and the configuration is read as text.
Run: python3 -m unittest discover tests
"""
import importlib.util
import re
import sys
import unittest
from pathlib import Path

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
MKDOCS_YML = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")

WORD_LIMIT = 1000  # REQ-004-09: an authored page reads in under five minutes
EXCLUDED_FROM_LIMIT = {"method.md"}  # the included reference, REQ-004-06
US_SPELLINGS = re.compile(  # REQ-004-10
    r"\b(color|colors|behavior|behaviors|center|centered|favor|favorite|analyze|analyzed|organize|organized|organizing|"
    r"organization|initialize|initialized|recognize|recognized|optimize|optimized|standardize|customize|customized|"
    r"honor|catalog|license)\b", re.IGNORECASE)


def load_hook():
    spec = importlib.util.spec_from_file_location("sdd_site_hook", DOCS / "_hooks" / "generate.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


HOOK = load_hook()


def authored_pages():
    return sorted(p for p in DOCS.rglob("*.md") if "_hooks" not in p.parts)


class TestConfiguration(unittest.TestCase):
    def test_title_and_address_REQ_004_12(self):
        self.assertIn("site_name: Spec-driven development", MKDOCS_YML)
        self.assertIn("site_url: https://eaceto.github.io/spec-driven-development/", MKDOCS_YML)

    def test_strict_and_pinned_dependencies_REQ_004_01_REQ_004_02(self):
        self.assertIn("strict: true", MKDOCS_YML)
        requirements = (ROOT / "requirements-site.txt").read_text().splitlines()
        self.assertTrue(requirements)
        for line in requirements:
            self.assertRegex(line, r"^[A-Za-z0-9_.-]+==\d", f"not pinned exactly: {line}")
        self.assertTrue(any(l.startswith("mkdocs-material==") for l in requirements))

    def test_mermaid_fences_are_configured_REQ_004_11(self):
        self.assertIn("name: mermaid", MKDOCS_YML)
        self.assertIn("class: mermaid", MKDOCS_YML)
        self.assertIn("```mermaid", (DOCS / "index.md").read_text(encoding="utf-8"))

    def test_hook_is_registered_and_pages_are_in_nav_REQ_004_06(self):
        self.assertIn("docs/_hooks/generate.py", MKDOCS_YML)
        for page in ("skills/index.md", "reference/templates.md", "reference/validator-rules.md", "method.md"):
            self.assertIn(page, MKDOCS_YML)

    def test_workflows_REQ_004_01_REQ_004_13(self):
        pages = (ROOT / ".github/workflows/pages.yml").read_text()
        checks = (ROOT / ".github/workflows/checks.yml").read_text()
        self.assertIn("mkdocs build --strict", pages)
        self.assertIn("deploy-pages", pages)
        self.assertIn("branches: [main]", pages)
        self.assertIn("pull_request", checks)
        self.assertIn("python3 specs/validate.py", checks)
        self.assertIn("unittest discover tests", checks)
        self.assertIn("mkdocs build --strict", checks)


class TestGeneratedPages(unittest.TestCase):
    def test_skill_page_is_the_skill_body_REQ_004_06(self):
        source = (ROOT / "skills/sdd-new/SKILL.md").read_text(encoding="utf-8")
        page = HOOK.render_skill("sdd-new", source)
        self.assertNotIn("sdd_version", page, "frontmatter is stripped")
        self.assertIn("# sdd-new", page)
        self.assertIn("## Steps", page)
        body = HOOK.split_frontmatter(source)[1]
        steps = body[body.index("## Steps"):]
        self.assertIn(steps.strip(), page, "the body is included unchanged")
        self.assertIn("Generated at build time", page)

    def test_rules_page_lists_every_rule_REQ_004_06(self):
        rules = HOOK.load_rules()
        page = HOOK.render_rules(rules)
        for r in rules:
            self.assertIn(f"`{r.id}`", page)
            for req in r.reqs:
                self.assertIn(req, page)

    def test_templates_page_includes_every_template_REQ_004_06(self):
        page = HOOK.render_templates(ROOT / "specs/templates")
        for path in (ROOT / "specs/templates").rglob("*.md"):
            self.assertIn(f"## `{path.relative_to(ROOT / 'specs/templates').as_posix()}`", page)
            self.assertIn(path.read_text(encoding="utf-8").strip()[:60], page)

    def test_generated_set_REQ_004_06(self):
        pages = HOOK.generated_pages()
        for name in ("sdd-init", "sdd-new", "sdd-plan", "sdd-implement", "sdd-verify", "sdd-archive"):
            self.assertIn(f"skills/{name}.md", pages)
        self.assertIn("skills/index.md", pages)
        self.assertIn("reference/templates.md", pages)
        self.assertIn("reference/validator-rules.md", pages)


class TestAuthoredPages(unittest.TestCase):
    def test_reading_time_REQ_004_09(self):
        over = []
        for page in authored_pages():
            if page.name in EXCLUDED_FROM_LIMIT:
                continue
            words = len(page.read_text(encoding="utf-8").split())
            if words > WORD_LIMIT:
                over.append(f"{page.relative_to(ROOT)}: {words} words")
        self.assertEqual([], over)

    def test_uk_spelling_REQ_004_10(self):
        hits = []
        for page in authored_pages():
            for n, line in enumerate(page.read_text(encoding="utf-8").splitlines(), 1):
                if line.strip().startswith(("http", "[", "|")) and "github.com" in line:
                    continue
                for m in US_SPELLINGS.finditer(line):
                    hits.append(f"{page.relative_to(ROOT)}:{n}: {m.group(0)}")
        self.assertEqual([], hits)

    def test_home_page_order_and_agents_REQ_004_03_REQ_004_07(self):
        home = (DOCS / "index.md").read_text(encoding="utf-8")
        what, tutorial, reference = home.index("## What it is"), home.index("## Your first change"), home.index("## The reference")
        self.assertTrue(what < tutorial < reference)
        self.assertIn("Claude Code", home)
        self.assertIn("untested", home)
        agents = (DOCS / "agents.md").read_text(encoding="utf-8")
        self.assertIn("## Tested", agents)
        self.assertIn("Untested", agents)

    def test_entry_pages_exist_REQ_004_05(self):
        for name in ("for-developers.md", "for-team-leads.md"):
            text = (DOCS / name).read_text(encoding="utf-8")
            self.assertIn("tutorial/", text)
            self.assertIn("method.md", text)

    def test_example_page_and_folder_REQ_004_08(self):
        self.assertTrue((ROOT / "examples/greenfield-go/specs/capabilities/greeting/spec.md").is_file())
        page = (DOCS / "examples/greenfield-go.md").read_text(encoding="utf-8")
        self.assertIn("examples/greenfield-go", page)

    def test_notes_example_validates_and_is_linked_REQ_007_01(self):
        import subprocess
        result = subprocess.run([sys.executable, "-B", str(ROOT / "specs/validate.py"), "--root", str(ROOT / "examples/notes-python")],
                                capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stdout)
        self.assertIn("notes-python", (DOCS / "tutorial/06-verify-archive.md").read_text(encoding="utf-8"))
        self.assertTrue((DOCS / "examples/notes-python.md").is_file())

    def test_home_first_screen_REQ_009_01(self):
        home = (DOCS / "index.md").read_text(encoding="utf-8")
        first_para = home.split("\n\n")[2]
        self.assertIn("agent", first_para.lower())
        self.assertIn("coding assistants", first_para)
        button = home.index("{ .md-button")
        self.assertLess(home.index("## Why adopt it"), button)
        after = home[button:button + 600]
        for word in ("git", "Python", "minutes"):
            self.assertIn(word, after)

    def test_glossary_and_single_devin_note_REQ_009_02(self):
        overview = (DOCS / "tutorial/index.md").read_text(encoding="utf-8")
        for term in ("**Change**", "**Capability**", "**Gate**", "**Tier**", "**Statuses**"):
            self.assertIn(term, overview)
        for page in (DOCS / "tutorial").glob("*.md"):
            self.assertNotIn("being added", page.read_text(encoding="utf-8"), page.name)

    def test_refusal_shown_on_step_3_REQ_009_03(self):
        step = (DOCS / "tutorial/03-new.md").read_text(encoding="utf-8")
        self.assertIn("## Try to skip the approval", step)
        self.assertIn("Gate 1", step[step.index("## Try to skip the approval"):])
        self.assertRegex(step[step.index("## Try to skip the approval"):], r"8 November 2026")

    def test_no_product_comparisons_REQ_009_04(self):
        import re as _re
        pattern = _re.compile(r"spec-kit|\bkiro\b|openspec", _re.IGNORECASE)
        for page in authored_pages() + [ROOT / "README.md"]:
            self.assertIsNone(pattern.search(page.read_text(encoding="utf-8")), page)

    def test_adoption_and_questions_pages_REQ_009_05(self):
        for name in ("adopting.md", "questions.md"):
            page = DOCS / name
            self.assertTrue(page.is_file())
            self.assertLess(len(page.read_text(encoding="utf-8").split()), WORD_LIMIT)
            self.assertIn(name, MKDOCS_YML)

    def test_skill_pages_open_with_the_request_REQ_009_06(self):
        page = HOOK.render_skill("sdd-new", (ROOT / "skills/sdd-new/SKILL.md").read_text(encoding="utf-8"))
        self.assertLess(page.index("Say to your agent"), page.index("## When to use"))

    def test_rule_ids_link_to_capabilities_REQ_009_07(self):
        where = HOOK.capability_of_requirements()
        self.assertEqual("spec-layout", where.get("REQ-001-02"))
        page = HOOK.render_rules(HOOK.load_rules(), where)
        self.assertIn("[REQ-001-02](https://github.com/eaceto/spec-driven-development/blob/main/specs/capabilities/spec-layout/spec.md)", page)

    def test_example_pages_carry_no_counts_REQ_009_08(self):
        import re as _re
        for name in ("greenfield-go.md", "notes-python.md"):
            text = (DOCS / "examples" / name).read_text(encoding="utf-8")
            self.assertIsNone(_re.search(r"\d+ violations, \d+ files, \d+ rules", text), name)

    def test_logo_and_favicon_REQ_009_09(self):
        self.assertIn("logo: material/", MKDOCS_YML)
        self.assertIn("favicon: assets/favicon.svg", MKDOCS_YML)
        self.assertTrue((DOCS / "assets/favicon.svg").is_file())

    def test_tutorial_steps_state_agent_and_date_REQ_004_04(self):
        steps = sorted((DOCS / "tutorial").glob("0*.md"))
        self.assertTrue(steps)
        for step in steps[1:]:  # step 1 installs files and has no agent transcript
            text = step.read_text(encoding="utf-8")
            self.assertIn('=== "Claude Code"', text, step.name)
            self.assertIn('=== "Devin CLI"', text, step.name)
            self.assertRegex(text, r"\d{1,2} November 2026|2026-11-\d{2}", step.name)


if __name__ == "__main__":
    unittest.main()
