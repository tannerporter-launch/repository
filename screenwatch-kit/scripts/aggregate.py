#!/usr/bin/env python3
"""Aggregate a day of screenwatch metadata — the "metadata first" step.

The analysis prompts (ANALYSIS-PROMPTS.md) and the `screenwatch` skill both say:
*aggregate `log.jsonl` with a script — don't read the raw 8,640-line file into
context.* This is that script. Point it at a day and it collapses the 5-second
ticks into activity blocks and computes the signals an AI needs to hunt for
repeated friction, plus the short list of frames actually worth looking at
(metadata first, vision second).

Log schema (one JSON object per line, produced by the capture loops):

    {"t": "09-00-05", "epoch": 1778...,, "app": "Chrome",
     "window": "Inbox (5) - Gmail", "url": "mail.google.com", "img": true}

Pure standard library — no third-party deps, Python 3.9+. The analysis functions
are importable and unit-tested; the CLI resolves real frame filenames on disk.

Usage:
    python3 aggregate.py                     # today, ~/screenwatch
    python3 aggregate.py --date 2026-07-08
    python3 aggregate.py --day-dir /path/to/days/2026-07-08 --json
"""

from __future__ import annotations

import argparse
import json
import os
import statistics
from datetime import date
from typing import Dict, List, Optional

DEFAULT_INTERVAL = 5           # seconds between ticks (matches the capture loops)
CHURN_WINDOW_S = 120           # "churn burst" detection window
CHURN_THRESHOLD = 6            # >6 app switches in the window = a burst
REVISIT_MIN = 3               # app/url returned to >= this many separate times
MAX_FRAMES = 30                # cap on frames selected for the AI to actually read


# --------------------------------------------------------------------------
# Loading
# --------------------------------------------------------------------------
def load_log(path: str) -> List[Dict]:
    """Read a ``log.jsonl`` into a list of tick dicts (bad lines skipped)."""
    events: List[Dict] = []
    if not os.path.exists(path):
        return events
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    events.sort(key=lambda e: e.get("epoch", 0))
    return events


def infer_interval(events: List[Dict], default: int = DEFAULT_INTERVAL) -> int:
    """Median gap between consecutive ticks — robust to idle-skip gaps."""
    epochs = [e.get("epoch") for e in events if isinstance(e.get("epoch"), (int, float))]
    gaps = [b - a for a, b in zip(epochs, epochs[1:]) if 0 < (b - a) <= 30]
    if not gaps:
        return default
    return max(1, int(round(statistics.median(gaps))))


# --------------------------------------------------------------------------
# Activity blocks
# --------------------------------------------------------------------------
def _key(e: Dict) -> tuple:
    return (e.get("app") or "unknown", e.get("window") or "", e.get("url") or "")


def build_blocks(events: List[Dict], interval: int = DEFAULT_INTERVAL) -> List[Dict]:
    """Collapse consecutive same app+window+url ticks into activity blocks.

    Each block records its span, duration (last-first epoch + one interval, so a
    single-tick block counts as ``interval`` seconds), and the timestamps of any
    ticks that saved a screenshot (``img_ts`` — the candidate frames to look at).
    """
    blocks: List[Dict] = []
    for e in events:
        k = _key(e)
        img = bool(e.get("img"))
        t = e.get("t")
        ep = e.get("epoch", 0)
        if blocks and blocks[-1]["_key"] == k:
            b = blocks[-1]
            b["end_t"] = t
            b["end_epoch"] = ep
            b["ticks"] += 1
            if img and t:
                b["img_ts"].append(t)
        else:
            blocks.append(
                {
                    "_key": k,
                    "app": k[0],
                    "window": k[1],
                    "url": k[2],
                    "start_t": t,
                    "end_t": t,
                    "start_epoch": ep,
                    "end_epoch": ep,
                    "ticks": 1,
                    "img_ts": [t] if (img and t) else [],
                }
            )
    for b in blocks:
        b["duration_s"] = (b["end_epoch"] - b["start_epoch"]) + interval
        del b["_key"]
    return blocks


# --------------------------------------------------------------------------
# Signals
# --------------------------------------------------------------------------
def per_app_seconds(blocks: List[Dict]) -> Dict[str, int]:
    out: Dict[str, int] = {}
    for b in blocks:
        out[b["app"]] = out.get(b["app"], 0) + b["duration_s"]
    return dict(sorted(out.items(), key=lambda kv: kv[1], reverse=True))


def context_switches(blocks: List[Dict]) -> int:
    """App changes between consecutive blocks (window-only changes don't count)."""
    switches = 0
    prev = None
    for b in blocks:
        if prev is not None and b["app"] != prev:
            switches += 1
        prev = b["app"]
    return switches


