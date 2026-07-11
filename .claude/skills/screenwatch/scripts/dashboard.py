#!/usr/bin/env python3
"""Render a self-contained time-tracking dashboard from screenwatch data.

The capture loop already logs how you spend every 5 seconds; `aggregate.py`
already turns a day into per-app time, activity blocks, context-switch rate, and
polling-loop candidates. This script is the *view* on top of that — it renders
one day, or a range of days, into a single standalone HTML file you open in a
browser. No server, no dependencies, no data leaves your machine.

    python3 dashboard.py                      # today
    python3 dashboard.py --days 7             # last 7 days (a real "where did my
                                              #   time go" view)
    python3 dashboard.py --date 2026-07-08 --out ~/Desktop/mon.html

Design follows the data-viz method: a validated, colorblind-safe categorical
palette (fixed hue order, never cycled), text in ink tokens rather than series
colors, direct labels + a table view so identity is never color-alone, and a
light/dark theme selected from the same ramps. Charts are plain HTML/CSS so the
file is dependency-free and prints cleanly.

The rendering functions are pure and unit-tested; the CLI reads days off disk and
reuses `aggregate.py` for all the number-crunching.
"""

from __future__ import annotations

import argparse
import html
import importlib.util
import os
import pathlib
from datetime import date, timedelta
from typing import Dict, List, Optional, Tuple

# Import the sibling aggregator (works whether run as a script or imported).
_AGG_PATH = pathlib.Path(__file__).resolve().parent / "aggregate.py"
_spec = importlib.util.spec_from_file_location("swk_aggregate", _AGG_PATH)
aggregate = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(aggregate)

# --- Validated categorical palette (dataviz reference instance) -----------
# Fixed slot order IS the colorblind-safety mechanism — assign in order, never
# cycle. A 9th app folds into "Other" (muted grey), never a generated hue.
SERIES_LIGHT = [
    "#2a78d6", "#1baf7a", "#eda100", "#008300",
    "#4a3aa7", "#e34948", "#e87ba4", "#eb6834",
]
SERIES_DARK = [
    "#3987e5", "#199e70", "#c98500", "#008300",
    "#9085e9", "#e66767", "#d55181", "#d95926",
]
OTHER_LIGHT = "#898781"
OTHER_DARK = "#898781"
MAX_SERIES = 8


def _fmt_dur(seconds: int) -> str:
    """Human duration: 4500 -> '1h 15m', 45 -> '45s', 300 -> '5m'."""
    seconds = int(seconds)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}h {m}m" if m else f"{h}h"
    if m:
        return f"{m}m"
    return f"{s}s"


def assign_app_colors(app_seconds: Dict[str, int]) -> List[Dict]:
    """Rank apps by time and assign fixed palette slots; overflow -> 'Other'.

    Returns a list of {app, seconds, slot} where slot is the palette index or
    -1 for the merged 'Other' bucket. Color follows the *entity* (rank here, but
    stable given the same input), never a repainted survivor set.
    """
    ranked = sorted(app_seconds.items(), key=lambda kv: kv[1], reverse=True)
    out: List[Dict] = []
    other = 0
    for i, (app, secs) in enumerate(ranked):
        if i < MAX_SERIES:
            out.append({"app": app, "seconds": secs, "slot": i})
        else:
            other += secs
    if other:
        out.append({"app": "Other", "seconds": other, "slot": -1})
    return out


