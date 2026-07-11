# Screenwatch Kit

An AI that watches you work and suggests workflow upgrades. A script screenshots
your screen every 5 seconds (plus what app/window/site you're on), stores it
cheaply, and an AI agent periodically analyzes it and answers: **"how can I
economize my workflow?"**

Real results from a week of use: hotkeys you didn't know you needed, a $30/mo
voice-to-text tool replaced with a free local one (250ms → 50ms latency), a
Chrome extension that automated a 5-min task done 3–4×/day. In aggregate:
~30 min/day back.

> This kit lives in this repo as a self-contained sub-project. The Claude Code
> skill is already installed at **`.claude/skills/screenwatch/`**, so opening a
> Claude Code session on this repo gives you `/screenwatch analyze`,
> `/screenwatch optimize`, and `/screenwatch status` immediately. To run the
> capture daemon on your own machine, follow the setup below (or hand the folder
> to an agent).

## Fastest setup (recommended)

Don't set this up by hand. Give this folder to an AI coding agent (Claude Code,
Cursor, etc.) and let it adapt everything to your machine:

1. Copy the `screenwatch-kit/` folder anywhere on your machine.
2. Open your AI agent in the folder (e.g. `cd screenwatch-kit && claude`).
3. Paste this:

> Read SETUP-AGENT-PROMPT.md in this folder and set up screenwatch on my
> machine. Verify it actually works end-to-end before you finish.

The agent detects your OS, installs the capture daemon, handles permissions, and
verifies a real screenshot + metadata line landed on disk.

## What's in here

- `SETUP-AGENT-PROMPT.md` — full instructions for your AI agent (macOS / Windows
  / Linux), including every gotcha we hit so your agent doesn't have to
  rediscover them.
- `mac/` — battle-tested macOS capture script, launchd config, and the
  permission-wrapper trick (`wrapper.c`).
- `windows/` — PowerShell capture script + Task Scheduler setup.
- `scripts/aggregate.py` — the **log aggregator** the analysis step calls, so no
  agent ever reads the raw 8,640-line log into context. Standard-library Python
  3.9+; run it directly to see what a day looks like. (A byte-identical copy is
  bundled in the skill so `/screenwatch analyze` can call it via
  `${CLAUDE_SKILL_DIR}`.)
- `scripts/dashboard.py` — renders a **self-contained HTML time-tracking
  dashboard** (stat tiles, time-per-app chart, activity timeline or multi-day
  trend, polling-loop callouts, table view). Theme-aware and colorblind-safe;
  standard-library only. Also bundled in the skill for `/screenwatch dashboard`.
- `ANALYSIS-PROMPTS.md` — copy-paste analyze/optimize prompts for any agent.
- `docs/diagrams.html` — hand-drawn system diagrams (open in a browser).

The Claude Code skill itself lives at the repo root under
`.claude/skills/screenwatch/` (that's where Claude Code discovers skills). If you
want it on another machine, copy that folder into `~/.claude/skills/screenwatch/`.

## Try the aggregator right now

```bash
# After you have at least one captured day:
python3 scripts/aggregate.py --date 2026-07-08          # readable report
python3 scripts/aggregate.py --date 2026-07-08 --json   # structured, for an agent
python3 scripts/aggregate.py --day-dir /path/to/days/2026-07-08
```

It prints per-app time, context-switch rate, churn bursts, repeated-revisit
("polling loop") candidates, and the short `frames_to_review` list — the only
frames an agent then needs to actually look at.

For a visual view of where your time goes, render the dashboard:

```bash
python3 scripts/dashboard.py --days 7      # last 7 days → one HTML file
python3 scripts/dashboard.py --date 2026-07-08
# writes ~/screenwatch/dashboards/<label>.html — open it in any browser
```

## How it stays cheap (the important design ideas)

1. **Metadata first, vision second.** Every 5s tick logs a JSON line (app, window
   title, URL) — a full day is ~8,640 lines of nearly-free text. Screenshots are
   only actually *looked at* by the AI for ~10–30 selected moments per day (the
   aggregator picks them).
2. **Small frames.** AI vision downsizes images to ~1568px anyway, so frames are
   stored at exactly that width as ~40KB WebP. Bigger is wasted disk and tokens.
3. **Dedupe + idle skip.** Same app/window/URL as the last tick → image only
   every ~30s. No input for 90s → no capture at all.
4. **Auto-prune.** Images delete after 30 days; the AI's daily notes and the
   running "observations ledger" are tiny and kept forever — they're the real
   asset.
5. **Repetition threshold.** An inefficiency becomes a suggestion only after it's
   been observed 3+ times. That's what makes suggestions land instead of noise.

## Privacy note (read this)

This records everything on your screen — passwords momentarily visible, DMs,
banking. It all stays on your machine in `~/screenwatch/` (or
`%USERPROFILE%\screenwatch\` on Windows), and only the frames your agent reads
during analysis ever leave it. Pause any time (your agent sets up a stop
command). Don't run it during sensitive sessions, and don't upload the raw
folder anywhere.
