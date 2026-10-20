# Stage 4 — Thumbnails that fit the platform

A thumbnail is not a poster for the video. It is a **decision surface** in a grid, seen for about 0.4 seconds, at 120–320 px wide.

## The rule that survives every platform: design crop-safe

Platforms crop the same file differently. Build one master that survives all of them:

```
MASTER 3840 x 2160 (16:9)
├─ safe box: centre 60% width x 60% height — all critical content lives here
├─ text box: centre square (1:1) — survives every crop
├─ face: upper-centre, eyes on the upper third
└─ nothing important within 8% of any edge
```

Then export per platform. Never design at 1280×720 and upscale.

## Specs by platform (verified October 2026)

| Platform | Thumbnail / cover size | Ratio | Cap | Notes |
|---|---|---|---|---|
| **YouTube long-form** | 3840×2160 recommended (1280×720 legacy, min 640 wide) | 16:9 | 2 MB mobile, 50 MB desktop | JPG/PNG. Text must read at 320 px |
| **YouTube Shorts** | 2160×3840 (9:16) for Shorts series; 1280×720 (16:9) still accepted | 9:16 or 16:9 | 2 MB | **Ambiguous by design** — YouTube's help page documents 16:9 while Studio accepts vertical. Upload 9:16 and keep the subject centred so a 16:9 crop still works |
| **Facebook Reels / video** | 1080×1920 (Reels cover); link preview 1200×630 | 9:16 / 1.91:1 | 30 MB | Cover text is partially covered by the UI — keep it above the bottom 25% |
| **Facebook feed post** | 1200×630 | 1.91:1 | 30 MB | The preview shows ~1.91:1 on desktop, 1:1 on mobile |
| **Instagram Reels** | 1080×1920 cover | 9:16 | 8 MB | Profile grid crops to **3:4** (1080×1440) — keep the subject in the middle |
| **Instagram feed** | 1080×1350 | 4:5 | 8 MB | 4:5 takes the most vertical space |
| **TikTok** | 1080×1920 cover | 9:16 | 10 MB | Profile grid crops to **1:1 centre** — keep the subject in the middle band |
| **LinkedIn** | 1200×627 | 1.91:1 | 5 MB | Text-forward, no yelling |
| **X** | 1280×720 | 16:9 | 5 MB | Small in timeline; one idea only |

When the platform's own documentation contradicts itself, **ask which placement matters** (channel page, search, Shorts shelf) and optimise for that one. Say which you chose.

## Composition rules

1. **One face, one object, one emotion.** Two focal points is zero focal points.
2. **Face ≥ 40% of frame height**, eyes on the upper third, looking toward the text.
3. **2–4 words**, max 5. Large, high-contrast, heavy weight.
4. **Text and image must not say the same thing.** The image shows, the words argue.
5. **Contrast at thumbnail scale**: check by shrinking to 120 px and squinting. If the subject disappears, it is too busy.
6. **No clutter**: no arrows, no red circles, no emoji, no channel logo in the corner, no episode numbers.
7. **A gap the brain wants to close**: an unfinished action, a covered object, a number with the answer missing.
8. **Colour** — one dominant hue, one accent. Faces and products should not fight the background.
9. **Consistency across a series** builds recognition faster than novelty: same crop logic, same font, same colour code.
10. **Do not fake**: no shocked-face stock expressions, no false claims, no misleading before/after.

## Three thumbnail archetypes

| Archetype | Use | Prompt skeleton |
|---|---|---|
| **Face + stake** | opinion, story, personal brand | `extreme close-up of [subject] at [emotion], eyes to lens, [object] blurred in foreground, high key from left, shallow depth, room for 3 words on the right` |
| **Object + question** | product, review, how-to | `hero shot of [product] on [surface], hard key, one detail in sharp focus, negative space top-left for text, 100mm macro` |
| **Before / after split** | transformation, comparison | `split composition, left dull/grey [before], right bright [after], same framing, vertical divider, no text` |

## Generating the base image

Generate the **image**, not a rendered thumbnail — you need clean space to typeset on.

```
Thumbnail plate, 16:9, 3840x2160, [style family].
SUBJECT: [same locked description as the video, or the product]
EXPRESSION / ACTION: [one readable emotion or action]
LIGHT: hard key from camera-right, soft fill, background falling to shadow.
COMPOSITION: subject on the right third, eyes upper third, clean negative
space on the left 40% for a headline.
NEGATIVE: no text, no letters, no logos, no watermark, no busy background,
no extra people, no distorted features.
```

Then typeset the words in an editor with a real font. Models render type badly, and a garbled word kills more clicks than a boring one.

## Text overlay rules

- Typeface: one heavy sans, one weight. No outlines thicker than 6 px, no drop shadows beyond 8 px.
- Colour: white or near-white on a darkened area, or a saturated brand accent.
- Never place text over a face.
- Keep 8% padding from every edge.
- Localise the text into the video's language, not the platform's.

## Delivery

Deliver:

1. `thumbnail_master.png` (16:9 or 9:16 depending on platform)
2. `thumbnail_alt_1.png` — different emotion or framing
3. `thumbnail_alt_2.png` — different promise
4. `thumbnail_preview_120.png` — the squint test, attached so the user sees what the grid sees

Explain in one line what each alt is testing. Never deliver four near-identical crops.

## The thumbnail audit

- [ ] Correct pixel size and file format for the destination
- [ ] Under the file-size cap
- [ ] Readable at 120 px wide
- [ ] ≥ 40% face or product
- [ ] 2–4 words, spelled correctly, in the audience's language
- [ ] No text over a face, no logo, no borders
- [ ] Survives the tightest crop of every platform you will post to
- [ ] Does not lie about the content