def churn_bursts(
    events: List[Dict],
    window_s: int = CHURN_WINDOW_S,
    threshold: int = CHURN_THRESHOLD,
) -> List[Dict]:
    """Find windows with more than ``threshold`` app switches — thrash bursts.

    Returns merged ``{start_epoch, end_epoch, switches}`` intervals. These are
    prime "you're bouncing between apps" evidence and drive frame selection.
    """
    # Epochs at which the app changed.
    changes: List[int] = []
    prev = None
    for e in events:
        app = e.get("app") or "unknown"
        if prev is not None and app != prev:
            changes.append(e.get("epoch", 0))
        prev = app

    bursts: List[Dict] = []
    for i, start in enumerate(changes):
        count = sum(1 for c in changes[i:] if c - start <= window_s)
        if count > threshold:
            end = start + window_s
            if bursts and start <= bursts[-1]["end_epoch"]:
                bursts[-1]["end_epoch"] = max(bursts[-1]["end_epoch"], end)
                bursts[-1]["switches"] = max(bursts[-1]["switches"], count)
            else:
                bursts.append(
                    {"start_epoch": start, "end_epoch": end, "switches": count}
                )
    return bursts


def revisits(blocks: List[Dict]) -> Dict[str, Dict[str, int]]:
    """Count how many *separate* blocks each app / url appears in.

    A high count means the surface was returned to repeatedly — the manual
    status-polling loop the brief wants to replace with a digest. (A single long
    focused session counts once; four separate checks count four.)
    """
    apps: Dict[str, int] = {}
    urls: Dict[str, int] = {}
    for b in blocks:
        apps[b["app"]] = apps.get(b["app"], 0) + 1
        if b["url"]:
            urls[b["url"]] = urls.get(b["url"], 0) + 1
    apps = {k: v for k, v in apps.items() if v >= REVISIT_MIN}
    urls = {k: v for k, v in urls.items() if v >= REVISIT_MIN}
    return {
        "apps": dict(sorted(apps.items(), key=lambda kv: kv[1], reverse=True)),
        "urls": dict(sorted(urls.items(), key=lambda kv: kv[1], reverse=True)),
    }


def _top(blocks: List[Dict], field: str, n: int = 5) -> List[Dict]:
    agg: Dict[str, int] = {}
    for b in blocks:
        v = b.get(field)
        if v:
            agg[v] = agg.get(v, 0) + b["duration_s"]
    ranked = sorted(agg.items(), key=lambda kv: kv[1], reverse=True)[:n]
    return [{field: k, "seconds": s} for k, s in ranked]


