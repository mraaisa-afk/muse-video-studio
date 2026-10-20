# Stage 2 — The prompt engine

A video prompt is a shot list for a machine that has no memory and no taste. Write it like a shot card, not like a mood board.

## The six-part compiler

Use all six blocks, in this order. Labels are for you — strip them if the model prefers prose.

```
1 FORMAT       duration · aspect · resolution · style family
2 SUBJECT      who/what, locked description, wardrobe, state
3 SPACE        location · time of day · light · atmosphere · palette
4 BEATS        timed actions, one line per second or per action
5 CAMERA       shot size · angle · movement · lens behaviour
6 SOUND        ambience · foley · music · dialogue (if supported)
7 NEGATIVE     what must not appear
```

### 1 FORMAT
```
9:16 vertical, 1080x1920, 5 seconds, 30fps.
Shot on 35mm, shallow depth of field, natural colour, light film grain.
```
Declare duration and aspect **even if the tool has settings** — it anchors the model's composition. Style family goes here: `cinematic live action`, `3D cartoon`, `2D vector animation`, `stop motion`, `documentary handheld`, `product commercial`, `anime`.

### 2 SUBJECT
Lock the subject in words you will reuse **byte-identically** across every clip of the same shoot. Rewriting the description is the single largest cause of a character changing between shots.
```
SUBJECT: Woman, early 30s, shoulder-length dark hair tucked behind one ear,
freckles, plain white t-shirt, olive-green canvas jacket, small silver hoop
earrings. Calm, slightly tired expression.
```
For objects: material, colour, wear, scale reference. For products, include the exact silhouette and label placement.

### 3 SPACE
```
SPACE: Small apartment kitchen, early morning. Window light from camera-left,
cool grey-blue shadows warm-tinted by a single pendant bulb. Cluttered but
tidy: ceramic bowls, a kettle, a stack of mail.
```
Two sentences. Name the light direction, because it is what makes ten clips look like one film.

### 4 BEATS
```
BEATS:
0.0-1.5s  She lifts the kettle, hesitates.
1.5-3.0s  Steam rises; she sets it down without pouring.
3.0-5.0s  She looks out the window, exhales.
```
Budget: **one action per 1.5 seconds** for realistic motion. Models compress anything denser. Never write a 20-second beat into a 5-second clip.

### 5 CAMERA
One move per clip. Name it in film terms:
`locked-off` · `slow push-in` · `pull-back` · `dolly left` · `handheld follow` · `orbit` · `crane up` · `whip pan` · `snap zoom` · `rack focus` · `low-angle hero`.

```
CAMERA: Locked-off medium close-up, 50mm equivalent, eye level, subject
centred with headroom for captions in the lower third.
```

### 6 SOUND
```
SOUND: Room tone, kettle click, faint traffic outside. No music.
DIALOGUE: (Maya) "I don't think I can keep doing this."
```
If the model has no audio, write `SOUND: none — added in assembly` and keep your plan in the storyboard instead.

### 7 NEGATIVE
```
NEGATIVE: no on-screen text, no subtitles, no watermark, no logo, no extra
people, no distorted hands, no warped faces, no jump cuts, no camera shake,
no lens flare, no oversaturation.
```
Negative prompts are cheap insurance. Always list the failures you actually saw last time.

## Prompt variants

### A · Talking head / testimony
```
9:16, 8s. A woman sits facing camera, framed chest-up, at a plain desk.
She speaks directly to lens, unhurried.
BEATS: 0-2s settles, 2-6s speaks, 6-8s small nod.
CAMERA: locked-off, 50mm, slight shallow focus, no autofocus hunting.
DIALOGUE: "We shipped it on a Friday. Nobody noticed for six weeks."
```
Rules: eyes to lens, not to a phone; no camera visible in frame; one line per clip.

### B · Product / object hero
```
9:16, 5s. Matte-black aluminium bottle on a wet slate surface.
BEATS: 0-1s water bead runs down; 1-3s slow rotation catches a rim highlight;
3-5s fine mist settles.
CAMERA: 100mm macro, slow orbit 15 degrees, locked focus on the label.
LIGHT: hard key from top-right, black fill, single soft rim.
NEGATIVE: no extra bottles, no fingers, no text on the label other than the
existing print, no reflections of a studio.
```

### C · B-roll / proof cutaway
```
16:9, 4s. Wide low-angle of a crowded market at dusk, awnings lit warm,
steam from a food cart crossing the frame left to right.
CAMERA: slow dolly right at walking pace, 24mm, deep focus.
SOUND: crowd murmur, sizzle, distant horn.
```
This is where you spend your best image. Put it at the moment the argument needs evidence.

### D · Motion graphic / text card
Models render text badly. Generate a clean plate, then composite the type:
```
9:16, 3s, static. Flat-design card, deep navy background, one rounded white
panel centred, generous empty margins. A small pulsing dot in the corner.
NEGATIVE: no letters, no numbers, no words, no icons of text.
```
Overlay the real words in the editor. If the tool renders text reliably, keep it under 6 words per card.

### E · Animated character
```
9:16, 5s, 3D cartoon, soft rounded shapes, saturated but not neon.
SUBJECT: [locked character block, verbatim]
BEATS: 0-1s turns to camera; 1-3s raises eyebrows; 3-5s shrugs.
CAMERA: medium close-up, slight push-in.
NEGATIVE: no realistic human proportions, no extra limbs, no scary expression.
```

## Segmenting anything longer than one clip

Model limits are in `03-models.md`. To build a 45-second video from 8-second clips:

1. Split on **beat boundaries**, never mid-motion.
2. Give each segment its own prompt with a header:
   `Segment 3 of 7 (16-24s). Same subject, wardrobe, location, light and grade as segment 2.`
3. Reuse the subject/space blocks **verbatim**.
4. Chain continuity: pass the previous clip's last frame, or the tool's snapshot/extension ID.
5. Plan the transition: hard cut, match cut, whip pan, or sound bridge. Write it in the storyboard, not in the prompt.
6. Keep every per-clip file. You will re-cut.

## The prompt audit (before you spend credits)

Run this list on every prompt:

- [ ] Duration and aspect stated first
- [ ] Subject description identical to every other clip in the shoot
- [ ] Light direction named
- [ ] Actions fit inside the duration (≈1 per 1.5 s)
- [ ] Exactly one camera move
- [ ] Sound plan present, or explicitly delegated to assembly
- [ ] Negatives list includes the last failure you saw
- [ ] No text you expect the model to render
- [ ] No real person's likeness, trademarked character, or copyrighted lyric
- [ ] Under 120 words — longer prompts dilute

## Prompt failures and their fixes

| Symptom | Cause | Fix |
|---|---|---|
| Subject changes between clips | description reworded | paste the exact same block |
| Everything happens at once | too many beats | 1 action per 1.5 s |
| Feels like stock footage | no light direction, no lens | name the key light and focal length |
| Garbled text | asked a model to render words | clean plate + overlay in edit |
| Camera nausea | two moves stacked | one move per clip |
| Flat, "AI-looking" colour | no grade language, no grain | specify palette, contrast, grain, and one imperfection |
| Cropped heads | modelled for 16:9 | state 9:16 and "headroom in upper third" |
| Repeated feet/hands morphing | long single take | cut earlier; hide joints at frame edges |
