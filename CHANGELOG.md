# Changelog

All notable changes to this project. Format follows [Keep a Changelog](https://keepachangelog.com/); versioning follows [SemVer](https://semver.org/).

## [1.0.0] — 2026-10-20

First public release.

### Added
- **Five-stage pipeline** — analyse → write → generate → thumbnail → publish, with a gate between each stage.
- **`SKILL.md`** — operating rules, output contract, reference map. Agent Skills format, frontmatter under the 1024-character description limit.
- **Nine reference files** — analysis method, six-part prompt compiler, model capabilities and hard limits, generation and QC, thumbnails, publish copy, 14 style recipes, platform matrix, case-card template.
- **Two presets** — `kids-education` (vocabulary, safety, quiz card, loop seam) and `product-ad` (objection → demo → proof → offer).
- **`lint_storyboard.py`** — 30+ rules across 12 groups, 9 platform profiles, language-calibrated pacing, stdlib only.
- **`qc_video.py`** — duration, trailing freeze, silence, shot cadence, integrated loudness and true peak. Seven platform profiles.
- **Three complete worked examples**, each passing its gate: a kids' history Short, a Bengali TikTok explainer, a 22-second product ad.
- **A deliberately broken fixture** that reproduces seven real defects from a shipped video, used as the regression baseline.
- **Dependency-free test suite** — 14 assertions covering verdicts, rule codes, platform sensitivity, tokenizer behaviour and package validity.
- **CI** — matrix across Python 3.10–3.13 on Linux, macOS and Windows, plus a render-QC job that builds a synthetic clip and asserts the freeze and silence detectors fire.

### Notes
- Verified platform specifications as of October 2026; re-check before a paid campaign.
- Model limits are taken from published Muse, Veo and Sora skill references, not from guesswork.

## Unreleased

### Planned
- `presets/fitness.md`, `presets/finance.md`, `presets/food.md`
- Vertical-first shot-length profile for TikTok Shop
- `--fix` mode on the linter for mechanical repairs (gap closing, option labelling)
- Community case cards

---

[1.0.0]: https://github.com/mraaisa-afk/muse-video-studio/releases/tag/v1.0.0
