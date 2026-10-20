# Quickstart

Five minutes from clone to a linted storyboard.

## 1 · Get the files

```bash
git clone https://github.com/mraaisa-afk/muse-video-studio.git
cd muse-video-studio
```

No install step. No dependencies. Python 3.10+ is the only requirement, and only for the scripts.

## 2 · Prove it works

```bash
python3 tests/run_tests.py
```

You should see `14/14 passed`. If not, the clone is damaged or the Python is older than 3.10.

Then watch the linter do its job on a deliberately broken board:

```bash
python3 skills/video-studio/scripts/lint_storyboard.py tests/fixtures/broken-storyboard.json
```

```
  [FAIL] GAP            1.80s of dead air between beat 2 (00:07.40) and beat 3 (00:09.20)
  [FAIL] DUP            beat 5 repeats beat 4 (60% overlap of content words)
  [FAIL] OUTRO-TAIL     13.20s of video after the last spoken word (cap 2.0s)
  FAIL 14   WARN 14   VERDICT: FIX FIRST
```

That is a real shipped video's defects, caught in one second and zero credits.

## 3 · Load the skill into your agent

**Muse app.** Consumer Muse has no skill upload as of October 2026. Open `skills/video-studio/SKILL.md`, copy all of it, start a fresh chat, and paste:

> This is my video production skill, `video-studio`. Use it whenever I ask for a video, short, reel, ad, explainer, thumbnail or publish copy. Follow the five stages in order. Remember it for all our future conversations.

Pin that chat. Long conversations drift; a pinned one with the skill at the top is the most reliable context you have.

**Muse Code.** Real installation:

```bash
cp -r skills/video-studio ~/.agents/skills/
muse skills validate ./skills/video-studio
muse skills install ./skills/video-studio --scope user
```

**Anything else** — Claude Code, Cursor, Codex, Gemini CLI — the folder is plain Agent Skills format. Drop it in the directory your agent reads.

## 4 · Make something

```
Use video-studio.
Topic: "why cold showers wake you up faster than coffee"
Platform: Instagram Reels · Language: English · 30 seconds
```

### What should happen

**Stage 1.** The agent replies with a brief, not a video prompt:

```
CORE MESSAGE   A cold shower spikes noradrenaline faster than caffeine can absorb,
               so the wake-up is chemical, not psychological.
AUDIENCE       Someone who drinks coffee to "start the day" and thinks the shower
               is just hygiene.
STRUCTURE      claim → proof → payoff
RISKS          Health claims need a caveat; no "cures" language.
ASSUMPTIONS    You want the physiology explained, not a personal experiment.

HOOKS
1. Contradiction  "Coffee takes 20 minutes. This takes 30 seconds."     ← strongest
2. Number         "One degree colder, three times the alertness."
3. Stake          "You are dragging for 90 minutes every morning for no reason."
4. Question       "Why does the shower wake you up before the coffee does?"
5. Demonstration  Cold water hits your chest, you gasp — cut to the chemical chart.
```

Approve one, or ask for a different angle. Do not let it skip to prompts.

**Stage 2.** You get `storyboard.json` and `prompts.md`. Run the gate yourself if the agent cannot:

```bash
python3 skills/video-studio/scripts/lint_storyboard.py storyboard.json
```

**Stage 3.** Generation. The agent works within the model's real limits — see `skills/video-studio/references/03-models.md`. Expect a segment plan, not a single 30-second render.

**Stage 4.** After the cut is locked, a thumbnail sized for Reels with the subject inside the 3:4 grid crop.

**Stage 5.** `publish-pack.md`: caption, hashtags, pinned comment, and what to change if it underperforms in 72 hours.

## 5 · Copy a template instead of starting cold

```bash
cp skills/video-studio/assets/storyboard.template.json my-episode.json
```

Edit `project` first (platform, language, duration, audience), then rewrite the beats but keep the timing discipline. When you change a beat's `end`, re-check that the next `start` matches — the linter will tell you.

Three complete examples live in `examples/`:

| Example | Shows |
|---|---|
| `kids-education/` | a 49-second Short with a quiz card and a loop seam |
| `bengali-tiktok/` | non-Latin script, 16-second explainer, 1:1 grid crop |
| `product-ad/` | objection → demo → proof → offer in 22 seconds |

## Common first-run problems

| Problem | Cause | Fix |
|---|---|---|
| `SyntaxError` on import | Python older than 3.10 | upgrade, or use the `--markdown` output only |
| Every board fails `DURATION` | platform key misspelled | use exactly the keys listed by `--help` |
| `linter exits 2` | JSON syntax error | the message includes the line; check trailing commas |
| Warnings in your language | no calibration row | add one to `WPS` in the linter and a fixture |
| Agent ignores the skill | it was summarised, not loaded | paste the full `SKILL.md`, not the description |

## Next

- [`how-the-gates-work.md`](how-the-gates-work.md) — why each rule exists, and what a false positive looks like
- [`faq.md`](faq.md) — the questions this project gets
- [`../CONTRIBUTING.md`](../CONTRIBUTING.md) — add a preset or a language
