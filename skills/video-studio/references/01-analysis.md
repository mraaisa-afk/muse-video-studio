# Stage 1 — Deep analysis of whatever you were handed

The quality of the video is decided here. Prompt engineering cannot rescue a brief that does not know what it is arguing.

## 1. Classify the input

| Input | What the user usually means | What you must extract |
|---|---|---|
| One-line topic | "Make something about X" | the angle they have not chosen yet |
| Article / blog / URL | "Turn this into a video" | the argument, not the table of contents |
| PDF / doc / notes | "Use my research" | claims, numbers, quotes, the one surprising finding |
| Existing video | "Make it better / shorter" | what works in seconds 0–3, where retention dies |
| Product / photo | "Sell this" | the one objection it removes |
| Personal story | "Tell my story" | the turn, the cost, the lesson |
| Data / dashboard | "Explain this" | the single comparison that lands |

If the input is a URL or file you cannot read, say so in one line and ask for the text. Do not invent its contents.

## 2. Produce the brief

Fill `assets/brief.template.json`. The fields that matter:

**`core_message`** — one sentence, under 20 words, that a stranger could repeat. If you cannot write it, the input is not ready and you should say which piece is missing.

**`audience`** — who exactly, and what they already believe. "Everyone" is not an audience. The useful form is: *"[specific person] who currently thinks [X] and needs to know [Y]."*

**`proof[]`** — numbers, names, demos, before/after. A video without proof is an opinion with music.

**`hook_angles[]`** — five, ranked. See the hook taxonomy below.

**`risks[]`** — unverifiable claims, rights, safety, platform policy, and anything that will get the video demonetised or removed.

**`assumptions[]`** — every gap you filled yourself. Write it down, so the user can correct it cheaply now instead of after generation.

## 3. The hook taxonomy

Rank by expected retention, not by cleverness.

| Type | Shape | Example |
|---|---|---|
| **Contradiction** | the audience's belief is false | "The pyramids were already ancient when Ramesses was born." |
| **Number** | one surprising figure | "This 40-second clip took 11 hours." |
| **Stake** | what is lost if they scroll | "Every day you post without this, you lose the same viewer twice." |
| **Question** | a gap they must close | "Why did the cheapest option outlast the expensive one?" |
| **Demonstration** | show the result first | open on the finished cake, then rewind |
| **Confession** | a mistake with a cost | "I wasted 3,000 dollars on ads before I understood this." |
| **Cold open** | start mid-action, no context | someone already running, already shouting |

Rules:
- A hook is spoken **and** shown. If the visual contradicts the line, the visual wins.
- Under 8 words spoken for short-form; under 12 for long-form.
- Never open with a logo, a title card, or "hi guys".
- Never open with a question the audience does not care about yet ("Have you ever wondered about insurance?").

## 4. Choose the format

Match the material to a structure. Do not force a 3-act story onto a listicle.

| Material | Structure |
|---|---|
| One strong claim + proof | **Claim → proof → payoff** (30–60 s) |
| A process with steps | **Problem → 3 steps → result** (60–180 s) |
| A story with a turn | **Setup → turn → consequence → lesson** (45–90 s) |
| Product | **Objection → demo → proof → offer** (15–30 s) |
| Comparison | **A vs B → decisive test → verdict** (30–90 s) |
| Explainer / educational | **Question → wrong belief → correction → check** (45–120 s) |
| Data | **Surprising chart → why → what to do** (30–60 s) |

Name the structure in the brief. The storyboard must follow it.

## 5. Audience calibration

- **Children (under 8):** one idea per 8 words, concrete nouns, no abstraction, no scary faces, no purchase language, bright palette, a question they can answer.
- **Teens:** speed, self-reference, visible craft, no lecturing.
- **Adults, general:** a stake they recognise within 3 seconds.
- **Professionals / B2B:** the claim first, the evidence second, the caveat third. No hype adjectives.
- **Skeptics:** concede the strongest counter-argument out loud, then answer it.

## 6. Depth checks before you leave stage 1

Answer all of these. If any answer is "I don't know", either ask (max 3 questions) or write an assumption.

1. What is the one sentence the viewer repeats to a friend?
2. What do they currently believe that this video changes?
3. What is the strongest counter-argument, and where does the video handle it?
4. What is the proof, and is it on screen or only spoken?
5. What is the emotional beat — curiosity, relief, delight, indignation, pride?
6. What is the CTA, and is it the single next action?
7. What is the platform's job here — search, browse, shares, or comments?
8. What would make this video get removed or age-restricted?
9. What visual does this idea deserve that a talking head cannot give it?
10. If the viewer watches only 3 seconds, what do they get?

## 7. Angle statement

Before writing beats, say this out loud to the user in one sentence:

> "This video argues that **____**, for **____**, using **____** as proof, ending with **____**."

If the sentence is awkward, the video will be too. Rewrite the angle, not the sentence.

## 8. Thin-input protocol

When the user gives almost nothing:

1. Ask at most **3** questions, choosing the ones that unlock the most: audience, the one thing to be believed, and the platform.
2. If unanswered, proceed with explicit assumptions in `brief.json`.
3. Generate the brief anyway. A confident wrong angle the user can correct is more useful than a list of questions.

Never stall a job waiting for perfect information. Never silently invent facts.
