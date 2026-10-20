# Preset — kids' education

Load this when `project.audience_age` is `kids_0_8` or `project.content_type` is `kids_edu`. It narrows the generic rules; it does not replace them.

## What changes

| Area | Rule |
|---|---|
| Vocabulary | one idea per 8 words; concrete nouns only; no abstractions (civilisation, approximately, millennium) |
| Pace | 2.2–2.8 words/sec; a 50 s video holds ~110 spoken words |
| Shot length | max 5 s, ideal 3–4 s. Children track faces and objects, not scenery |
| Colour | saturated, 3-colour palette, consistent per series so the show is recognisable before the title is read |
| Faces | oversized eyes, friendly expression, never stern — a stern historical figure reads as scary |
| Quiz | if used, a full-screen card with 2 labelled options and a 3-2-1 countdown. Never ask over a talking shot |
| Ending | end on the next question, not a "Like & Subscribe" freeze |
| Loop | final frame matches the first; the CTA question becomes the seam |
| Facts | every historical or scientific claim sourced in `analysis.facts[]` |
| Safety | no weapons, blood, death, slavery, war, jumpscares, purchase language, fake urgency |
| Compliance | mark **Made for Kids** where the content is directed at children |

## Beat template (45–55 s)

```
0.0–2.8   HOOK       a child's question, mid-action
2.8–9.0   SETUP      who / where, one idea
9.0–20.0  EXCHANGE   a confident wrong belief
20.0–28.0 TURN       contradiction + the best visual in the video
28.0–33.0 QUIZ       full-screen card, A/B, countdown
33.0–38.0 REVEAL     correct option resolves
38.0–46.0 PAYOFF     the real fact, one memorable number
46.0–49.5 CTA        "who should we interview next?"
49.5–51.0 LOOP       frame-1 match, motion only
```

## Dialogue engine

**Confident wrong → gentle correction → wow.** Three lines, six seconds.

```
KID:   "You built the pyramids!"
GUEST: "Not me. They were already ancient when I was born."
KID:   "Wait — older than you?"
```

No agreement lines ("they really did"). They add no information and read as buffering.

## Character lock

Keep a `style-bible.md` per series and paste the character blocks **byte-identically** into every prompt. Rewriting the costume description is the main cause of a character changing between clips.

## Metadata

- Title: `[keyword]: [specific hook] | [format/audience tag]`, keyword in the first 40 characters.
- Thumbnail: one face + one object + 2–4 words, legible at 120 px.
- Description line 1: what the child learns, with the primary keyword.
- Pinned comment: the next-episode question.

## Why these numbers

They come from a real review of a shipped video: dead air at 00:26–00:32, a quiz asked over a static side-profile shot at 00:33–00:38, and a 6-second static outro at 00:48–00:54. Each became a rule that now fails a machine check. See `references/cases/`.

## Worked example

`assets/storyboard.template.json` is a complete kids' Short that passes the lint with zero findings. Copy it and change the subject.
