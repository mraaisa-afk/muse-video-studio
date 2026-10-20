#!/usr/bin/env python3
"""
validate_skill.py — repository self-check.

Verifies that the skill package obeys the Agent Skills format and that every
file it references actually exists. Run it before every release and in CI.

    python3 scripts/validate_skill.py
    python3 scripts/validate_skill.py --skill skills/video-studio

Exit 0 = valid, 1 = problems found, 2 = skill not found.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
LINK_RE = re.compile(r"`((?:references|presets|assets|scripts)/[^`]+?\.(?:md|json|py|sh))`")

REQUIRED_FILES = ["SKILL.md"]
RECOMMENDED = ["README.md", "INSTALL.md"]


def parse_frontmatter(text: str) -> tuple[dict, str, list[str]]:
    errors: list[str] = []
    if not text.startswith("---"):
        return {}, text, ["SKILL.md must start with a --- frontmatter block"]
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text, ["frontmatter block is not closed with ---"]
    raw = text[3:end].strip()
    body = text[end + 4:]
    data: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        m = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        if val.startswith('"') and val.endswith('"'):
            val = val[1:-1]
        data[key] = val
    return data, body, errors


def validate(skill_dir: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    notes: list[str] = []

    if not skill_dir.is_dir():
        return [f"skill directory not found: {skill_dir}"], notes

    for f in REQUIRED_FILES:
        if not (skill_dir / f).exists():
            errors.append(f"missing required file: {f}")
    for f in RECOMMENDED:
        if not (skill_dir / f).exists():
            notes.append(f"recommended file missing: {f}")

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return errors, notes

    text = skill_md.read_text(encoding="utf-8")
    fm, _body, fm_errors = parse_frontmatter(text)
    errors.extend(fm_errors)

    name = fm.get("name", "")
    if not name:
        errors.append("frontmatter: 'name' is required")
    else:
        if not NAME_RE.match(name):
            errors.append(f"frontmatter: name '{name}' must be lowercase letters, digits and hyphens")
        if len(name) > 64:
            errors.append(f"frontmatter: name is {len(name)} chars (limit 64)")
        if name != skill_dir.name:
            errors.append(f"frontmatter: name '{name}' must match the folder name '{skill_dir.name}'")

    desc = fm.get("description", "")
    if not desc:
        errors.append("frontmatter: 'description' is required")
    else:
        if len(desc) > 1024:
            errors.append(f"frontmatter: description is {len(desc)} chars (limit 1024)")
        if len(desc) < 120:
            notes.append("description is short — trigger matching will be weak")

    # every referenced file must exist
    missing = []
    for rel in sorted(set(LINK_RE.findall(text))):
        if not (skill_dir / rel).exists():
            missing.append(rel)
    for m in missing:
        errors.append(f"SKILL.md references a file that does not exist: {m}")

    # no empty reference files
    for sub in ("references", "presets"):
        d = skill_dir / sub
        if d.is_dir():
            for f in d.rglob("*.md"):
                if f.stat().st_size < 200:
                    notes.append(f"thin reference file: {f.relative_to(skill_dir)}")

    notes.append(f"files: {sum(1 for _ in skill_dir.rglob('*') if _.is_file())}")
    notes.append(f"description: {len(desc)}/1024 chars")
    return errors, notes


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skill", default="skills/video-studio", type=Path)
    a = ap.parse_args(argv)

    errors, notes = validate(a.skill)
    print(f"validating {a.skill}")
    for n in notes:
        print(f"  · {n}")
    if errors:
        print()
        for e in errors:
            print(f"  FAIL  {e}")
        print(f"\n  {len(errors)} problem(s)")
        return 1
    print("\n  PASS  skill package is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
