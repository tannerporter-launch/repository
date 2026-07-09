---
name: screenwatch
description: Analyze the screenwatch capture archive — build daily activity notes, track recurring workflow inefficiencies, and suggest optimizations. Use for "/screenwatch analyze [date]", "/screenwatch optimize [focus]", "/screenwatch status", or any question about what the user was doing on a past day / how to improve their workflow based on observed behavior.
---

# Screenwatch analysis

## Data layout
- `~/screenwatch/days/YYYY-MM-DD/log.jsonl` — one line per 5s tick: `{t, epoch, app, window, url, img}`. `img: true` means a screenshot `HH-MM-SS.webp` (or `.jpg`) exists in the same folder.
- `~/screenwatch/days/YYYY-MM-DD/*.webp|*.jpg` — ~1568px-wide screenshots (pruned after 30 days).
- `~/screenwatch/notes/YYYY-MM-DD.md` — analysis output (kept forever; the durable record).
- `~/screenwatch/observations.md` — rolling ledger of recurring inefficiencies with occurrence counts.

(On Windows the base is `%USERPROFILE%\screenwatch\` and `url` is usually empty — window titles carry the page title instead.)

## Cost discipline (important)
Metadata first, vision second. The JSONL log answers most questions (what apps, how long, how often switching, which URLs) for near-zero tokens. Only Read screenshots where metadata can't tell the story — and read them individually. Target 10–30 images per analyzed day, never all of them. Aggregate the log with a script via the shell, not by reading raw JSONL into context — a ready-made aggregator ships with this skill.

## `analyze [date]` (default: yesterday if it has data, else today)
1. **Aggregate the log** with the bundled script — do NOT read `log.jsonl` into context:
   ```bash
   python3 "${CLAUDE_SKILL_DIR}/scripts/aggregate.py" --date YYYY-MM-DD --json
   ```
   It collapses ticks into activity blocks and returns per-app time, block durations, context-switch rate per hour, top URLs/windows, "churn bursts" (>6 app switches in 2 minutes), repeated-revisit ("polling loop") candidates, and a `frames_to_review` list — the ≤30 frames actually worth looking at, already resolved to real filenames. (Use `--day-dir PATH` for a non-default location; drop `--json` for a readable summary. The script is standard-library only.)
2. **Pick frames to actually look at**: read the screenshots in `frames_to_review` (block transitions, longest blocks, and churn bursts). Never read all frames.
3. **Look specifically for inefficiency evidence**: open menus/right-click menus (mouse used where a hotkey exists), manual file-dialog navigation, repeated copy-paste between the same two apps, hand-scrolling long documents for search, dated/suboptimal tooling, undismissed notification piles, re-doing something automatable, manual status-polling loops.
4. **Write `~/screenwatch/notes/YYYY-MM-DD.md`**: a short timeline (activity blocks with times), what was worked on, tool inventory, and an "Inefficiencies observed" list with concrete evidence (frame filenames). Also note *positive* patterns worth keeping.
5. **Update `~/screenwatch/observations.md`**: for each inefficiency, if a matching entry exists increment its count and update `last:`; otherwise add one. Format:
   `- [count: 3, last: 2026-07-08] Opens X via Spotlight → browser → typing URL; a pinned tab or launcher hotkey would be ~5s faster each time. (Seen: 2026-07-06/14-22-10.webp, ...)`

## `optimize [focus]`
1. Read `observations.md` and the last ~7 days of notes.
2. Entries with count ≥ 3 are confirmed patterns — turn each into a specific recommendation: the exact hotkey, the replacement tool (verify it's current via web search if unsure), or an automation you can build on the spot (shell script, launcher script command, browser extension, scheduled agent).
3. Rank by estimated time saved per week. Present the top 3–5; offer to implement the automatable ones.
4. If `focus` is given (e.g. "browser", "email"), filter to that area.

## `status`
Report whether the capture daemon is running, today's frame count and disk usage, and any recent errors in `~/screenwatch/daemon.log`.
