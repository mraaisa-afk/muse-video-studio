# How the gates work

Two gates protect you from two different failures. Neither is a quality opinion; both are measurements.

```
Gate A  lint_storyboard.py   →  the PLAN is sound
Gate B  qc_video.py          →  the FILE is sound
```

Gate A is free and catches roughly four out of five defects. Gate B costs one ffmpeg run and catches the rest.

---

## Gate A — the storyboard

Reads `storyboard.json`. The verdict comes from the platform, the language and the content type declared in `project`.

```bash
python3 skills/video-studio/scripts/lint_storyboard.py storyboard.json
```

### The rules, and why each one exists

| Code | What it catches | Threshold | Why this number |
|---|---|---|---|
| `DURATION` | wrong length for the destination | per platform | a 22 s clip cannot fill a 60 s long-form slot; a 90 s clip cannot be a Short |
| `ASPECT` | vertical content shipped horizontal | per platform | letterboxing costs more attention than a re-render |
| `HOOK-START` | pre-roll before the hook | > 0.4 s | anything before the first frame is a swipe |
| `HOOK-INTRO` | "welcome back", "in this video" | any | housekeeping is the single most common cause of a 0–2 s drop |
| `HOOK-CARD` | logo or title card as the hook | any | nobody has ever stayed for a logo |
| `HOOK-LEN` | a hook that runs long | > 3 s short-form | attention is decided in the first two |
| `GAP` | dead air between beats | > 0.45 s | measured: silence above ~0.45 s reads as buffering |
| `OVERLAP` | two beats occupying the same second | any | a timeline bug that renders as a glitch |
| `DUP` | two consecutive lines teaching the same thing | ≥ 60% content-word overlap | the exact defect found at 00:26 in a real review |
| `AGREE` | "they really did", "yes exactly" | any | adds no information and restarts the energy curve |
| `WPS` | a line that cannot be spoken in its slot | 1.6–3.1 wps hard | below reads stalled, above is unintelligible |
| `WORD-BUDGET` | more script than runtime | per platform | cut a beat; never speed up the voice |
| `QUIZ-LAYOUT` | a question asked over a talking shot | any non-card layout | an answer surface must be visible |
| `QUIZ-TEXT` | fewer than two labelled options | < 2 | "A) Yes / B) No" is the affordance |
| `QUIZ-LEN` | a quiz you cannot read in time | 3–6 s | under 3 s there is no thinking time |
| `SHOT-LENGTH` | one setup held too long | per platform | visual sameness is the mid-video drop |
| `OUTRO-TAIL` | video after the last word | per platform | the 6 s static tail is the classic swipe trigger |
| `END-CARD` | a static card anywhere in a vertical video | any | end cards are a long-form convention |
| `LOOP-SEAM` | no match between last and first frame | warn | re-watch is the cheapest amplification |
| `FACT` | a claim with no source | per content type | education and documentary need provenance |
| `CORE-MESSAGE` | no stated argument | empty | a video without an argument is a montage |
| `SAFETY` | vocabulary that fails kids' or ad policy | list | cheaper to catch here than at review |
| `CHARACTER` | a speaker not in the cast list | warn | a typo in a voice mapping is a wasted render |
| `THUMB-WORDS` | more than 5 words on a thumbnail | > 5 | unreadable at 120 px |
| `THUMB-REPEAT` | thumbnail text repeats the title | subset | the two surfaces should complete each other |
| `KEYWORD` | primary keyword not in the title | warn | search intent is decided in the first 40 characters |

### Severity policy

- **FAIL** — the video will underperform for a structural reason. Fix the plan.
- **WARN** — deliberate choices are sometimes right. Confirm the intent.
- `--strict` promotes every WARN to FAIL for a flagship upload.

A false positive is a bug. Open an issue with the storyboard that triggered it.

### Platform profiles

One dict drives the thresholds:

```python
youtube_shorts: lo=8, hi=180, sweet=(15,60),     outro=2.0,  shot=(5,7),   title=100, hashes=3
youtube_long:   lo=60, hi=7200, sweet=(180,1200), outro=20.0, shot=(8,12),  title=100, hashes=3
tiktok:         lo=5, hi=600, sweet=(12,40),     outro=1.5,  shot=(3,5),   title=150, hashes=5
```

Adding a platform is one row. Nothing else changes.

### Language handling

Two things are calibrated per language:

1. **Pacing** (`WPS`) — a comfortable words-per-second band.
2. **Tokenisation** — the word counter splits on whitespace and trims edge punctuation, rather than matching Unicode letters. This matters: a letter-based regex shreds Bengali and Hindi because viramas and matras are combining marks.

```
$ python3 -c "..."
['আপনি', 'প্রতিদিন', 'কত', 'মিনিট', 'হাঁটেন']    # 5 words, intact
```

CJK has no spaces, so its characters are estimated at roughly two per word.

---

## Gate B — the rendered file

```bash
python3 skills/video-studio/scripts/qc_video.py master.mp4 --platform youtube_shorts
```

| Check | Method | Fails when |
|---|---|---|
| `DURATION` | container probe | outside the platform window |
| `FREEZE-TAIL` | `freezedetect` on the tail | the picture is static for more than 2 s at the end |
| `SILENCE` | `silencedetect` at −35 dB | a gap over 0.6 s sits between dialogue |
| `SHOT-CADENCE` | scene-change timestamps | one setup holds past the platform cap |
| `LOUDNESS` | `ebur128` integrated | outside −16 to −13 LUFS |
| `TRUEPEAK` | ebur128 sample peak | above −1.5 dBTP |

A freeze that runs to the end of file emits no `freeze_end` event in ffmpeg. The script handles that case explicitly — it is the exact shape of the 6-second static outro defect.

### Why these are measured, not assumed

Freeze and silence are invisible in a script and obvious in a file. A script can say "the outro is one second"; only the render knows that the last clip was padded and the timeline was not trimmed. That is why Gate B exists as a separate stage rather than a checkbox.

---

## The verdict

| | Meaning |
|---|---|
| `PUBLISH-READY` | no FAIL, fewer than 3 WARN |
| `PASS WITH WARNINGS` | no FAIL, but confirm the intent behind each WARN |
| `FIX FIRST` | at least one FAIL — do not generate, do not upload |

## The not-verified list

Every QC report ends with what it could **not** check:

> Voice naturalness · pronunciation · lip-sync · music balance · caption sync · compression artefacts · colour banding · whether the joke or the argument lands.

Those need a human. A report that claims otherwise is lying, and a skill that lies about its coverage is worse than no skill.

## Cost

Gate A is instant and free. Gate B is one ffmpeg pass, a few seconds for a Short. Both are cheaper than a single wasted generation, which is the whole argument for running them before you spend anything.
