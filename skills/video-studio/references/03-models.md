# Stage 3 — Model profiles and hard limits

Never promise a capability the tool does not have. Read the row, then design the video around it.

Verified facts below come from the published skill references of working Muse/Veo/Sora pipelines (October 2026). If your build differs, **ask the user for the clip limit and audio support**, then update this table.

## Quick comparison

| Tool | Clip length | Audio in generation | Image / reference input | Continuity mechanism |
|---|---|---|---|---|
| **Muse built-in video** | ~10 s, not controllable | Synthetic SFX only, no audio input | Text and images; **no audio upload** | `resume_from_snapshot_id`, last-frame reference |
| **Veo 3.1** (Vertex / AI Studio) | 4, 6, 8 s | **Native dialogue, SFX, ambience** | Up to 3 reference images; image-to-video | Native **extension** (+~7 s per call, max 20) |
| **Sora** | 5, 10, 15, 20 s | Silent | Image-to-video | Stitch |
| **Kling / Seedance** | ~5–10 s | Usually silent; some dialogue | Strong image-to-video, best face/identity lock | First/last frame, reference images |
| **Runway / Pika** | ~4–10 s | Usually silent | Image-to-video | Frame conditioning |

## Muse built-in video — measured limits

- **~10 seconds per generation, duration not settable.** A 45-second video is 5–7 generations plus assembly. Say this in the brief; do not promise a one-shot 45-second render.
- **No audio input.** You cannot "use this song" or "sync to this narration". Plan music and voice as a separate assembly step.
- **Aspect ratio is declared in the prompt**, not in a setting: write `9:16` or `16:9`. It is respected roughly, so check the first clip before generating the rest.
- **Reference images:** confirm the file exists, keep filenames **ASCII** (non-ASCII paths get rejected upstream), and send images before text in the prompt payload.
- **Face/identity lock is weak.** Even with explicit locking instructions, a reference photo may not carry. If identity must hold, use an image-to-video model with stronger conditioning, or design the shot so the face is not the subject.
- **Author blind spots:** it cannot watch or listen to the result. Frame extraction is the only self-check. Dialogue, accent, lip-sync and mix are always user-verified.

## Veo 3.1 — when dialogue matters

- 4/6/8 s only; 720p or 1080p; 9:16 or 16:9.
- Native audio means you can write dialogue in quotes and it will be spoken with lip-sync. This is the fastest route to a talking-head video.
- Up to 3 reference images guide identity, style and product.
- **Extension** gives true continuation of the same shot: each call adds ~7 s, up to 20 calls (~2.5 min), input must be Veo-generated, output 720p. Use extension for one continuous take; use stitching for scene changes.
- Practical: an 8-second clip with dialogue beats three 5-second silent clips for talking content. Choose it when the words are the product.

## Sora — when duration matters

- 5–20 s per clip, silent. Best for a single unbroken visual idea, surreal or scenic material, and B-roll that will carry a separate voice track.
- No audio means everything is added later; plan the sound design in the storyboard.

## Kling / Seedance — when identity matters

- Image-to-video with strong first-frame conditioning is the most reliable way to keep the same face or product across shots. Generate a clean still, then animate it.
- Dialectics differ per model (multi-shot markers, reference tags). When a model has its own syntax reference, follow it exactly instead of inventing.

## Decision tree

```
Does the video need spoken dialogue or lip-sync?
├─ yes → Veo 3.1 (8s + extension)  or Muse built-in + separate TTS
└─ no
   ├─ Need one continuous take longer than 10s? → Veo extension
   ├─ Need the identical face/product across many shots? → Kling/Seedance image-to-video
   ├─ Need 15-20s in one generation? → Sora
   ├─ Need native SFX and you're inside Muse? → Muse built-in
   └─ Need speed and volume? → cheapest model at 5s, more cuts
```

## Honest-limits script

Say this to the user, once, before generating:

> "Generation is limited to ~{N}s per clip and there is no audio input, so I will build {M} clips and assemble them, then add voice and music in the edit. I can verify the picture by extracting frames; I cannot hear the mix or judge lip-sync — those need your check."

That sentence prevents most disappointment. Never let the user discover a limit after paying for renders.

## Rights and safety, per model

- Do not prompt for a real person's likeness, a living public figure, a trademarked character, or a copyrighted song lyric.
- Do not recreate a specific copyrighted film scene; reference *qualities* (lighting, palette, lens), not protected characters.
- For children's content, no realistic child faces, no scary or violent imagery, no purchase prompts.
- Keep a record of any reference image's licence in `assets/`.

## When the tool is unknown

Ask exactly three questions and proceed:

1. What is the maximum clip length?
2. Does it generate audio or dialogue?
3. Can it take a reference image or a previous clip as a continuation?

Design for the smallest of the three. A video built for 5-second silent clips still works on a better tool; the reverse is not true.
