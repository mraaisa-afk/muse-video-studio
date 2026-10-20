# Case cards

One file per shipped video. The point is not documentation — it is that the next video starts from evidence instead of taste.

## Template

```markdown
# Case NN — "<title>"

Format / platform / runtime:
Model(s) used:
Result: views / retention / whatever you can measure

## What shipped
One paragraph. No adjectives.

## What worked
Evidence, not opinions. Timestamp or metric.

## What failed
| # | Timestamp / metric | Finding | Severity |
|---|---|---|---|

## Root cause
Why it failed. Be specific: a scripted beat, a missing card, a template imported from the wrong format.

## Rule change
Which rule now prevents it, in which file. If no rule changed, say so.

## Transferable lesson
One sentence another creator could use.
```

## Case 01 — the review that built this skill

A kids' history Short, ~54 s, nine beats, one B-roll cutaway at 00:10.

| # | Where | Finding | Now enforced by |
|---|---|---|---|
| 1 | 00:26–00:32 | 1.5–2 s pause plus a repeated talking point before the quiz | `GAP` (> 0.45 s) and `DUP` (≥ 60% content-word overlap) |
| 2 | 00:33–00:38 | quiz asked over a static side-profile shot; no question, options or timer on screen | `QUIZ-LAYOUT`, `QUIZ-TEXT`, `QUIZ-COUNTDOWN` |
| 3 | 00:48–00:54 | 6 s static freeze after the CTA finished | `OUTRO-TAIL` (> 2 s) and `FREEZE-TAIL` in render QC |
| 4 | whole | shot cadence too slow for vertical | `SHOT-LENGTH` (5 s warn / 7 s fail) |
| 5 | 00:10 | the best moment in the video was an accidental cutaway | now a required TURN beat in the kids preset |

**Root cause:** agreement beats were scripted, the quiz was treated as dialogue instead of a graphic, and a long-form end card was imported into a vertical format.

**Transferable lesson:** a reaction is cheaper than a line, and vertical video ends on a question, not a card.
