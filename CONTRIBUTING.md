# Contributing

The bar for a contribution is one sentence: **bring evidence, not adjectives.**

A rule that says "make it more engaging" is not a contribution. A rule that says "silence between two dialogue beats above 0.45 s reads as buffering, measured on 40 uploads" is.

## What is most useful

| Contribution | How | Why it matters |
|---|---|---|
| **A new preset** | copy `skills/video-studio/presets/kids-education.md`, change vocabulary, safety and beat template | Presets are where the skill becomes specific without becoming narrow |
| **A platform row** | add to `PLATFORMS` in `scripts/lint_storyboard.py` and the matrix in `references/08-platform-matrix.md` | New platforms appear constantly |
| **A language calibration** | add a row to `WPS` and `STOPWORDS`, then add a fixture | The tokenizer breaks silently on scripts it has not seen |
| **A case card** | `references/cases/NN-slug.md` following the template | A card with a timestamp and a metric is worth ten opinions |
| **A bug in a rule** | a fixture that reproduces it, then the fix | Rules over-fit; a failing fixture is the proof |

## Workflow

```bash
git clone https://github.com/mraaisa-afk/muse-video-studio.git
cd muse-video-studio
python3 tests/run_tests.py        # nothing should break before you start
```

1. Open an issue first for anything larger than a typo. Describe the failure with a timestamp, a metric, or a before/after.
2. Branch: `feat/preset-fitness` or `fix/gap-threshold`.
3. Make the change. If it is a rule, add a fixture that fails before and passes after.
4. Run:

```bash
python3 scripts/validate_skill.py
python3 tests/run_tests.py
for f in examples/*/storyboard.json; do python3 skills/video-studio/scripts/lint_storyboard.py "$f"; done
```

5. Open the PR. Fill in the template — specifically the "evidence" field.

## Rules for rules

1. **A rule needs a threshold, a reason and a fix.** No rule without all three.
2. **Every rule gets a code** in `UPPER-CASE`, and a row in `references/04-generate-and-qc.md`.
3. **False positives are worse than misses.** If a rule fires on a legitimate video, tighten it or make it a WARN.
4. **Platform-specific numbers belong in `PLATFORMS`**, not buried in a check.
5. **Never add a rule that cannot be checked from the storyboard JSON or the rendered file.**

## Style

- Markdown: sentence case headings, one idea per paragraph, tables over bullet walls.
- Python: stdlib only, no dependencies, type hints, `from __future__ import annotations`.
- Scripts must run on Python 3.10+ and exit with meaningful codes: `0` ok, `1` findings, `2` bad input, `3` missing tool.
- Comments explain *why*, not *what*.

## What will be declined

- Prompt packs with no storyboard behind them.
- "Make it go viral" advice with no mechanism.
- Anything that promises face-lock, audio sync, or a QC result the tooling cannot produce.
- Rebranded copies of an existing skill without original work.

## Credit

Contributors are credited in `CHANGELOG.md` under the release that shipped their work.

## Code of conduct

Be decent. Critique the rule, not the person. Assume the other contributor has measured something you have not.