def build_view(days: List[Tuple[str, Dict]]) -> Dict:
    """Assemble everything the renderer needs from one or more day aggregates.

    ``days`` is a list of ``(date_label, aggregate_output)`` in chronological
    order. One day -> a timeline + blocks view; many -> a per-day trend + totals.
    """
    # Merge per-app time across the whole window.
    totals: Dict[str, int] = {}
    tracked = 0
    idle = 0
    switches = 0
    for _, agg in days:
        for app, secs in agg.get("per_app_seconds", {}).items():
            totals[app] = totals.get(app, 0) + secs
        tracked += agg.get("tracked_seconds", 0)
        idle += agg.get("idle_seconds", 0)
        switches += agg.get("context_switches", 0)

    apps = assign_app_colors(totals)
    active = max(0, tracked - idle)
    hours = tracked / 3600 if tracked else 0
    n_days = len(days)

    tiles = [
        {"label": "Time tracked", "value": _fmt_dur(tracked),
         "sub": f"across {n_days} day{'s' if n_days != 1 else ''}"},
        {"label": "Active", "value": _fmt_dur(active),
         "sub": f"{_fmt_dur(idle)} idle"},
        {"label": "Context switches",
         "value": f"{round(switches / hours, 1) if hours else 0}/hr",
         "sub": f"{switches} total"},
        {"label": "Apps used", "value": str(len([a for a in apps if a['app'] != 'Other'])),
         "sub": "distinct"},
    ]

    view: Dict = {
        "n_days": n_days,
        "tiles": tiles,
        "apps": apps,
        "tracked": tracked,
    }

    # Single day: proportional activity timeline + polling/churn callouts.
    if n_days == 1:
        label, agg = days[0]
        view["title"] = "Screen-time dashboard"
        view["subtitle"] = label
        slot_of = {a["app"]: a["slot"] for a in apps}
        view["timeline"] = [
            {
                "app": b["app"],
                "duration_s": b["duration_s"],
                "slot": slot_of.get(b["app"], -1),
                "label": f"{b['app']} · {_fmt_dur(b['duration_s'])}"
                         + (f" · {b['window']}" if b.get("window") else ""),
            }
            for b in agg.get("activity_blocks", [])
        ]
        rv = agg.get("revisits", {})
        callouts = []
        for u, c in rv.get("urls", {}).items():
            callouts.append({"label": u, "count": c, "kind": "site"})
        for a, c in rv.get("apps", {}).items():
            callouts.append({"label": a, "count": c, "kind": "app"})
        view["revisits"] = callouts
        view["churn_bursts"] = len(agg.get("churn_bursts", []))
    else:
        view["title"] = "Screen-time dashboard"
        view["subtitle"] = f"{days[0][0]} → {days[-1][0]}"
        view["trend"] = [
            {"label": lbl, "seconds": agg.get("tracked_seconds", 0)}
            for lbl, agg in days
        ]

    return view


# --------------------------------------------------------------------------
# Rendering (pure string building — no I/O)
# --------------------------------------------------------------------------
_CSS = """
:root{
  --plane:#f9f9f7; --surface:#fcfcfb; --ink:#0b0b0b; --ink2:#52514e;
  --muted:#898781; --grid:#e1e0d9; --baseline:#c3c2b7;
  --border:rgba(11,11,11,0.10); --other:#898781;
}
@media (prefers-color-scheme:dark){
  :root{
    --plane:#0d0d0d; --surface:#1a1a19; --ink:#fff; --ink2:#c3c2b7;
    --muted:#898781; --grid:#2c2c2a; --baseline:#383835;
    --border:rgba(255,255,255,0.10); --other:#898781;
  }
}
*{box-sizing:border-box}
body{margin:0;background:var(--plane);color:var(--ink);
  font-family:system-ui,-apple-system,"Segoe UI",sans-serif;
  padding:2rem 1.25rem 4rem;line-height:1.45}
.wrap{max-width:960px;margin:0 auto;display:flex;flex-direction:column;gap:1.75rem}
header h1{font-size:1.5rem;margin:0 0 .2rem}
header p{margin:0;color:var(--ink2)}
.card{background:var(--surface);border:1px solid var(--border);border-radius:12px;
  padding:1.1rem 1.25rem;box-shadow:0 1px 3px rgba(0,0,0,.05)}
.card h2{font-size:.8rem;text-transform:uppercase;letter-spacing:.04em;
  color:var(--muted);margin:0 0 .9rem}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:1rem}
.tile .v{font-size:1.9rem;font-weight:650;letter-spacing:-.01em}
.tile .l{color:var(--ink2);font-size:.85rem}
.tile .s{color:var(--muted);font-size:.78rem;margin-top:.15rem}
.bar-row{display:grid;grid-template-columns:130px 1fr auto;align-items:center;
  gap:.6rem;margin:.35rem 0}
.bar-row .name{color:var(--ink2);font-size:.85rem;white-space:nowrap;
  overflow:hidden;text-overflow:ellipsis}
.bar-track{background:var(--grid);border-radius:5px;height:16px;overflow:hidden}
.bar-fill{height:100%;border-radius:5px}
.bar-row .val{font-size:.82rem;color:var(--ink2);
  font-variant-numeric:tabular-nums}
.timeline{display:flex;height:26px;border-radius:6px;overflow:hidden;
  border:1px solid var(--border);background:var(--grid)}
.seg{min-width:2px;border-right:2px solid var(--surface)}
.timeline-scale{display:flex;justify-content:space-between;color:var(--muted);
  font-size:.72rem;margin-top:.35rem}
.callouts{display:flex;flex-direction:column;gap:.45rem}
.callout{display:flex;align-items:center;gap:.6rem}
.badge{background:var(--grid);color:var(--ink);border-radius:999px;
  padding:.05rem .5rem;font-size:.78rem;font-variant-numeric:tabular-nums;
  white-space:nowrap}
.callout .lbl{color:var(--ink2);font-size:.88rem}
table{border-collapse:collapse;width:100%;font-size:.85rem}
th,td{text-align:left;padding:.35rem .5rem;border-bottom:1px solid var(--grid)}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums}
.swatch{display:inline-block;width:10px;height:10px;border-radius:2px;
  margin-right:.5rem;vertical-align:middle}
.scroll{overflow-x:auto}
.foot{color:var(--muted);font-size:.78rem}
"""


