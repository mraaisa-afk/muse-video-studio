# INSTALL

## Path 1 — Muse app (chat, web, iOS/Android)

Meta's consumer Muse has **no skill upload button** as of October 2026 — skills there are built-in, Meta-authored capabilities. The working method is paste-and-pin:

1. Open `SKILL.md` and copy the whole file.
2. New chat. Paste it with:

   > This is my video production skill, `video-studio`. Use it whenever I ask for a video, short, reel, ad, explainer, thumbnail, or publish copy. Follow the five stages in order. Remember it for all our future conversations.

3. Test it immediately with a real request. If the agent replies with a **brief and five hooks** instead of a video prompt, it loaded correctly.

**Keep one pinned chat** for the project and return to it. Long chats drift; a pinned chat with the skill at the top is the most reliable context you have.

If the chat cannot run scripts, paste `references/02-prompt-engine.md` when you reach stage 2 and ask the agent to check the storyboard against the rule list in `references/04-generate-and-qc.md` manually.

## Path 2 — Muse Code (real installation)

Muse Code is Meta's developer agent and the one Muse product that reads standard `SKILL.md` files. It discovers:

- `<repo>/.agents/skills/<skill-id>/SKILL.md` — project scope
- `~/.agents/skills/`, `$XDG_CONFIG_HOME/muse/skills` — user scope
- `~/.claude/skills/`, Codex skills dir — cross-compatibility

```bash
mkdir -p ~/.agents/skills
cp -r video-studio ~/.agents/skills/

muse skills validate ./video-studio
muse skills install ./video-studio --scope user
muse skills list
```

Project scope, so a team shares it:

```bash
mkdir -p .agents/skills && cp -r video-studio .agents/skills/
```

Invoke it in a session, e.g. `/video-studio` then the topic. With the project folder in the repo, the agent can run `lint_storyboard.py` and `qc_video.py` itself — that is where the gates become real instead of advisory.

## Path 3 — any other agent

The format is portable (Claude Code, Cursor, Codex, Gemini CLI). The scripts are plain Python:

```bash
python3 scripts/lint_storyboard.py assets/storyboard.template.json
python3 scripts/qc_video.py master.mp4 --platform tiktok
```

Requirements: Python 3.10+ for the lint script (stdlib only). `qc_video.py` needs ffmpeg — system `ffmpeg` or `pip install imageio-ffmpeg`.

## Verify the install

```bash
python3 scripts/lint_storyboard.py assets/storyboard.template.json   # expect: FAIL 0, PUBLISH-READY
python3 scripts/lint_storyboard.py assets/examples/bengali-tiktok.json # expect: FAIL 0, 1 WARN
```

If both pass, the skill is intact.

## Customise in the first ten minutes

1. **`assets/brief.template.json`** — add your brand's default audience and tone, so every brief starts closer to right.
2. **`presets/`** — write a preset for your niche (fitness, finance, food). Copy `kids-education.md`, change the vocabulary and safety rules.
3. **`references/07-style-recipes.md`** — keep the two looks you actually use; delete the rest so the agent stops offering Italian neorealism.
4. **`scripts/lint_storyboard.py` → `PLATFORMS`** — only if a real platform spec changed. Re-check the date before editing.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Agent starts writing prompts immediately | skill was summarised, not loaded | paste the full `SKILL.md`, not the description |
| Agent invents model capabilities | `03-models.md` not loaded | name the file in the request |
| Lint exits 2 | JSON syntax error | the message gives the line; `python3 -m json.tool storyboard.json` |
| QC exits 3 | no ffmpeg | `pip install imageio-ffmpeg` |
| Every storyboard fails `DURATION` | platform spelled differently | use the exact keys in `PLATFORMS` |
| Pacing warnings in a non-English language | calibration missing | add a row to `WPS` in `lint_storyboard.py` |
| Storyboard passes but the video still feels slow | the plan is sound; the edit is not | run `qc_video.py`, then check the mute-watch test |

## Compatibility

| Requirement | Status |
|---|---|
| `SKILL.md` at folder root | yes |
| Frontmatter `name` (≤64, kebab-case) | `video-studio` |
| Frontmatter `description` (≤1024 chars) | within limit |
| Progressive disclosure (`references/`) | yes, nine files, loaded on demand |
| Scripts runnable standalone | yes |
| License | MIT |

## What this skill will not do

- Promise face-lock on a model that does not support it.
- Judge whether the video is good.
- Verify audio, lip-sync or mix without you watching.
- Replace a strategy decision about *what* to make.
