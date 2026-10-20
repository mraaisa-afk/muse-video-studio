#!/usr/bin/env python3
"""
run_tests.py — dependency-free test runner.

Runs the storyboard linter against known-good and known-bad fixtures and
asserts the verdict, the exit code, and the presence of specific rule codes.

    python3 tests/run_tests.py
    python3 tests/run_tests.py -v

Exit 0 = all pass.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINT = ROOT / "skills" / "video-studio" / "scripts" / "lint_storyboard.py"

PASS, FAIL = "PASS", "FAIL"
results: list[tuple[str, str, str]] = []


def run(storyboard: Path) -> tuple[int, dict]:
    proc = subprocess.run(
        [sys.executable, str(LINT), str(storyboard), "--json"],
        capture_output=True, text=True,
    )
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:
        payload = {"findings": [], "counts": {}, "verdict": "PARSE-ERROR"}
    return proc.returncode, payload


def record(name: str, ok: bool, detail: str = "") -> None:
    results.append((PASS if ok else FAIL, name, detail))


def expect_clean(name: str, path: Path) -> None:
    rc, out = run(path)
    fails = [f for f in out.get("findings", []) if f["severity"] == "FAIL"]
    record(name, rc == 0 and not fails,
           "" if rc == 0 and not fails else f"exit={rc} fails={[f['code'] for f in fails]}")


def expect_codes(name: str, path: Path, codes: list[str]) -> None:
    rc, out = run(path)
    found = {f["code"] for f in out.get("findings", []) if f["severity"] == "FAIL"}
    missing = [c for c in codes if c not in found]
    record(name, rc == 1 and not missing,
           "" if rc == 1 and not missing else f"exit={rc} missing={missing}")


def expect_no_codes(name: str, path: Path, codes: list[str]) -> None:
    _rc, out = run(path)
    found = {f["code"] for f in out.get("findings", []) if f["severity"] == "FAIL"}
    bad = [c for c in codes if c in found]
    record(name, not bad, "" if not bad else f"unexpected={bad}")


def main(argv=None) -> int:
    verbose = "-v" in (argv or sys.argv[1:])

    if not LINT.exists():
        print(f"linter not found at {LINT}", file=sys.stderr)
        return 2

    # ── positive fixtures: must produce zero FAIL ──────────────────────────
    expect_clean("kids education Short passes clean",
                 ROOT / "examples/kids-education/storyboard.json")
    expect_clean("Bengali TikTok explainer passes clean",
                 ROOT / "examples/bengali-tiktok/storyboard.json")
    expect_clean("product ad passes clean",
                 ROOT / "examples/product-ad/storyboard.json")
    expect_clean("shipped skill template passes clean",
                 ROOT / "skills/video-studio/assets/storyboard.template.json")

    # ── negative fixture: must reproduce the original review ───────────────
    broken = ROOT / "tests/fixtures/broken-storyboard.json"
    expect_codes("broken board exits 1 and fails", broken, ["GAP", "DUP", "OUTRO-TAIL"])
    expect_codes("broken board flags the hook", broken, ["HOOK-INTRO", "HOOK-CARD"])
    expect_codes("broken board flags the quiz", broken, ["QUIZ-LAYOUT", "QUIZ-TEXT", "QUIZ-LEN"])
    expect_codes("broken board flags integrity", broken, ["FACT", "CORE-MESSAGE", "TITLE-MISSING"])
    expect_codes("broken board flags the static end card", broken, ["END-CARD", "SHOT-LENGTH"])

    # ── platform sensitivity: same board, different destination ────────────
    ad = json.loads((ROOT / "examples/product-ad/storyboard.json").read_text())
    ad["project"]["platform"] = "youtube_long"
    tmp = ROOT / "tests" / "fixtures" / "_tmp_platform.json"
    tmp.write_text(json.dumps(ad, indent=2))
    _rc, out = run(tmp)
    codes = {f["code"] for f in out.get("findings", []) if f["severity"] == "FAIL"}
    record("a 22s ad fails the youtube_long minimum", "DURATION" in codes, f"codes={sorted(codes)}")
    tmp.unlink(missing_ok=True)

    # ── language handling: Bengali must not be shredded into fragments ─────
    sys.path.insert(0, str(LINT.parent))
    import importlib.util
    spec = importlib.util.spec_from_file_location("lint_storyboard", LINT)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["lint_storyboard"] = mod
    spec.loader.exec_module(mod)
    record("Bengali tokenizer keeps words whole",
           len(mod.words("আপনি প্রতিদিন কত মিনিট হাঁটেন?")) == 5,
           f"got {mod.words('আপনি প্রতিদিন কত মিনিট হাঁটেন?')}")
    record("English tokenizer strips punctuation",
           mod.words("Why did you build the pyramids?") ==
           ["Why", "did", "you", "build", "the", "pyramids"])
    record("CJK is estimated, not counted as one token",
           len(mod.words("我们今天学习金字塔")) > 1)

    # ── skill package validity ─────────────────────────────────────────────
    val = subprocess.run([sys.executable, str(ROOT / "scripts/validate_skill.py")],
                         capture_output=True, text=True)
    record("skill package validates", val.returncode == 0,
           val.stdout.strip().splitlines()[-1] if val.stdout else "")

    # ── report ─────────────────────────────────────────────────────────────
    failed = [r for r in results if r[0] == FAIL]
    width = max(len(r[1]) for r in results) + 2
    print()
    for status, name, detail in results:
        line = f"  {status}  {name:<{width}}"
        if detail and (verbose or status == FAIL):
            line += f"  {detail}"
        print(line)
    print(f"\n  {len(results) - len(failed)}/{len(results)} passed")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
