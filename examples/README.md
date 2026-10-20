# Worked examples

Three complete storyboards, each passing its gate. Copy one and change the subject — the timing discipline is the part worth keeping.

| Example | Platform | Length | Language | What it demonstrates |
|---|---|---|---|---|
| [`kids-education/`](kids-education/) | YouTube Shorts | 49 s | English | quiz card, loop seam, required proof cutaway, sourced claims |
| [`bengali-tiktok/`](bengali-tiktok/) | TikTok | 16 s | Bengali | non-Latin script, 1:1 grid crop, 3-hashtag discipline |
| [`product-ad/`](product-ad/) | Instagram Reels | 22 s | English | objection → demo → proof → offer, no dialogue in the demo |

> **Note on `bengali-tiktok/`:** Non-English strings in this file are intentional test data, not repository documentation.

## Verify all three

```bash
for f in examples/*/storyboard.json; do
  python3 skills/video-studio/scripts/lint_storyboard.py "$f"
done
```

Expected: `FAIL 0` on each, with at most a pacing warning.

## What each file contains

Every example is a single `storyboard.json` — the complete source of truth for stages 2 through 5:

```
project      platform, language, aspect, duration, audience, goal, cast
analysis     core message, chosen hook, structure, sourced facts, assumptions
beats[]      timed beats with shot, camera, text, on-screen text, transitions
quiz         optional: card layout, labelled options, countdown
outro        last word end, video end, question, loop seam
thumbnail    text, subject, emotion, crop-safety
publish      title, keyword, description hook, tags, hashtags, pinned comment
```

The linter reads `project` first and applies the right platform thresholds to everything else. Change one field — `"platform": "tiktok"` — and the same board is judged against a different standard.

## Generating the other artifacts

The skill produces `brief.json`, `prompts.md` and `publish-pack.md` from this board at stages 1, 2 and 5. See [`kids-education/prompts.md`](kids-education/prompts.md) for a finished prompt pack.
