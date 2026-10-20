# Video Studio

A universal video-production skill for Muse and any Agent-Skills-capable assistant.
**Give it a topic or a file. Get back a brief, a storyboard, prompts, a video, a thumbnail for your platform, and the copy to publish it.**

No channel, no niche, no "Day 1" hardcoded. Kids' education is one preset among many.

```
topic / file / brief
      │
   1  ANALYSE   → brief.json · core message · 5 hooks · risks · assumptions
      │ gate: user approves the angle
   2  WRITE     → storyboard.json + prompts.md
      │ gate: lint = 0 FAIL
   3  GENERATE  → clips + stitched master
      │ gate: render QC = 0 FAIL
   4  THUMBNAIL → master + 2 alternates, platform-correct, crop-safe
   5  PUBLISH   → publish-pack.md (title, description, tags, hashtags, pinned comment)
```

## Why this exists

Most video skills stop at prompt engineering. That is the easy half. The failures that actually cost views are structural: a hook that opens on a logo, 2 seconds of dead air at 00:26, a quiz asked over a talking shot, a 6-second static outro that invites the swipe, a vertical file uploaded with a horizontal cover.

This skill turns those failures into **machine checks** — before generation, and again on the rendered file.

## What is inside

```
video-studio/
├── SKILL.md                        pipeline, gates, 12 operating rules
├── INSTALL.md                      three install paths
├── README.md
├── references/
│   ├── 01-analysis.md              turning any input into a brief
│   ├── 02-prompt-engine.md         six-part prompt compiler + 5 variants
│   ├── 03-models.md                Muse built-in / Veo 3.1 / Sora / Kling limits
│   ├── 04-generate-and-qc.md       segment plan, ffmpeg assembly, QC, re-edit triage
│   ├── 05-thumbnails.md            per-platform specs, safe zones, 3 archetypes
│   ├── 06-publish-copy.md          per-platform copy that is not a translation
│   ├── 07-style-recipes.md         14 looks with paste-ready style blocks
│   ├── 08-platform-matrix.md       every spec in one table
│   └── cases/README.md             case-card template + the review that built this
├── presets/
│   ├── kids-education.md           vocabulary, safety, quiz, loop rules
│   └── product-ad.md               objection → demo → proof → offer
├── assets/
│   ├── brief.template.json
│   ├── storyboard.template.json    a complete Short that passes clean
│   ├── publish-pack.template.md
│   └── examples/bengali-tiktok.json
└── scripts/
    ├── lint_storyboard.py          pre-flight gate, 30+ rules, 9 languages
    ├── qc_video.py                 post-render gate, 7 platform profiles
    ├── check_all.sh                both gates
    └── README.md
```

## The gates in action

```bash
$ python3 scripts/lint_storyboard.py assets/storyboard.template.json

================================================================================
  STORYBOARD LINT  ·  project-001 · kids_edu · youtube_shorts · en
================================================================================
  (no findings)

  FAIL 0   WARN 0   VERDICT: PUBLISH-READY
```

```bash
$ python3 scripts/qc_video.py master.mp4 --platform youtube_shorts

[FAIL] FREEZE-TAIL    picture is static for the last 6.0 s (from 00:30.00 to 00:36.00)
[FAIL] SILENCE        2.00 s of silence at 00:20.00-00:22.00
[FAIL] SHOT-CADENCE   one shot holds 30.0 s (00:00.00-00:30.00)
  FAIL 3   WARN 1   VERDICT: FIX FIRST
```

It works in other languages too — the tokenizer keeps Indic scripts intact and pacing is calibrated per language:

```bash
$ python3 scripts/lint_storyboard.py assets/examples/bengali-tiktok.json
  [WARN] SHOT-LENGTH     beat 4 holds one shot 3.3s
  FAIL 0   WARN 1   VERDICT: PUBLISH-READY
```

## Platform coverage

| | Video | Thumbnail | Copy |
|---|---|---|---|
| YouTube Shorts | 9:16, 15–60 s sweet | 2160×3840 (16:9 also accepted) | title-first, 3 hashtags |
| YouTube long-form | 16:9, chapters | 3840×2160, ≤2 MB mobile | search-intent description |
| Facebook Reels / feed | 9:16 / 1.91:1 | 1080×1920 / 1200×630 | written to be shared |
| Instagram Reels / feed | 9:16 / 4:5 | 1080×1920 (3:4 grid crop) | first line carries it |
| TikTok | 9:16, 12–40 s sweet | 1080×1920 (1:1 grid crop) | 3–5 hashtags, no links |
| LinkedIn | 16:9 | 1200×627 | claim, evidence, caveat |
| X | 16:9 | 1280×720 | one idea |

## Model coverage

| Tool | Clip limit | Audio | Continuity |
|---|---|---|---|
| Muse built-in | ~10 s | synthetic SFX only, no audio input | snapshot ID, last frame |
| Veo 3.1 | 4 / 6 / 8 s | native dialogue + SFX | extension, +7 s per call |
| Sora | 5–20 s | silent | stitch |
| Kling / Seedance | 5–10 s | usually silent | strong image-to-video identity lock |

The skill tells you which to use for dialogue, for identity, and for length — and refuses to promise face-lock where the model does not deliver it.

## Quick start

```
Use video-studio.
Topic: "why cold showers wake you up faster than coffee"
Platform: Instagram Reels · Language: English · 30 seconds
```

Expected first reply: a 150-word brief, five ranked hooks, and the risks — **not** a video prompt. That separation is what keeps the output from being generic.

## Install

- **Muse app:** copy `SKILL.md` into a fresh chat, say *"use this whenever I ask for a video, remember it."* Consumer Muse has no skill upload yet.
- **Muse Code:** `cp -r video-studio ~/.agents/skills/` then `muse skills validate ./video-studio`.
- **Any other agent:** it is plain Agent Skills format.

Details and troubleshooting in `INSTALL.md`.

## Honest limits

- `lint_storyboard.py` measures the **plan**. A clean lint means the structure is sound, not that the video is good.
- `qc_video.py` measures duration, freeze, silence, cuts and loudness. It cannot hear the voice, judge lip-sync, judge the music balance, or know whether the joke lands.
- Face-lock is weak on built-in generators. The skill tells you to regenerate a drifting clip, not to ship it.
- This is a process skill. It raises your floor and stops the repeats. Taste is still yours.

## Based on

Research into the published Muse/Veo/Sora skill repos (October 2026): the six-part prompt template and measured Muse Video limits from `masonmosen/muse-video-prompt-skill`, the six-role / compiler architecture from `LuoJiangYong/muse-video-skill`, the shot-design A/B/C method from `ErosShen/cinematic-shot-design-skill`, the evidence-driven inspection gate from `Hughhhcoder/cinematic-ai-director`, and current platform specifications. Ideas are credited; all wording here is original.

MIT.
