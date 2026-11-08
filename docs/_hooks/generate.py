"""MkDocs hook: generate the skills, templates and validator pages from their sources at build time.

One copy of every rule (REQ-004-06). Edit skills/*/SKILL.md, specs/templates/ or specs/validate.py;
never the generated pages. The render functions are pure so the test suite can call them without MkDocs.
"""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = ROOT / "skills"
TEMPLATES_DIR = ROOT / "specs" / "templates"
VALIDATOR = ROOT / "specs" / "validate.py"
GENERATED_NOTE = "<!-- Generated at build time from {source}. Edit the source, not this page. -->\n\n"
CAPABILITIES_DIR = ROOT / "specs" / "capabilities"
REPO_BLOB = "https://github.com/eaceto/spec-driven-development/blob/main"
SKILL_PROMPTS = {  # REQ-009-06: what a person says to the agent to reach each skill
    "sdd-init": "Set up spec-driven development in this project.",
    "sdd-new": "Start a change: <what you want, in two or three sentences>.",
    "sdd-plan": "Plan change 001.",
    "sdd-implement": "Implement the next task of change 001.",
    "sdd-verify": "Verify change 001.",
    "sdd-archive": "Archive change 001.",
}


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
    prompt = SKILL_PROMPTS.get(name)
    say = f"\n**Say to your agent:** \"{prompt}\"\n" if prompt else ""
    note = f'\n!!! info "When an agent reaches for it"\n    {trigger}\n' if trigger else ""
    return GENERATED_NOTE.format(source=f"skills/{name}/SKILL.md") + heading + "\n" + say + note + rest


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


def capability_of_requirements(capabilities_dir: Path = CAPABILITIES_DIR) -> dict:
    """Map every requirement id found in a capability spec to that capability's id. REQ-009-07."""
    out = {}
    if not capabilities_dir.is_dir():
        return out
    for spec in sorted(capabilities_dir.glob("*/spec.md")):
        for m in re.finditer(r"^### (REQ-[A-Z0-9-]+?-\d{2,}):", spec.read_text(encoding="utf-8"), flags=re.M):
            out.setdefault(m.group(1), spec.parent.name)
    return out


def link_requirement(req_id: str, where: dict) -> str:
    cap = where.get(req_id)
    return f"[{req_id}]({REPO_BLOB}/specs/capabilities/{cap}/spec.md)" if cap else req_id


def render_rules(rules, where=None) -> str:
    where = capability_of_requirements() if where is None else where
    page = GENERATED_NOTE.format(source="specs/validate.py") + "# Validator rules\n\n"
    page += ("What `python3 specs/validate.py` checks, generated from the validator's own rule list. "
             "Each rule names the requirement of the method it enforces, so a violation tells you what is wrong and why the rule exists.\n\n")
    page += "| Rule | Enforces | Checks that |\n|---|---|---|\n"
    for r in rules:
        page += f"| `{r.id}` | {', '.join(link_requirement(q, where) for q in r.reqs)} | {r.description} |\n"
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
