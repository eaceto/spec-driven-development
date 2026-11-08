"""MkDocs hook: generate the skills, templates and validator pages from their sources at build time.

One copy of every rule (REQ-004-06). Edit skills/*/SKILL.md, specs/templates/ or specs/validate.py;
never the generated pages. The render functions are pure so the test suite can call them without MkDocs.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = ROOT / "skills"
TEMPLATES_DIR = ROOT / "specs" / "templates"
VALIDATOR = ROOT / "specs" / "validate.py"
GENERATED_NOTE = "<!-- Generated at build time from {source}. Edit the source, not this page. -->\n\n"


def split_frontmatter(text: str):
    """Return (fields, body) for a file with a --- frontmatter block; fields is a flat dict of top-level keys."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    fields = {}
    for line in text[3:end].splitlines():
        if line.startswith(" ") or ":" not in line:
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields, text[end + 4:].lstrip("\n")


def render_skill(name: str, text: str) -> str:
    fields, body = split_frontmatter(text)
    first_newline = body.find("\n")
    heading, rest = body[:first_newline], body[first_newline + 1:]
    trigger = fields.get("description", "")
    note = f'\n!!! info "When an agent reaches for it"\n    {trigger}\n' if trigger else ""
    return GENERATED_NOTE.format(source=f"skills/{name}/SKILL.md") + heading + "\n" + note + rest


def render_skills_index(names) -> str:
    rows = "\n".join(f"- [`{n}`]({n}.md)" for n in names)
    return (GENERATED_NOTE.format(source="skills/") + "# Skills\n\nSix procedures, one per step of the lifecycle. "
            "Each page is the skill file itself, so what an agent reads is what you read.\n\n" + rows + "\n")


def render_templates(templates_dir: Path) -> str:
    page = GENERATED_NOTE.format(source="specs/templates/") + "# Templates\n\n"
    page += ("Every file below is copied from `specs/templates/` when the site is built. "
             "The comments inside are the guidance an author sees when creating a change; the skills copy these files into a project.\n\n")
    for path in sorted(p for p in templates_dir.rglob("*.md")):
        rel = path.relative_to(templates_dir).as_posix()
        page += f"## `{rel}`\n\n````markdown\n{path.read_text(encoding='utf-8').rstrip()}\n````\n\n"
    return page


def load_rules():
    spec = importlib.util.spec_from_file_location("sdd_validate_for_docs", VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    sys.dont_write_bytecode = True
    spec.loader.exec_module(module)
    return module.RULES


def render_rules(rules) -> str:
    page = GENERATED_NOTE.format(source="specs/validate.py") + "# Validator rules\n\n"
    page += ("What `python3 specs/validate.py` checks, generated from the validator's own rule list. "
             "Each rule names the requirement of the method it enforces, so a violation tells you what is wrong and why the rule exists.\n\n")
    page += "| Rule | Enforces | Checks that |\n|---|---|---|\n"
    for r in rules:
        page += f"| `{r.id}` | {', '.join(r.reqs)} | {r.description} |\n"
    return page


def generated_pages() -> dict:
    pages = {}
    names = sorted(p.name for p in SKILLS_DIR.iterdir() if p.is_dir() and (p / "SKILL.md").is_file())
    for name in names:
        pages[f"skills/{name}.md"] = render_skill(name, (SKILLS_DIR / name / "SKILL.md").read_text(encoding="utf-8"))
    pages["skills/index.md"] = render_skills_index(names)
    pages["reference/templates.md"] = render_templates(TEMPLATES_DIR)
    pages["reference/validator-rules.md"] = render_rules(load_rules())
    return pages


def on_files(files, config):
    from mkdocs.structure.files import File
    for uri, content in generated_pages().items():
        files.append(File.generated(config, uri, content=content))
    return files