def _color_css(slot: int) -> str:
    """CSS that resolves a palette slot to its light/dark hex via inline vars."""
    if slot < 0:
        return "background:var(--other)"
    return f"background:var(--s{slot})"


def _series_vars() -> str:
    lines = []
    for i, hexv in enumerate(SERIES_LIGHT):
        lines.append(f"--s{i}:{hexv};")
    dark = "".join(f"--s{i}:{h};" for i, h in enumerate(SERIES_DARK))
    return (
        ":root{" + "".join(lines) + "}"
        + "@media (prefers-color-scheme:dark){:root{" + dark + "}}"
    )


def _esc(s: str) -> str:
    return html.escape(str(s), quote=True)


def render_dashboard(view: Dict) -> str:
    """Render the assembled view into a complete standalone HTML document."""
    apps = view["apps"]
    total = view["tracked"] or 1
    max_secs = max((a["seconds"] for a in apps), default=1) or 1

    # Time-per-app horizontal bars (magnitude → length; identity → color).
    bar_rows = []
    for a in apps:
        pct = a["seconds"] / total * 100
        width = a["seconds"] / max_secs * 100
        bar_rows.append(
            f'<div class="bar-row">'
            f'<span class="name" title="{_esc(a["app"])}">'
            f'<span class="swatch" style="{_color_css(a["slot"])}"></span>'
            f'{_esc(a["app"])}</span>'
            f'<div class="bar-track"><div class="bar-fill" '
            f'style="width:{width:.1f}%;{_color_css(a["slot"])}" '
            f'title="{_esc(a["app"])}: {_fmt_dur(a["seconds"])} ({pct:.0f}%)">'
            f'</div></div>'
            f'<span class="val">{_fmt_dur(a["seconds"])} · {pct:.0f}%</span>'
            f'</div>'
        )

    # Accessibility: a table view so identity is never color-alone.
    table_rows = "".join(
        f'<tr><td><span class="swatch" style="{_color_css(a["slot"])}"></span>'
        f'{_esc(a["app"])}</td>'
        f'<td class="num">{_fmt_dur(a["seconds"])}</td>'
        f'<td class="num">{a["seconds"] / total * 100:.0f}%</td></tr>'
        for a in apps
    )

    sections = []

    # Stat tiles.
    tiles = "".join(
        f'<div class="tile"><div class="v">{_esc(t["value"])}</div>'
        f'<div class="l">{_esc(t["label"])}</div>'
        f'<div class="s">{_esc(t["sub"])}</div></div>'
        for t in view["tiles"]
    )
    sections.append(f'<section class="card"><div class="tiles">{tiles}</div></section>')

    # Time per app.
    sections.append(
        '<section class="card"><h2>Time per app</h2>'
        + "".join(bar_rows) + "</section>"
    )

    # Single-day timeline.
    if "timeline" in view and view["timeline"]:
        tl_total = sum(b["duration_s"] for b in view["timeline"]) or 1
        segs = "".join(
            f'<div class="seg" style="flex-grow:{b["duration_s"]};'
            f'{_color_css(b["slot"])}" title="{_esc(b["label"])}"></div>'
            for b in view["timeline"]
        )
        sections.append(
            '<section class="card"><h2>Activity timeline (proportional)</h2>'
            f'<div class="timeline">{segs}</div>'
            '<div class="timeline-scale"><span>start of tracked time</span>'
            f'<span>{_fmt_dur(tl_total)} total</span></div></section>'
        )

    # Multi-day trend (one bar per day, single hue — magnitude over time).
    if "trend" in view and view["trend"]:
        tmax = max((d["seconds"] for d in view["trend"]), default=1) or 1
        rows = "".join(
            f'<div class="bar-row">'
            f'<span class="name">{_esc(d["label"])}</span>'
            f'<div class="bar-track"><div class="bar-fill" '
            f'style="width:{d["seconds"] / tmax * 100:.1f}%;background:var(--s0)" '
            f'title="{_esc(d["label"])}: {_fmt_dur(d["seconds"])}"></div></div>'
            f'<span class="val">{_fmt_dur(d["seconds"])}</span></div>'
            for d in view["trend"]
        )
        sections.append(
            '<section class="card"><h2>Tracked time per day</h2>' + rows + "</section>"
        )

    # Polling loops + churn (the "repeated friction" signal).
    if view.get("revisits"):
        callouts = "".join(
            f'<div class="callout"><span class="badge">{c["count"]}×</span>'
            f'<span class="lbl">Returned to {_esc(c["label"])}'
            f'{" (app)" if c["kind"] == "app" else ""}</span></div>'
            for c in view["revisits"]
        )
        churn = view.get("churn_bursts", 0)
        churn_line = (
            f'<div class="callout"><span class="badge">{churn}</span>'
            f'<span class="lbl">churn burst{"s" if churn != 1 else ""} '
            f'(rapid app-switching windows)</span></div>'
            if churn else ""
        )
        sections.append(
            '<section class="card"><h2>Repeated friction (polling loops)</h2>'
            '<div class="callouts">' + callouts + churn_line + "</div>"
            '<p class="foot">Surfaces you return to many separate times are prime '
            'targets for a digest, hotkey, or automation.</p></section>'
        )

    # Table view (accessibility).
    sections.append(
        '<section class="card"><h2>All apps (table view)</h2>'
        '<div class="scroll"><table><thead><tr><th>App</th>'
        '<th class="num">Time</th><th class="num">Share</th></tr></thead>'
        f'<tbody>{table_rows}</tbody></table></div></section>'
    )

    body = (
        '<div class="wrap">'
        f'<header><h1>{_esc(view["title"])}</h1>'
        f'<p>{_esc(view["subtitle"])}</p></header>'
        + "".join(sections)
        + '<p class="foot">Generated locally from ~/screenwatch metadata. '
        'No screenshots included; nothing left your machine.</p>'
        '</div>'
    )

    return (
        "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
        f"<title>{_esc(view['title'])} — {_esc(view['subtitle'])}</title>"
        f"<style>{_series_vars()}{_CSS}</style></head>"
        f"<body>{body}</body></html>"
    )


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def _load_day(base: str, day: str) -> Optional[Dict]:
    day_dir = os.path.join(base, "days", day)
    log = os.path.join(day_dir, "log.jsonl")
    events = aggregate.load_log(log)
    if not events:
        return None
    return aggregate.aggregate(events)


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Render a screenwatch time dashboard.")
    p.add_argument("--date", help="single day YYYY-MM-DD (default: today)")
    p.add_argument("--days", type=int, help="render the last N days as a range")
    p.add_argument("--base", default=aggregate._default_base(),
                   help="screenwatch home (default: ~/screenwatch)")
    p.add_argument("--out", help="output HTML path (default: <base>/dashboards/<label>.html)")
    args = p.parse_args(argv)

    labels: List[str]
    if args.days:
        today = date.today()
        labels = [(today - timedelta(days=i)).isoformat()
                  for i in range(args.days - 1, -1, -1)]
    else:
        labels = [args.date or date.today().isoformat()]

    days: List[Tuple[str, Dict]] = []
    for lbl in labels:
        agg = _load_day(args.base, lbl)
        if agg is not None:
            days.append((lbl, agg))

    if not days:
        where = f"last {args.days} days" if args.days else labels[0]
        print(f"No screenwatch metadata found for {where} under {args.base}. "
              "Is the capture daemon running?")
        return 1

    view = build_view(days)
    doc = render_dashboard(view)

    if args.out:
        out = os.path.expanduser(args.out)
    else:
        label = f"{days[0][0]}_to_{days[-1][0]}" if len(days) > 1 else days[0][0]
        out = os.path.join(args.base, "dashboards", f"{label}.html")
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(doc)
    print(f"Dashboard written to {out}")
    print(f"Open it in a browser:  file://{os.path.abspath(out)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
