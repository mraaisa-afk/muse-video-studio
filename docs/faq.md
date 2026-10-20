# FAQ

## Is this an official Meta project?

No. It is an independent skill package in the open Agent Skills format. It is not affiliated with or endorsed by Meta. Names like "Muse", "Veo" and "Sora" are used descriptively to say what the skill works with.

## Can I install a skill into the Muse app?

Not through a button. As of October 2026, consumer Muse documents skills as built-in, Meta-authored capabilities, with no upload path for user skills. The method that works is paste-and-pin: copy `SKILL.md` into a fresh chat and ask Muse to remember it for future conversations.

**Muse Code** is different — it reads standard `SKILL.md` files from `~/.agents/skills/`, `<repo>/.agents/skills/`, and even `~/.claude/skills/`. See `docs/quickstart.md`.

## Does it actually generate video?

It directs generation. The agent writes the prompts, calls whatever video tool you have connected, and assembles the output. This repository does not ship a renderer and requires no API key to be useful — the lint and QC gates run with plain Python.

If your agent cannot generate, the skill still produces the brief, storyboard, prompt pack, thumbnail plan and publish pack. That is most of the value for a solo creator.

## Why a 0.45-second threshold on silence?

Because a pause longer than that between two dialogue lines stops reading as a beat and starts reading as a buffer. It was measured on a real review: a 1.8-second gap at 00:26 of a 54-second video, immediately followed by a repeated talking point. Both defects are now rules.

The number is not sacred. Change it in the `PLATFORMS` dict — but change it once, for every video, so the whole channel is judged against the same standard.

## Will it make my videos generic?

The opposite is the design goal. Stage 1 refuses to write a prompt until it has a core message, an audience and an approved hook. Generic output comes from skipping that stage, which is exactly what most prompt templates do.

The style recipes exist for the same reason: fourteen named looks force a decision instead of defaulting to "cinematic".

## Does it work for non-English content?

Yes. Pacing is calibrated per language (`en`, `bn`, `hi`, `ur`, `es`, `fr`, `pt`, `ar`, `id`), and the tokenizer keeps Indic scripts intact instead of shredding them into fragments — a real bug that a naive regex causes.

`examples/bengali-tiktok/storyboard.json` is a complete Bangla example that passes the gate.

If your language is missing, add a row to `WPS` and `STOPWORDS` in the linter, plus a fixture. Two lines of data, one test.

## The linter fired on my video and it was fine. Now what?

That is a bug, and it is the most useful issue you can open. Attach the storyboard. A false positive gets the rule tightened or demoted to WARN, and your case becomes a fixture so it cannot regress.

Rule design accepts missing a bad video before it accepts failing a good one.

## Why does it refuse to promise face-lock?

Because the models do not deliver it. Built-in video generation keeps identity weakly even with explicit locking instructions; the published pipeline notes say so directly. Promising it and failing costs you a full re-render and your trust.

When identity genuinely has to hold, the skill routes you to image-to-video conditioning (Kling, Seedance) instead of pretending text prompts will do it.

## Can it judge whether my video is good?

No, and it says so every time. The gates measure structure: timing, cadence, dead air, freeze, loudness, copy completeness. They cannot tell you whether the joke lands, whether the voice sounds human, or whether the thumbnail earns the click.

Every report ends with an explicit not-verified list. Treat that list as your job.

## How do I add a platform?

One row in the `PLATFORMS` dict in `skills/video-studio/scripts/lint_storyboard.py`, and one row in `references/08-platform-matrix.md`. Include the aspect, the duration window, the sweet spot, the outro cap, the shot-length caps, the title limit and the hashtag limit.

Add a fixture if the platform has an unusual rule.

## Can I use it commercially?

MIT. Fork it, ship it inside a paid product, sell the videos you make with it. No attribution required, though a star is appreciated.

The one thing the licence does not give you is rights to other people's music, footage or likeness. The skill flags rights risks in stage 1, but clearing them is your job.

## Why is the broken fixture committed on purpose?

A test that only checks good input proves nothing. `tests/fixtures/broken-storyboard.json` reproduces seven specific defects from a real shipped video, and CI asserts the linter still rejects it. If a refactor quietly disables a rule, CI goes red.

That is the difference between a skill and a template.

## How do I keep it from rotting?

The platforms change. YouTube moved its recommended thumbnail size; Shorts thumbnail guidance has been internally inconsistent between the help page and Studio. TikTok and Reels change crops.

Two habits: put the verification date next to any spec you rely on, and add a case card after every upload that surprises you. The `CHANGELOG.md` records what changed and when.
