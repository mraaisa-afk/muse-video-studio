---
name: video-studio
description: "End-to-end video production for any topic, file or brief: deep source analysis, then shot-level generation prompts, then model-specific generation, then a platform-correct thumbnail, then publish-ready copy. Use whenever the user shares a topic, article, document, script, product, brand or footage and asks for a video, short, reel, ad, explainer, story, trailer, storyboard, prompt pack, thumbnail, title, description, tags, caption or publish pack. Also use for hook rewrites, video QC, re-editing, or making existing content perform better. Model-agnostic: Muse built-in video, Veo 3.1, Sora, Kling, Seedance, Runway, Pika. Any language, any platform."
license: MIT
---

# Video Studio — topic in, publish-ready video out

Five stages, in order. Each stage has a gate. **Do not start a stage before the previous gate is cleared or the user explicitly waives it.**

```
1 ANALYSE  → brief.json      gate: angle + hook approved
2 WRITE    → storyboard.json + prompts.md   gate: storyboard lint = 0 FAIL
3 GENERATE → clips + stitched master        gate: render QC = 0 FAIL
4 THUMBNAIL→ thumbnail.png + 3 alt crops    gate: readable at 120 px
5 PUBLISH  → publish-pack.md                gate: platform fields complete
```

The order is not a preference. Skipping stage 1 produces generic videos. Skipping the gate before stage 3 is how you spend credits generating a video whose script was broken.

## Stage 1 — Analyse the input (never skip)

Whatever the user gives you — one sentence, a URL, a PDF, a 40-page doc, a product photo — convert it into `brief.json` (template: `assets/brief.template.json`).

Read `references/01-analysis.md` for the full method. The minimum:

1. **Classify the input**: topic · file · URL · existing video · product · personal story · data.
2. **Extract** the core message (one sentence), the 3–5 key points, the proof points (numbers, names, demos), and the audience's actual pain.
3. **Choose the format** that fits the material, not the one the user named, if they differ — then say why in one line.
4. **Propose 5 hooks**, ranked. A hook is a contradiction, a number, a stake, or a question the viewer cannot answer alone.
5. **List risks**: unverifiable claims, rights issues, safety/compliance, claims that need sourcing.
6. **State assumptions** for anything missing. Ask at most 3 questions; if the user does not answer, proceed with assumptions written down.

Output a short brief to the user — 150 words max, plus the hook options. Wait for approval.

## Stage 2 — Write the storyboard and prompts

Produce `storyboard.json` (template: `assets/storyboard.template.json`). Every beat needs `start`, `end`, `type`, `shot`, `camera`, and — if it has words — `speaker` and `text`.

Beat types that work across genres: `hook · setup · context · proof · turn · demo · payoff · cta · loop`.

Then write `prompts.md`: one prompt per generated clip, using the six-part compiler in `references/02-prompt-engine.md`. Keep each prompt self-contained and under the model's clip limit (see `references/03-models.md`).

**Gate:** run

```bash
python3 scripts/lint_storyboard.py storyboard.json
```

Exit 0 required. Show the user the finding table. Fix the script, never the linter.

## Stage 3 — Generate, assemble, verify

- Generate clip by clip in beat order; chain continuity (snapshot ID, last frame, reference image) where the tool supports it.
- Keep per-clip files. Stitch in timeline order.
- Loudness-normalise to the platform target.
- **Gate:** `python3 scripts/qc_video.py master.mp4 --platform <platform>`. Report the numbers.

Read `references/04-generate-and-qc.md` for the segment plan, continuity mechanics, ffmpeg assembly and the honest-limits list.

## Stage 4 — Thumbnail for the destination

Generate the thumbnail **after** you know what actually happens in the final cut — not from the script. Pick the frame that carries the strongest emotion or the clearest promise.

Read `references/05-thumbnails.md` for per-platform dimensions, safe zones, text rules and prompt templates. Deliver a primary plus two alternates that survive the tightest crop.

## Stage 5 — Publish copy for the chosen platform

Read `references/06-publish-copy.md`. Deliver `publish-pack.md` with every field the platform actually uses: title, description or caption, tags/hashtags, chapters, pinned comment, cover text, end-screen line, and the first-2-line hook.

The copy is written **for the platform**, not translated from a generic template. YouTube rewards search intent; TikTok and Reels reward first-second retention and on-screen text; Facebook rewards shareability and comment prompts.

## Output contract

Every completed job delivers:

| File | Contents |
|---|---|
| `brief.json` | classification, core message, hooks, risks, assumptions |
| `storyboard.json` | timed beats, shots, camera, on-screen text, sources |
| `prompts.md` | one six-part prompt per clip, in order |
| clips + `master.mp4` | per-clip files and the assembled cut |
| `qc.md` | lint table, render numbers, and the not-verified list |
| `thumbnail.png` + alternates | platform-correct, crop-safe |
| `publish-pack.md` | all platform fields, ready to paste |

If a file is missing, say which one and why. Never imply a gate passed that you did not run.

## Operating rules

1. **Model-agnostic.** Never invent a capability. Check `references/03-models.md`; if the tool is unknown, ask for its clip limit and audio support, then proceed.
2. **Declare duration and aspect in every prompt.** Most tools silently change format otherwise.
3. **One idea per beat.** If a beat needs two sentences of explanation, it is two beats.
4. **No dead air, no static tail.** These are the two most common reasons a good video dies at 30 seconds and at the end.
5. **Never fabricate a QC result.** If ffmpeg is unavailable, write "QC not run" and say why.
6. **Never claim audio, lip-sync or voice quality you cannot verify.** List them as user-verified.
7. **Facts about people, health, money or history need a source** in `analysis.facts[]`. Cut the claim rather than soften it into vagueness.
8. **Respect rights.** Do not prompt for a real person's likeness, a trademarked character, or a copyrighted song unless the user has the rights.
9. **Language follows the audience**, not the interface. If the user writes in Bengali but publishes to a US audience, ask which language the video should speak.
10. **One deliverable format per platform.** Do not hand the user a 16:9 file for a 9:16 platform and call it "adaptable".
11. **Save everything in a dated folder** so a re-edit does not restart from zero.
12. **When a video fails, write a case card** (`references/cases/`). That is how the skill gets better than the last upload.

## Reference map

| File | Load when |
|---|---|
| `references/01-analysis.md` | stage 1, any input type |
| `references/02-prompt-engine.md` | stage 2, writing prompts |
| `references/03-models.md` | stage 2–3, choosing a model or hitting a limit |
| `references/04-generate-and-qc.md` | stage 3, assembly and QC |
| `references/05-thumbnails.md` | stage 4 |
| `references/06-publish-copy.md` | stage 5 |
| `references/07-style-recipes.md` | stage 1–2, choosing a look |
| `references/08-platform-matrix.md` | stage 1, 4, 5 — specs in one table |
| `presets/kids-education.md` | the audience is children |
| `presets/product-ad.md` | selling something |

## Quick start

```
Use video-studio. Here is my topic: "<topic>" / here is my file: <path>.
Platform: YouTube Shorts. Language: Bengali. Target: 45 seconds.
```

The agent must reply with a brief and 5 hooks — not with a video prompt.
