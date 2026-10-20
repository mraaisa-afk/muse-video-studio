#!/usr/bin/env python3
"""
lint_storyboard.py — pre-flight gate for any video storyboard.

Generic: works for kids' education, product ads, talking heads, tutorials,
documentaries, music visuals — on any platform, in any language.

Reads storyboard.json (see assets/storyboard.template.json) and checks the
timing, pacing, structure, platform fit, sourcing and thumbnail before a
single credit is spent on generation.

Usage:
    python3 lint_storyboard.py storyboard.json
    python3 lint_storyboard.py storyboard.json --strict
    python3 lint_storyboard.py storyboard.json --markdown
    python3 lint_storyboard.py storyboard.json --json

Exit codes: 0 no FAIL · 1 at least one FAIL · 2 unreadable input
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# Platform profiles
# ─────────────────────────────────────────────────────────────────────────────
PLATFORMS = {
    "youtube_shorts":   dict(aspect="9:16", lo=8,    hi=180,   sweet=(15, 60),    outro=2.0,  shot=(5, 7),   title=100, tags=15, hashes=3),
    "youtube_long":     dict(aspect="16:9", lo=60,   hi=7200,  sweet=(180, 1200), outro=20.0, shot=(8, 12),  title=100, tags=20, hashes=3),
    "facebook_reels":   dict(aspect="9:16", lo=5,    hi=90,    sweet=(15, 45),    outro=2.0,  shot=(5, 7),   title=200, tags=10, hashes=5),
    "facebook_feed":    dict(aspect="4:5",  lo=5,    hi=14400, sweet=(30, 180),   outro=6.0,  shot=(6, 9),   title=200, tags=10, hashes=5),
    "instagram_reels":  dict(aspect="9:16", lo=5,    hi=180,   sweet=(15, 45),    outro=2.0,  shot=(4, 6),   title=200, tags=30, hashes=5),
    "instagram_feed":   dict(aspect="4:5",  lo=3,    hi=3600,  sweet=(15, 60),    outro=3.0,  shot=(5, 7),   title=200, tags=30, hashes=5),
    "tiktok":           dict(aspect="9:16", lo=5,    hi=600,   sweet=(12, 40),    outro=1.5,  shot=(3, 5),   title=150, tags=10, hashes=5),
    "linkedin":         dict(aspect="16:9", lo=15,   hi=900,   sweet=(30, 120),   outro=5.0,  shot=(6, 9),   title=200, tags=10, hashes=5),
    "x":                dict(aspect="16:9", lo=1,    hi=140,   sweet=(15, 45),    outro=2.0,  shot=(4, 6),   title=280, tags=5,  hashes=2),
}

# Words per second. Approximate — scripts are a proxy for speech, not a measurement.
WPS = {
    "en": dict(target=(2.2, 2.8), hard=(1.6, 3.1)),
    "bn": dict(target=(2.0, 2.6), hard=(1.5, 3.0)),
    "hi": dict(target=(2.1, 2.7), hard=(1.6, 3.1)),
    "ur": dict(target=(2.0, 2.6), hard=(1.5, 3.0)),
    "es": dict(target=(2.4, 3.2), hard=(1.8, 3.5)),
    "fr": dict(target=(2.3, 3.0), hard=(1.7, 3.3)),
    "pt": dict(target=(2.3, 3.0), hard=(1.7, 3.3)),
    "ar": dict(target=(2.0, 2.7), hard=(1.5, 3.1)),
    "id": dict(target=(2.2, 2.9), hard=(1.6, 3.2)),
    "default": dict(target=(2.2, 2.8), hard=(1.6, 3.1)),
}

STOPWORDS = {
    "en": "a an the and or but if so then than that this these those is am are was were be been being do does did have has had will would can could should may might must i you he she it we they me him her us them my your his its our their to of in on at for with by from up down out off over under again very just not no yes oh ah hey hi ok okay well now really all too as about into there here what which who when where why how one two got get".split(),
    "bn": "\u098f\u09ac\u0982 \u09ac\u09be \u0995\u09bf\u09a8\u09cd\u09a4\u09c1 \u09a4\u09be\u09b0 \u0986\u09b0 \u0986\u09ae\u09bf \u09a4\u09c1\u09ae\u09bf \u09b8\u09c7 \u098f\u0987 \u0993\u0987 \u098f\u0995\u099f\u09bf \u098f\u0995\u099f\u09be \u0995\u09b0\u09c7 \u09b9\u09af\u09bc \u099b\u09bf\u09b2 \u09a8\u09be \u0993 \u098f\u09b0 \u09af\u09c7 \u0995\u09bf \u0995\u09c0 \u09a5\u09c7\u0995\u09c7 \u099c\u09a8\u09cd\u09af \u09b8\u09be\u09a5\u09c7 \u09a4\u09be\u09b0 \u098f\u0987 \u09b8\u09c7\u0987 \u0986\u09ae\u09bf \u0986\u09ae\u09be\u09a6\u09c7\u09b0 \u09a4\u09cb\u09ae\u09be\u09b0 \u09ae\u09a8\u09c7 \u09ac\u09b2\u09cb \u098f\u0996\u09a8 \u09a4\u09ac\u09c7 \u09af\u09a6\u09bf \u09a4\u0996\u09a8 \u0985\u09a8\u09c7\u0995 \u0996\u09c1\u09ac \u09b6\u09c1\u09a7\u09c1 \u0986\u09b0\u0993 \u098f\u099f\u09be \u09b8\u09c7\u099f\u09be \u0995\u09b0\u09c7 \u09b9\u09af\u09bc\u09c7\u099b\u09bf\u09b2 \u09b9\u09b2\u09cb \u0986\u099b\u09c7 \u09a8\u09c7\u0987".split(),
    "default": "a an the and or but of to in on at for with by from is are was were be been this that it its i you he she we they".split(),
}

AGREEMENT = [
    r"^(yes|yeah|yep|right|exactly|true|correct)[,!. ]",
    r"^they (really )?did", r"^he (really )?did", r"^she (really )?did",
    r"^(that'?s|that is) (right|true|correct)",
    r"^(you'?re|you are) right", r"^(i|we) agree", r"^of course[,!. ]",
    r"^(mm+|hm+|uh huh|indeed)\b",
    "^(\u09b9\u09cd\u09af\u09be\u0981|\u09a0\u09bf\u0995|\u098f\u0995\u09a6\u09ae|\u09a4\u09be\u09ce\u0995\u09cd\u09b7\u09a3\u09bf\u0995)",
]
INTROS = [
    r"welcome back", r"welcome to", r"^hi (guys|kids|friends|everyone)",
    r"^hello (guys|kids|friends|everyone)", r"^hey (guys|kids|friends|everyone)",
    r"today we (will|are going to) (learn|talk|discuss)", r"in this video",
    r"let'?s (learn|start|begin|get started)", r"are you ready",
    "^(\u09b8\u09cd\u09ac\u09be\u0997\u09a4\u09ae|\u0986\u099c \u0986\u09ae\u09b0\u09be|\u098f\u0987 \u09ad\u09bf\u09a1\u09bf\u0993\u09a4\u09c7)",
]
ENDCARDS = [r"end-card", r"endcard", r"title-card", r"outro-card", r"logo", r"static-end"]

SAFETY_KIDS = [
    r"\bscary\b", r"\bblood\b", r"\bgun\b", r"\bkill", r"\bdie\b", r"\bdeath\b",
    r"\bhate\b", r"\bstupid\b", r"\bidiot\b", r"\bwar\b", r"\bweapon", r"\bsword\b",
    r"\bslave", r"\bbuy now\b", r"\bsale\b", r"\bcheap\b", r"\bdiscount\b",
    r"\bshop\b", r"\bpurchase\b", r"\bsubscribe\b",
]
SAFETY_GENERAL = [
    r"\bkill\b", r"\bgore\b", r"\bnude\b", r"\bsex\b", r"\bdrugs?\b",
    r"\bsuicide\b", r"\bself[- ]harm\b", r"\bterrorist\b", r"\bbomb\b",
    r"\bguaranteed cure\b", r"\blose \d+ ?(kg|pounds|lbs)\b",
]
KIDS_AGE = {"kids_0_8", "kids", "children", "family"}
SOURCE_REQUIRED = {"education", "documentary", "news", "explainer", "kids_edu", "tutorial"}


@dataclass
class Finding:
    severity: str
    code: str
    detail: str
    fix: str = ""


@dataclass
class Report:
    findings: list[Finding] = field(default_factory=list)

    def add(self, sev: str, code: str, detail: str, fix: str = ""):
        self.findings.append(Finding(sev, code, detail, fix))

    def count(self, sev: str) -> int:
        return sum(1 for f in self.findings if f.severity == sev)

    @property
    def verdict(self) -> str:
        if self.count("FAIL"):
            return "FIX FIRST"
        return "PUBLISH-READY" if self.count("WARN") < 3 else "PASS WITH WARNINGS"


# ── helpers ─────────────────────────────────────────────────────────────────
TOKEN_SPLIT = re.compile(r"\S+")
TRIM_CHARS = ".,!?;:\"'()[]{}…—–-।॥«»<>"
CJK = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uac00-\ud7af]")


def words(text: str) -> list[str]:
    """Whitespace tokens with edge punctuation trimmed.

    Keeps Indic scripts intact: viramas and matras are combining marks, so a
    regex over Unicode letters shreds Bengali/Hindi words into fragments.
    CJK has no spaces, so its characters are estimated at ~2 chars per word.
    """
    out: list[str] = []
    for tok in TOKEN_SPLIT.findall(text or ""):
        tok = tok.strip(TRIM_CHARS)
        if not tok:
            continue
        cjk = CJK.findall(tok)
        if cjk and len(cjk) >= max(2, len(tok) // 2):
            out.extend(["字"] * max(1, round(len(cjk) / 2)))
        else:
            out.append(tok)
    return out


def content_words(text: str, lang: str) -> set[str]:
    stop = set(STOPWORDS.get(lang, STOPWORDS["default"]))
    return {w.lower() for w in words(text) if w.lower() not in stop}


def jaccard(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if a and b else 0.0


def t(sec: float) -> str:
    m, s = divmod(max(0.0, float(sec)), 60)
    return f"{int(m):02d}:{s:05.2f}"


def hits(patterns, text):
    low = (text or "").lower()
    return [p for p in patterns if re.search(p, low)]


# ── checks ──────────────────────────────────────────────────────────────────
def check(sb: dict, strict: bool = False) -> Report:
    r = Report()
    p = sb.get("project") or {}
    platform = (p.get("platform") or "youtube_shorts").lower()
    cfg = PLATFORMS.get(platform, PLATFORMS["youtube_shorts"])
    lang = (p.get("language") or "en").lower()
    pace = WPS.get(lang, WPS["default"])
    beats = sorted(sb.get("beats") or [], key=lambda b: float(b.get("start", 0)))
    kind = (p.get("content_type") or "explainer").lower()
    age = (p.get("audience_age") or "general").lower()
    kids = age in KIDS_AGE or kind in {"kids_edu"}

    if not beats:
        r.add("FAIL", "EMPTY", "no beats in the storyboard", "Add a timed beat sheet.")
        return r

    for b in beats:
        b["start"] = float(b.get("start", 0))
        if b.get("end") is None:
            b["end"] = b["start"] + max(1.0, len(words(b.get("text", ""))) / pace["target"][1])
        b["end"] = float(b["end"])

    dur = float((sb.get("outro") or {}).get("video_end") or beats[-1]["end"])

    # 1 duration vs platform
    if dur < cfg["lo"]:
        r.add("FAIL", "DURATION", f"{dur:.1f}s is below the {platform} minimum ({cfg['lo']}s)")
    elif dur > cfg["hi"]:
        r.add("FAIL", "DURATION", f"{dur:.1f}s exceeds the {platform} maximum ({cfg['hi']}s)")
    elif not (cfg["sweet"][0] <= dur <= cfg["sweet"][1]):
        r.add("WARN", "DURATION", f"{dur:.1f}s is outside the {platform} sweet spot {cfg['sweet'][0]}-{cfg['sweet'][1]}s",
              "Move toward the sweet spot unless the format demands otherwise.")

    # 2 aspect
    want = cfg["aspect"]
    have = (p.get("aspect") or want).replace(" ", "")
    if have != want and not (platform in {"youtube_shorts", "youtube_long"} and have in {"9:16", "16:9"}):
        r.add("WARN", "ASPECT", f"aspect {have} does not match {platform} ({want})",
              "Pick the platform's native ratio; do not letterbox a vertical into a horizontal.")

    # 3 hook
    h = beats[0]
    if h["start"] > 0.4:
        r.add("FAIL", "HOOK-START", f"first beat starts at {h['start']:.2f}s", "Cut the pre-roll to zero.")
    hook_cap = 3.0 if platform.endswith("shorts") or platform in {"tiktok", "instagram_reels", "facebook_reels"} else 8.0
    if h["end"] - h["start"] > hook_cap:
        r.add("WARN", "HOOK-LEN", f"hook runs {h['end'] - h['start']:.1f}s (cap {hook_cap:.0f}s)", "Tighten it.")
    if hits(INTROS, h.get("text", "")):
        r.add("FAIL", "HOOK-INTRO", f"hook opens with housekeeping: \"{(h.get('text') or '')[:40]}\"",
              "Open on the claim, the stake or the action.")
    if hits(ENDCARDS, h.get("shot", "")):
        r.add("FAIL", "HOOK-CARD", f"hook is a card shot ({h.get('shot')})", "Never open on a logo or title card.")
    if "?" not in (h.get("text") or "") and (h.get("type") or "") != "hook":
        pass
    if "?" not in (h.get("text") or "") and not (h.get("on_screen") or "").strip():
        r.add("WARN", "HOOK-QUESTION", "hook contains no question or on-screen text",
              "A question or a bold claim creates the reason to keep watching.")

    # 4 timeline
    for a, b in zip(beats, beats[1:]):
        gap = b["start"] - a["end"]
        if gap < -0.01:
            r.add("FAIL", "OVERLAP", f"beat {b['id']} starts {-gap:.2f}s before beat {a['id']} ends")
        elif gap > 0.45:
            r.add("FAIL", "GAP", f"{gap:.2f}s of dead air between beat {a['id']} ({t(a['end'])}) and beat {b['id']} ({t(b['start'])})",
                  "Close it in the edit; target <= 0.45s.")
        elif gap > 0.25:
            r.add("WARN", "GAP", f"{gap:.2f}s gap between beats {a['id']} and {b['id']}", "Fine if music or a visual beat covers it.")

    # 5 repetition
    spoken = [b for b in beats if words(b.get("text", ""))]
    for a, b in zip(spoken, spoken[1:]):
        score = jaccard(content_words(a.get("text", ""), lang), content_words(b.get("text", ""), lang))
        if score >= 0.6:
            r.add("FAIL", "DUP", f"beat {b['id']} repeats beat {a['id']} ({score:.0%} overlap of content words)",
                  "Delete one, or replace it with a reaction or a visual.")
        if hits(AGREEMENT, b.get("text", "")):
            r.add("WARN", "AGREE", f"beat {b['id']} is an agreement line", "Replace with a reaction shot or a sting.")

    # 6 pace
    lang_warned = lang not in WPS
    if lang_warned:
        r.add("WARN", "LANGUAGE", f"no pacing calibration for '{lang}' — using the default 2.2-2.8 wps",
              "Check one recorded line against the estimate.")
    total = 0
    for b in beats:
        n = len(words(b.get("text", "")))
        total += n
        if n < 4 or (b.get("type") or "") in {"quiz", "reveal", "loop", "pause"}:
            continue
        d = b["end"] - b["start"]
        if d <= 0:
            continue
        w = n / d
        if not (pace["hard"][0] <= w <= pace["hard"][1]):
            r.add("FAIL", "WPS", f"beat {b['id']} is {w:.2f} words/sec ({n}w / {d:.1f}s) — outside {pace['hard'][0]}-{pace['hard'][1]}",
                  "Rewrite the line length; do not change voice speed.")
        elif not (pace["target"][0] <= w <= pace["target"][1]):
            r.add("WARN", "WPS", f"beat {b['id']} is {w:.2f} words/sec — outside the {pace['target'][0]}-{pace['target'][1]} target")

    budget = round(max(10, dur - 4) * pace["target"][1])
    if total > budget:
        r.add("WARN", "WORD-BUDGET", f"{total} spoken words for {dur:.0f}s (budget ~{budget})", "Cut a beat, not the pauses.")

    # 7 quiz (only when the format asks for one)
    quiz = sb.get("quiz")
    if p.get("requires_quiz"):
        if not quiz:
            r.add("FAIL", "QUIZ-MISSING", "requires_quiz is true but there is no quiz block")
        else:
            qs, qe = float(quiz.get("start", 0)), float(quiz.get("end", 0))
            qlen = qe - qs
            if qlen < 3:
                r.add("FAIL", "QUIZ-LEN", f"quiz is on screen {qlen:.1f}s", "Give at least 3s to read and answer.")
            elif qlen > 6:
                r.add("WARN", "QUIZ-LEN", f"quiz is on screen {qlen:.1f}s", "Over 6s stalls.")
            opts = quiz.get("options") or []
            if len(opts) < 2:
                r.add("FAIL", "QUIZ-TEXT", f"{len(opts)} on-screen options", "Show at least two labelled options.")
            elif not all(re.match(r"^\s*[A-D][\).]", str(o)) for o in opts):
                r.add("WARN", "QUIZ-TEXT", "options are not letter-labelled", "Use 'A) ...' / 'B) ...'.")
            if not quiz.get("countdown"):
                r.add("WARN", "QUIZ-COUNTDOWN", "no countdown", "A timer is the affordance to answer.")
            if (quiz.get("layout") or "").lower() not in {"full-screen-card", "overlay-card", "split-card"}:
                r.add("FAIL", "QUIZ-LAYOUT", f"quiz layout is '{quiz.get('layout')}'",
                      "Never ask a question over a talking shot; cut to a card.")

    # 8 outro
    outro = sb.get("outro") or {}
    last = outro.get("last_word_end")
    if last is None:
        last = max((b["end"] for b in spoken), default=dur)
    tail = dur - float(last)
    if tail > cfg["outro"]:
        r.add("FAIL", "OUTRO-TAIL", f"{tail:.2f}s of video after the last spoken word (cap {cfg['outro']}s)",
              "Trim the tail and close the gap.")
    elif tail > cfg["outro"] * 0.8:
        r.add("WARN", "OUTRO-TAIL", f"{tail:.2f}s tail — near the cap", "Keep motion in it.")
    if p.get("requires_loop") and outro.get("loop_seam") is False:
        r.add("WARN", "LOOP-SEAM", "loop_seam is false", "Match the last frame to the first for re-watch.")
    if (p.get("goal") or "") == "conversion" and not any(b.get("type") == "cta" for b in beats):
        r.add("FAIL", "CTA-MISSING", "goal is conversion but there is no cta beat")
    elif not any(b.get("type") == "cta" for b in beats):
        r.add("WARN", "CTA-MISSING", "no cta beat", "Give the viewer one next action.")

    # 9 shot cadence
    warn_s, fail_s = cfg["shot"]
    for b in beats:
        length = b["end"] - b["start"]
        if length > fail_s:
            r.add("FAIL", "SHOT-LENGTH", f"beat {b['id']} holds one shot {length:.1f}s (cap {fail_s}s)",
                  "Add a cutaway, a reaction, or move the camera.")
        elif length > warn_s:
            r.add("WARN", "SHOT-LENGTH", f"beat {b['id']} holds one shot {length:.1f}s")
    want_beats = max(4, math.ceil(dur / (6 if dur < 180 else 15)))
    if len(beats) < want_beats:
        r.add("WARN", "SHOT-COUNT", f"{len(beats)} beats for {dur:.0f}s (want ~{want_beats})", "More cuts, same script.")
    for b in beats[1:]:
        if hits(ENDCARDS, b.get("shot", "")):
            r.add("FAIL", "END-CARD", f"beat {b['id']} is a static card ({b.get('shot')})", "Cards belong in long-form endscreens only.")

    # 10 safety
    rules = SAFETY_KIDS if kids else SAFETY_GENERAL
    for b in beats:
        for fld in ("text", "on_screen"):
            low = (b.get(fld) or "").lower()
            found = {m.group(0) for pat in rules if (m := re.search(pat, low))}
            if not found:
                continue
            term = max(found, key=len)
            if term == "subscribe":
                r.add("WARN", "SAFETY", f"beat {b['id']} says 'subscribe'", "Put the ask on screen, not in the script.")
            else:
                r.add("FAIL", "SAFETY", f"beat {b['id']} contains '{term}' ({fld})",
                      "Rewrite. Kids' content and ad policy both reject this.")

    # 11 sourcing
    if not (sb.get("analysis") or {}).get("core_message"):
        sev = "FAIL" if kind in SOURCE_REQUIRED else "WARN"
        r.add(sev, "CORE-MESSAGE", "analysis.core_message is empty", "One sentence: what is this video arguing?")
    needs_src = kind in SOURCE_REQUIRED or kids
    for b in beats:
        if (b.get("type") or "") in {"fact", "proof"} and needs_src and not b.get("claim_source"):
            r.add("FAIL", "FACT", f"beat {b['id']} makes a factual claim with no claim_source",
                  "Add it to analysis.facts[] and reference it, or cut the claim.")
    if needs_src and not (sb.get("analysis") or {}).get("facts"):
        r.add("WARN", "FACT", "no analysis.facts[] entry", "Source the claims before publishing.")

    # 12 characters
    cast = {c.lower() for c in (p.get("characters") or [])}
    for b in beats:
        sp = (b.get("speaker") or "").strip().lower()
        if sp and cast and sp not in cast:
            r.add("WARN", "CHARACTER", f"beat {b['id']} speaker '{sp}' is not in project.characters[]")

    # 13 on-screen text
    for b in beats:
        os_ = (b.get("on_screen") or "").strip()
        if len(os_) > 60:
            r.add("WARN", "ONSCREEN-LEN", f"beat {b['id']} has {len(os_)} chars of on-screen text", "Cut to the words that must be read.")

    # 14 thumbnail
    th = sb.get("thumbnail") or {}
    if not (th.get("text") or "").strip():
        r.add("WARN", "THUMB-MISSING", "no thumbnail text", "2-4 words that do not repeat the title.")
    else:
        n = len(words(th["text"]))
        if n > 5:
            r.add("WARN", "THUMB-WORDS", f"thumbnail text is {n} words", "2-4 words maximum.")
        title_words = {w.lower() for w in words((sb.get("publish") or {}).get("title", ""))}
        th_words = {w.lower() for w in words(th["text"])}
        if th_words and th_words <= title_words:
            r.add("WARN", "THUMB-REPEAT", "thumbnail text repeats the title",
                  "The image shows; the words should argue something else.")

    # 15 publish fields
    pub = sb.get("publish") or {}
    title = pub.get("title") or ""
    if not title:
        r.add("FAIL", "TITLE-MISSING", "no publish.title")
    elif len(title) > cfg["title"]:
        r.add("FAIL", "TITLE-LEN", f"title is {len(title)} chars (cap {cfg['title']})")
    kw = (pub.get("primary_keyword") or "").strip().lower()
    if kw and title:
        if kw not in title.lower():
            r.add("WARN", "KEYWORD", f"primary keyword '{kw}' is not in the title")
        elif title.lower().index(kw) > 40:
            r.add("WARN", "KEYWORD-POS", f"keyword starts at char {title.lower().index(kw)} — after the visible cut",
                  "Move it into the first 40 characters.")
    hashes = pub.get("hashtags") or []
    if len(hashes) > cfg["hashes"]:
        r.add("WARN", "HASHTAGS", f"{len(hashes)} hashtags (platform sweet spot is <= {cfg['hashes']})")
    if not (pub.get("pinned_comment") or "").strip():
        r.add("WARN", "PINNED", "no pinned_comment", "Ask the question you want answered.")

    if strict:
        for f in r.findings:
            if f.severity == "WARN":
                f.severity = "FAIL"
    return r


def render(r: Report, sb: dict, markdown: bool = False) -> str:
    p = sb.get("project") or {}
    head = f"{p.get('id', 'project')} · {p.get('content_type', '?')} · {p.get('platform', '?')} · {p.get('language', '?')}"
    order = {"FAIL": 0, "WARN": 1}
    rows = sorted(r.findings, key=lambda f: (order.get(f.severity, 2), f.code))
    out = []
    if markdown:
        out.append(f"**Pre-flight — {head}**\n")
        out.append("| Severity | Rule | Finding | Fix |")
        out.append("|---|---|---|---|")
        for f in rows:
            out.append(f"| {f.severity} | `{f.code}` | {f.detail} | {f.fix} |")
    else:
        out.append("=" * 80)
        out.append(f"  STORYBOARD LINT  ·  {head}")
        out.append("=" * 80)
        if not rows:
            out.append("  (no findings)")
        for f in rows:
            out.append(f"  [{f.severity:<4}] {f.code:<15} {f.detail}")
            if f.fix:
                out.append(f"           {'':<15} -> {f.fix}")
    out.append("")
    line = f"FAIL {r.count('FAIL')}   WARN {r.count('WARN')}   VERDICT: {r.verdict}"
    out.append(f"**{line}**" if markdown else f"  {line}")
    if r.count("FAIL") == 0:
        tail = "Structure is sound. Voice, lip-sync and mix still need a human check after render."
        out.append(f"*{tail}*" if markdown else f"  {tail}")
    return "\n".join(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Pre-flight lint for any video storyboard.")
    ap.add_argument("storyboard", type=Path)
    ap.add_argument("--strict", action="store_true", help="treat WARN as FAIL")
    ap.add_argument("--markdown", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    try:
        sb = json.loads(a.storyboard.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"error: {a.storyboard} not found", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"error: invalid JSON — {e}", file=sys.stderr)
        return 2

    rep = check(sb, strict=a.strict)
    if a.json:
        print(json.dumps({"verdict": rep.verdict,
                          "counts": {s: rep.count(s) for s in ("FAIL", "WARN")},
                          "findings": [f.__dict__ for f in rep.findings]}, indent=2, ensure_ascii=False))
    else:
        print(render(rep, sb, markdown=a.markdown))
    return 0 if rep.count("FAIL") == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
