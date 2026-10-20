# Stage 3 — Generate, assemble, verify

## The segment plan

Before generating, convert the storyboard into a segment list inside the model's limit.

```
45 s target · 8 s clips → ceil(45/8) = 6–8 segments (edge clips can be shorter)
```

Rules:
- Cut on **beat boundaries**, never mid-motion.
- Never mix aspect ratios across segments.
- Put your most expensive visual in the segment that carries the turn or the proof.
- Leave a 0.3–0.5 s handle on each clip; you will need it for the cut.
- For a continuous take, use the model's extension/snapshot mechanism instead of a cut.

## Generate — in this order

1. **Pilot one clip.** Generate the hardest segment first (usually the one with a face, a hand, or a product). If it fails, the whole look fails — fix the prompt before spending the rest.
2. **Lock the subject block.** Copy the exact same subject text into every remaining prompt.
3. **Chain.** Pass the previous clip's last frame or snapshot ID. Confirm the tool accepted it; a silently dropped reference is the usual cause of a "randomly changed" costume.
4. **Name files by beat:** `s03_16-24s_v1.mp4`. You will re-cut, and `output_final_final.mp4` is how projects die.
5. **Keep failures.** A failed clip is a case card: what you asked, what appeared, what you changed.

## Verify each clip before moving on

Extract 3 frames (first, middle, last) and check:

- [ ] Subject matches the lock (face, wardrobe, colour, props)
- [ ] Light direction matches the previous clip
- [ ] No morphing limbs, extra fingers, warped text
- [ ] Aspect is what you asked for
- [ ] Motion direction is usable (not cutting into a wall)
- [ ] Nothing policy-violating slipped in

Re-generate the clip that fails. Do not carry a known-bad clip into the edit hoping it reads better at speed — it does not.

## Assemble

### Order
Timeline order. Place the voice track first, then cut picture to it. Cutting to music is a different job; do that only if the piece is music-led.

### Stitch
```bash
# 1. normalise every clip to the same codec/fps/size first
ffmpeg -i raw/s03.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30" \
       -c:v libx264 -crf 18 -preset medium -an clips/s03.mp4

# 2. concat with a list file
printf "file 'clips/s01.mp4'\nfile 'clips/s02.mp4'\n" > list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy picture.mp4

# 3. lay voice + music under, duck the music
ffmpeg -i picture.mp4 -i voice.wav -i music.wav \
  -filter_complex "[2:a]volume=0.18[m];[1:a][m]amix=inputs=2:duration=longest:dropout_transition=2[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k master_raw.mp4

# 4. loudness to the platform target (-14 LUFS is the safe default for social)
ffmpeg -i master_raw.mp4 -af "loudnorm=I=-14:TP=-1.5:LRA=11" -c:v copy -c:a aac -b:a 192k master.mp4
```

If you do not have ffmpeg, the QC script reports that honestly and you say "QC not run".

## The QC gate

```bash
python3 scripts/qc_video.py master.mp4 --platform youtube_shorts
```

It measures:

| Check | What it catches | Typical fail |
|---|---|---|
| Duration | wrong length for the platform | 36 s submitted to a 45 s slot |
| Freeze tail | static end card | 6 seconds of a smiling freeze |
| Silence | dead air inside dialogue | a 2 s gap where the edit did not close |
| Shot cadence | one shot held too long | 12 s of one angle in a 45 s video |
| Loudness / peak | mix jumps between clips | −22 LUFS on one platform, −13 on another |

Then do the **human pass**, which no script can do:

1. Watch once **muted**. Is the story clear from the images alone?
2. Watch once **with sound only**, screen off. Is the audio intelligible and smooth?
3. Watch on a phone, in daylight, at arm's length. That is the real viewing condition.
4. Check the first 2 seconds with no context. Would you stop?
5. Check the last 2 seconds. Is there motion, and a reason to re-watch or click?

## The not-verified list

Every QC report ends with this, verbatim in spirit:

> Automated checks: {pass/fail table}. Not verified by automation: voice naturalness, pronunciation, lip-sync, music balance, caption sync, compression artefacts, colour banding, and whether the joke or the argument actually lands. Those need a human check.

Never write "everything looks good" about a file you cannot see or hear.

## Re-edit protocol

When the user says "it's not working", diagnose before regenerating:

| Symptom | Likely cause | Cheapest fix |
|---|---|---|
| Viewers leave at 0–2 s | hook is a logo, a greeting, or a slow pan | re-cut the first 3 s only |
| Drop at 40–50% | mid-video dead air or repeated point | trim gaps, delete one beat |
| No comments | no question asked | add a text card question before the CTA |
| No re-watch | no loop seam | match final frame to first |
| High views, no follows | no reason to expect more | add a series promise or a next-episode line |
| Comments say "AI" | uncanny motion, plastic skin | more cuts, less face time, add grain and imperfection |

Fix in that order. Re-generating everything is almost never the answer.
