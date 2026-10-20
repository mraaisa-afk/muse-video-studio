# Scripts

Two gates. `lint_storyboard.py` runs on the plan; `qc_video.py` runs on the rendered file.

## Gate A — storyboard lint (before you spend credits)

```bash
python3 scripts/lint_storyboard.py storyboard.json
python3 scripts/lint_storyboard.py storyboard.json --markdown   # table for chat
python3 scripts/lint_storyboard.py storyboard.json --strict     # WARN = FAIL
python3 scripts/lint_storyboard.py storyboard.json --json
```

Reads `project.platform`, `project.language`, `project.content_type` and `project.audience_age`, then applies the right thresholds automatically.

```bash
# a kids' Short that passes clean
python3 scripts/lint_storyboard.py assets/storyboard.template.json

# a Bengali TikTok explainer that passes with one warning
python3 scripts/lint_storyboard.py assets/examples/bengali-tiktok.json
```

**No dependencies.** Standard library only.

### What it checks

| Group | Rules |
|---|---|
| Platform fit | duration window, aspect, title length, hashtag count |
| Hook | starts at 0, ≤3 s, no "welcome back", no logo card, has a question or on-screen text |
| Timeline | overlapping beats, dead air > 0.45 s |
| Repetition | consecutive lines with ≥60% shared content words, agreement lines |
| Pace | words per second per line, calibrated per language (en, bn, hi, ur, es, fr, pt, ar, id) |
| Structure | shot length caps, beat count, static end cards |
| Quiz (optional) | card layout, labelled options, countdown, 3–6 s on screen |
| Outro | tail after the last word, loop seam, CTA present |
| Integrity | every factual claim sourced when the format requires it |
| Safety | kids' vocabulary list vs general policy list |
| Thumbnail | text present, 2–4 words, not just a repeat of the title |
| Publish | title, keyword position, hashtags, pinned comment |

### Thresholds

Platforms live in one dict at the top of the file:

```python
youtube_shorts: lo=8, hi=180, sweet=(15,60),   outro=2.0,  shot=(5,7),  title=100, hashes=3
youtube_long:   lo=60, hi=7200, sweet=(180,1200), outro=20.0, shot=(8,12), title=100, hashes=3
tiktok:         lo=5,  hi=600, sweet=(12,40),   outro=1.5,  shot=(3,5),  title=150, hashes=5
```

Add a platform by adding a row. Nothing else needs to change.

## Gate B — render QC (after assembly)

```bash
python3 scripts/qc_video.py master.mp4 --platform youtube_shorts
python3 scripts/qc_video.py master.mp4 --platform tiktok --lufs -14
python3 scripts/qc_video.py master.mp4 --json-out qc.json
python3 scripts/qc_video.py master.mp4 --no-scene      # faster
```

Measures duration, trailing freeze, silence gaps, shot cadence, integrated loudness and true peak.

Exit `3` = ffmpeg missing. Say "QC not run" rather than claiming a pass.

Needs `ffmpeg` on PATH, or `pip install imageio-ffmpeg`.

## Both

```bash
bash scripts/check_all.sh assets/storyboard.template.json master.mp4
```

The platform is read from the storyboard and passed to the QC automatically.

## Sample output

```
==============================================================================
  STORYBOARD LINT  ·  bn-tiktok-walking · explainer · tiktok · bn
==============================================================================
  [WARN] SHOT-LENGTH     beat 4 holds one shot 3.3s

  FAIL 0   WARN 1   VERDICT: PUBLISH-READY
  Structure is sound. Voice, lip-sync and mix still need a human check after render.
```

```
[FAIL] FREEZE-TAIL    picture is static for the last 6.0 s (from 00:30.00 to 00:36.00)
[FAIL] SILENCE        2.00 s of silence at 00:20.00-00:22.00
[FAIL] SHOT-CADENCE   one shot holds 30.0 s (00:00.00-00:30.00)
```

## Honest limits

These scripts measure structure and the rendered file. They cannot judge whether the idea is good, whether the voice sounds human, whether the joke lands, or whether the thumbnail earns the click. Those stay with you.