def select_frames(
    blocks: List[Dict],
    bursts: List[Dict],
    max_frames: int = MAX_FRAMES,
) -> List[Dict]:
    """Choose the ≤``max_frames`` timestamps worth actually looking at.

    Priority: (1) the frame at each block transition, (2) frames inside churn
    bursts, (3) frames from the longest blocks. Returns ``{t, reason}`` in
    chronological order, deduped. The CLI turns each ``t`` into a real filename.
    """
    picked: Dict[str, str] = {}  # t -> reason (first reason wins)

    def add(t: Optional[str], reason: str) -> None:
        if t and t not in picked:
            picked[t] = reason

    # 1) Transitions — the first captured frame of each block.
    for b in blocks:
        if b["img_ts"]:
            add(b["img_ts"][0], "transition")

    # 2) Churn bursts — any captured frame whose block overlaps a burst.
    for b in blocks:
        for burst in bursts:
            if b["start_epoch"] <= burst["end_epoch"] and b["end_epoch"] >= burst["start_epoch"]:
                for t in b["img_ts"]:
                    add(t, "churn")
                break

    # 3) Longest blocks — a mid frame from each.
    for b in sorted(blocks, key=lambda x: x["duration_s"], reverse=True):
        if b["img_ts"]:
            add(b["img_ts"][len(b["img_ts"]) // 2], "long-block")

    ordered = sorted(picked.items(), key=lambda kv: kv[0])  # HH-MM-SS sorts fine
    return [{"t": t, "reason": r} for t, r in ordered[:max_frames]]


# --------------------------------------------------------------------------
# Top-level aggregation
# --------------------------------------------------------------------------
def aggregate(events: List[Dict], interval: Optional[int] = None) -> Dict:
    """Run the full pipeline over one day's events."""
    if interval is None:
        interval = infer_interval(events)
    blocks = build_blocks(events, interval)
    bursts = churn_bursts(events)
    switches = context_switches(blocks)
    tracked = sum(b["duration_s"] for b in blocks)
    hours = tracked / 3600 if tracked else 0

    return {
        "interval_s": interval,
        "ticks": len(events),
        "blocks": len(blocks),
        "tracked_seconds": tracked,
        "frames_captured": sum(1 for e in events if e.get("img")),
        "context_switches": switches,
        "switches_per_hour": round(switches / hours, 1) if hours else 0,
        "per_app_seconds": per_app_seconds(blocks),
        "top_windows": _top(blocks, "window"),
        "top_urls": _top(blocks, "url"),
        "revisits": revisits(blocks),
        "churn_bursts": bursts,
        "frames_to_review": select_frames(blocks, bursts),
        "activity_blocks": [
            {
                "start_t": b["start_t"],
                "end_t": b["end_t"],
                "duration_s": b["duration_s"],
                "app": b["app"],
                "window": b["window"],
                "url": b["url"],
            }
            for b in blocks
        ],
    }


def format_report(agg: Dict, date_label: Optional[str] = None) -> str:
    """Human-readable summary — the quick read before the JSON detail."""
    lines = []
    hdr = "Screenwatch aggregate" + (f" — {date_label}" if date_label else "")
    lines.append(hdr)
    lines.append("=" * len(hdr))
    tracked_min = agg["tracked_seconds"] // 60
    lines.append(
        f"{agg['ticks']} ticks / {agg['blocks']} activity blocks / "
        f"~{tracked_min} min tracked (interval {agg['interval_s']}s)."
    )
    lines.append(
        f"Context switches: {agg['context_switches']} "
        f"({agg['switches_per_hour']}/hour). "
        f"Frames captured: {agg['frames_captured']}, "
        f"selected for review: {len(agg['frames_to_review'])}."
    )
    if agg["per_app_seconds"]:
        lines.append("\nTime per app:")
        for app, s in list(agg["per_app_seconds"].items())[:8]:
            lines.append(f"  {s // 60:>4}m  {app}")
    rv = agg["revisits"]
    if rv["urls"] or rv["apps"]:
        lines.append("\nPolling / revisit candidates (returned to >= "
                     f"{REVISIT_MIN}x):")
        for u, c in rv["urls"].items():
            lines.append(f"  {c:>3}x  {u}")
        for a, c in rv["apps"].items():
            lines.append(f"  {c:>3}x  {a} (app)")
    if agg["churn_bursts"]:
        lines.append(f"\nChurn bursts (>{CHURN_THRESHOLD} switches / "
                     f"{CHURN_WINDOW_S}s): {len(agg['churn_bursts'])}")
    if agg["frames_to_review"]:
        lines.append("\nFrames to look at (metadata first, vision second):")
        for f in agg["frames_to_review"]:
            lines.append(f"  {f['t']}  [{f['reason']}]")
    return "\n".join(lines)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def _default_base() -> str:
    return os.environ.get("SCREENWATCH_HOME") or os.path.join(
        os.path.expanduser("~"), "screenwatch"
    )


def _resolve_frame_files(day_dir: str, frames: List[Dict]) -> List[Dict]:
    """Turn selected ``t`` timestamps into real filenames on disk (.webp/.jpg)."""
    out = []
    for f in frames:
        fname = None
        for ext in (".webp", ".jpg", ".jpeg", ".png"):
            cand = f["t"] + ext
            if os.path.exists(os.path.join(day_dir, cand)):
                fname = cand
                break
        out.append({**f, "file": fname or (f["t"] + ".webp")})
    return out


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Aggregate a day of screenwatch metadata.")
    p.add_argument("--date", help="YYYY-MM-DD (default: today)")
    p.add_argument("--base", default=_default_base(),
                   help="screenwatch home (default: ~/screenwatch)")
    p.add_argument("--day-dir", help="explicit day folder (overrides --base/--date)")
    p.add_argument("--json", action="store_true", help="emit JSON instead of a report")
    p.add_argument("--interval", type=int, help="override tick interval seconds")
    args = p.parse_args(argv)

    day = args.date or date.today().isoformat()
    day_dir = args.day_dir or os.path.join(args.base, "days", day)
    day_label = args.date or os.path.basename(os.path.normpath(day_dir))
    log_path = os.path.join(day_dir, "log.jsonl")

    events = load_log(log_path)
    if not events:
        print(f"No metadata at {log_path}. Is the capture daemon running?")
        return 1

    agg = aggregate(events, interval=args.interval)
    agg["frames_to_review"] = _resolve_frame_files(day_dir, agg["frames_to_review"])

    if args.json:
        print(json.dumps(agg, indent=2))
    else:
        print(format_report(agg, day_label))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
