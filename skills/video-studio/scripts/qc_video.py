#!/usr/bin/env python3
"""
qc_video.py — post-render gate for Fun Education TV Shorts.

Measures the rendered file the way a reviewer would, but with numbers:
  * duration
  * trailing freeze (the 6-second static outro defect)
  * silence gaps inside dialogue (the 00:26-00:32 dead-air defect)
  * shot cadence (longest uncut hold)
  * integrated loudness and true peak

Usage:
    python3 qc_video.py final.mp4
    python3 qc_video.py final.mp4 --json-out qc.json
    python3 qc_video.py final.mp4 --no-scene          # skip scene detection (faster)

Requires ffmpeg on PATH, or the imageio-ffmpeg packaged binary.

Exit codes:
    0  no FAIL findings
    1  at least one FAIL finding
    3  ffmpeg not available / unreadable file
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

# Platform profiles: (hard_min, hard_max, sweet_min, sweet_max)
PLATFORMS = {
    "youtube_shorts":  (8, 180, 15, 60),
    "youtube_long":    (60, 7200, 180, 1200),
    "facebook_reels":  (5, 90, 15, 45),
    "instagram_reels": (5, 180, 15, 45),
    "tiktok":          (5, 600, 12, 40),
    "linkedin":        (15, 900, 30, 120),
    "x":               (1, 140, 15, 45),
    "generic":         (5, 3600, 15, 60),
}
PLATFORM = "youtube_shorts"
DUR_MIN, DUR_MAX = 8.0, 180.0
SWEET_MIN, SWEET_MAX = 15.0, 60.0
LUFS_TARGET, LUFS_LO, LUFS_HI = -14.0, -16.0, -13.0
FREEZE_WARN, FREEZE_FAIL = 1.6, 2.0
SILENCE_WARN, SILENCE_FAIL = 0.45, 0.60
SHOT_WARN, SHOT_FAIL = 5.0, 7.0
LOUD_LO, LOUD_HI = -16.0, -13.0
PEAK_MAX = -1.5


@dataclass
class Finding:
    severity: str
    code: str
    detail: str
    fix: str = ""


@dataclass
class QC:
    findings: list[Finding] = field(default_factory=list)
    metrics: dict = field(default_factory=dict)

    def add(self, sev, code, detail, fix=""):
        self.findings.append(Finding(sev, code, detail, fix))

    def count(self, s):
        return sum(1 for f in self.findings if f.severity == s)

    @property
    def verdict(self):
        if self.count("FAIL"):
            return "FIX FIRST"
        return "PUBLISH-READY" if self.count("WARN") < 3 else "PASS WITH WARNINGS"


def find_ffmpeg() -> str | None:
    for cand in (os.environ.get("FFMPEG_BINARY"), "ffmpeg"):
        if cand and shutil.which(cand):
            return shutil.which(cand)
    try:
        import imageio_ffmpeg  # type: ignore
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return None


def run(cmd: list[str]) -> str:
    proc = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    return (proc.stdout or "") + (proc.stderr or "")


def probe_duration(ffmpeg: str, src: Path) -> float:
    ffprobe = shutil.which("ffprobe")
    if ffprobe:
        out = run([ffprobe, "-v", "error", "-show_entries", "format=duration",
                   "-of", "default=nw=1:nk=1", str(src)]).strip()
        try:
            return float(out)
        except ValueError:
            pass
    out = run([ffmpeg, "-hide_banner", "-i", str(src), "-f", "null", "-"])
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", out)
    if not m:
        return 0.0
    h, mi, s = m.groups()
    return int(h) * 3600 + int(mi) * 60 + float(s)


def detect_freezes(ffmpeg: str, src: Path, total: float, min_len: float = 0.5) -> list[tuple[float, float]]:
    out = run([ffmpeg, "-hide_banner", "-nostats", "-i", str(src), "-an",
               "-vf", f"freezedetect=n=-60dB:d={min_len}", "-f", "null", "-"])
    starts = [float(x) for x in re.findall(r"freeze_start:\s*([\d.]+)", out)]
    ends = [float(x) for x in re.findall(r"freeze_end:\s*([\d.]+)", out)]
    durs = [float(x) for x in re.findall(r"freeze_duration:\s*([\d.]+)", out)]
    pairs = []
    for i, s in enumerate(starts):
        if i < len(ends):
            e = ends[i]
        elif i < len(durs):
            e = s + durs[i]
        else:
            e = total          # freeze ran to the end of file: no freeze_end is emitted
        pairs.append((s, e))
    return pairs


def detect_silences(ffmpeg: str, src: Path, noise_db: int = -35, min_len: float = 0.5) -> list[tuple[float, float]]:
    out = run([ffmpeg, "-hide_banner", "-nostats", "-i", str(src), "-vn",
               "-af", f"silencedetect=n={noise_db}dB:d={min_len}", "-f", "null", "-"])
    starts = [float(x) for x in re.findall(r"silence_start:\s*(-?[\d.]+)", out)]
    ends = [float(x) for x in re.findall(r"silence_end:\s*(-?[\d.]+)", out)]
    durs = [float(x) for x in re.findall(r"silence_duration:\s*([\d.]+)", out)]
    pairs = []
    for i, s in enumerate(starts):
        e = ends[i] if i < len(ends) else (s + durs[i] if i < len(durs) else None)
        if e is not None:
            pairs.append((max(0.0, s), e))
    return pairs


def detect_scenes(ffmpeg: str, src: Path, threshold: float = 0.25) -> list[float]:
    out = run([ffmpeg, "-hide_banner", "-nostats", "-i", str(src), "-an",
               "-vf", f"select='gt(scene,{threshold})',showinfo", "-f", "null", "-"])
    return sorted({float(x) for x in re.findall(r"pts_time:([\d.]+)", out)})


def detect_loudness(ffmpeg: str, src: Path) -> tuple[float | None, float | None]:
    out = run([ffmpeg, "-hide_banner", "-nostats", "-i", str(src), "-vn",
               "-af", "ebur128=peak=true", "-f", "null", "-"])
    integ = re.findall(r"I:\s*(-?[\d.]+)\s*LUFS", out)
    peaks = re.findall(r"Peak:\s*(-?[\d.]+)\s*dBFS", out)
    i = float(integ[-1]) if integ else None
    p = float(peaks[-1]) if peaks else None
    return i, p


def analyse(src: Path, ffmpeg: str, do_scene: bool = True) -> QC:
    qc = QC()
    dur = probe_duration(ffmpeg, src)
    qc.metrics["duration_s"] = round(dur, 2)
    if dur <= 0:
        qc.add("FAIL", "UNREADABLE", "could not read a duration from the file",
               "Confirm the render finished and the container is closed.")
        return qc

    # --- duration
    if dur < DUR_MIN:
        qc.add("FAIL", "DURATION", f"{dur:.1f} s is under the {PLATFORM} minimum ({DUR_MIN:.0f} s)", "Add a beat or a payoff.")
    elif dur > DUR_MAX:
        qc.add("FAIL", "DURATION", f"{dur:.1f} s exceeds the {PLATFORM} maximum ({DUR_MAX:.0f} s)", "Cut a beat.")
    elif not (SWEET_MIN <= dur <= SWEET_MAX):
        qc.add("WARN", "DURATION", f"{dur:.1f} s is outside the {PLATFORM} sweet spot {SWEET_MIN:.0f}-{SWEET_MAX:.0f} s")

    # --- trailing freeze
    freezes = detect_freezes(ffmpeg, src, dur)
    qc.metrics["freezes"] = [{"start": round(a, 2), "end": round(b, 2)} for a, b in freezes]
    tail = 0.0
    if freezes:
        last_start, last_end = freezes[-1]
        if dur - last_end <= 1.0:  # freeze runs to the end of file
            tail = dur - last_start
            qc.metrics["freeze_tail_s"] = round(tail, 2)
    if tail > FREEZE_FAIL:
        qc.add("FAIL", "FREEZE-TAIL",
               f"picture is static for the last {tail:.1f} s (from {fmt(dur - tail)} to {fmt(dur)})",
               "Trim to last word + 1-2 s and close the gap. Never hold an end card.")
    elif tail > FREEZE_WARN:
        qc.add("WARN", "FREEZE-TAIL", f"static tail of {tail:.1f} s", "Keep motion (blink, drift, pulse) in the tail.")

    # --- silence
    silences = detect_silences(ffmpeg, src)
    qc.metrics["silences"] = [{"start": round(a, 2), "end": round(b, 2), "len": round(b - a, 2)} for a, b in silences]
    inner = [(a, b) for a, b in silences if a > 0.5 and b < dur - 1.0]
    worst = max(inner, key=lambda p: p[1] - p[0], default=None)
    if worst:
        length = worst[1] - worst[0]
        if length > SILENCE_FAIL:
            qc.add("FAIL", "SILENCE", f"{length:.2f} s of silence at {fmt(worst[0])}-{fmt(worst[1])}",
                   "Trim the clip tail in assembly. Target gap <= 0.45 s.")
        elif length > SILENCE_WARN:
            qc.add("WARN", "SILENCE", f"{length:.2f} s pause at {fmt(worst[0])}-{fmt(worst[1])}",
                   "Fine only if music carries it.")

    # --- shot cadence
    if do_scene:
        cuts = detect_scenes(ffmpeg, src)
        qc.metrics["scene_cuts"] = [round(c, 2) for c in cuts]
        qc.metrics["shot_count"] = len(cuts) + 1
        marks = [0.0] + cuts + [dur]
        lengths = [b - a for a, b in zip(marks, marks[1:])]
        longest = max(lengths) if lengths else dur
        qc.metrics["longest_shot_s"] = round(longest, 2)
        idx = lengths.index(longest)
        if longest > SHOT_FAIL:
            qc.add("FAIL", "SHOT-CADENCE",
                   f"one shot holds {longest:.1f} s ({fmt(marks[idx])}-{fmt(marks[idx + 1])})",
                   "Add a cutaway or a reaction shot. Max 5 s per setup.")
        elif longest > SHOT_WARN:
            qc.add("WARN", "SHOT-CADENCE", f"longest shot is {longest:.1f} s at {fmt(marks[idx])}",
                   "Aim for <= 5 s per setup.")
        if len(cuts) + 1 < 8:
            qc.add("WARN", "SHOT-COUNT", f"only {len(cuts) + 1} detected shots",
                   "A 50 s Short wants 8-14. Raise the cut rhythm.")

    # --- loudness
    integ, peak = detect_loudness(ffmpeg, src)
    qc.metrics["lufs_i"] = integ
    qc.metrics["true_peak_dbfs"] = peak
    if integ is not None and not (LUFS_LO <= integ <= LUFS_HI):
        qc.add("WARN", "LOUDNESS", f"integrated loudness {integ:.1f} LUFS (target {LUFS_LO:.0f} to {LUFS_HI:.0f})",
               f"Normalise the master to {LUFS_TARGET:.0f} LUFS.")
    if peak is not None and peak > PEAK_MAX:
        qc.add("WARN", "TRUEPEAK", f"true peak {peak:.1f} dBFS (limit {PEAK_MAX})",
               "Lower the limiter ceiling to -1.5 dBTP.")
    return qc


def fmt(s: float) -> str:
    m, sec = divmod(max(0.0, s), 60)
    return f"{int(m):02d}:{sec:05.2f}"


def render(qc: QC, src: Path) -> str:
    out = ["=" * 78, f"  POST-RENDER QC  ·  {src.name}  ·  {PLATFORM}", "=" * 78]
    m = qc.metrics
    out.append(f"  duration {m.get('duration_s', 0):.1f} s"
               f" · shots {m.get('shot_count', '-')}"
               f" · longest shot {m.get('longest_shot_s', '-')} s"
               f" · freeze tail {m.get('freeze_tail_s', 0):.1f} s"
               f" · LUFS {m.get('lufs_i', '-')}")
    out.append("")
    if not qc.findings:
        out.append("  (no findings)")
    order = {"FAIL": 0, "WARN": 1}
    for f in sorted(qc.findings, key=lambda f: (order.get(f.severity, 2), f.code)):
        out.append(f"  [{f.severity:<4}] {f.code:<14} {f.detail}")
        if f.fix:
            out.append(f"           {'':<14} -> {f.fix}")
    out.append("")
    out.append(f"  FAIL {qc.count('FAIL')}   WARN {qc.count('WARN')}   VERDICT: {qc.verdict}")
    out.append("  Not verified by automation: voice naturalness, lip-sync, music mix,")
    out.append("  name pronunciation, caption sync, banding. Those need human ears and eyes.")
    return "\n".join(out)


def main(argv=None) -> int:
    global PLATFORM, DUR_MIN, DUR_MAX, SWEET_MIN, SWEET_MAX, LUFS_TARGET, LUFS_LO, LUFS_HI
    ap = argparse.ArgumentParser(description="Post-render QC for a kids' Short.")
    ap.add_argument("video", type=Path)
    ap.add_argument("--json-out", type=Path, default=None)
    ap.add_argument("--no-scene", action="store_true", help="skip scene detection")
    ap.add_argument("--platform", default="youtube_shorts", choices=sorted(PLATFORMS),
                    help="platform profile used for the duration window")
    ap.add_argument("--lufs", type=float, default=LUFS_TARGET, help="integrated loudness target")
    args = ap.parse_args(argv)

    if not args.video.exists():
        print(f"error: {args.video} not found", file=sys.stderr)
        return 3
    ffmpeg = find_ffmpeg()
    if not ffmpeg:
        print("error: ffmpeg not found. Install ffmpeg, or `pip install imageio-ffmpeg`.", file=sys.stderr)
        print("QC not run — report this honestly instead of claiming a pass.", file=sys.stderr)
        return 3

    PLATFORM = args.platform
    DUR_MIN, DUR_MAX, SWEET_MIN, SWEET_MAX = map(float, PLATFORMS[args.platform])
    LUFS_TARGET = args.lufs
    LUFS_LO, LUFS_HI = args.lufs - 2.0, args.lufs + 1.0
    qc = analyse(args.video, ffmpeg, do_scene=not args.no_scene)
    print(render(qc, args.video))

    if args.json_out:
        args.json_out.write_text(json.dumps({
            "file": str(args.video),
            "verdict": qc.verdict,
            "counts": {s: qc.count(s) for s in ("FAIL", "WARN")},
            "metrics": qc.metrics,
            "findings": [f.__dict__ for f in qc.findings],
        }, indent=2), encoding="utf-8")
        print(f"\n  wrote {args.json_out}")

    return 0 if qc.count("FAIL") == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
