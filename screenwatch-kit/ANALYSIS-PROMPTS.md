# Analysis prompts (for any AI agent with file + image access)

If you use Claude Code, use the bundled `screenwatch` skill instead and just type `/screenwatch analyze`. Otherwise, paste these.

Either way, Step 1 is scripted for you: `scripts/aggregate.py` does the aggregation so no agent ever reads the raw 8,640-line log into context. Run it directly to see what it produces:

```bash
python3 scripts/aggregate.py --date 2026-07-08        # readable report
python3 scripts/aggregate.py --date 2026-07-08 --json # structured, for an agent
```

It's standard-library Python 3.9+ — nothing to install.

## Daily analysis

> Analyze my screenwatch data for [DATE] in `~/screenwatch/days/[DATE]/`.
>
> Step 1 — Aggregate `log.jsonl` with a script (don't read the raw file into context). Run `python3 scripts/aggregate.py --date [DATE] --json` — it collapses the 5-second ticks into activity blocks (consecutive same app+window+url) and computes per-app time, block durations, app-switch rate, top windows/URLs, churn bursts (>6 app switches in 2 minutes), repeated-revisit ("polling loop") candidates, and a `frames_to_review` list of the ≤30 frames worth looking at.
>
> Step 2 — Look at only the screenshots in the aggregator's `frames_to_review` list (block transitions, longest blocks, churn bursts — already resolved to real filenames). Never read all frames — metadata first, vision second.
>
> Step 3 — Hunt for inefficiency evidence in those frames: menus opened by mouse where a hotkey exists, manual navigation, repeated copy-paste between the same apps, manual status-polling loops (checking dashboards/notifications by hand), outdated or overpriced tools, anything repetitive enough to automate.
>
> Step 4 — Write `~/screenwatch/notes/[DATE].md` with a timeline, what I worked on, and an "Inefficiencies observed" list citing frame filenames. Then update `~/screenwatch/observations.md`: one line per recurring inefficiency in the form `- [count: N, last: DATE] description (Seen: frames...)` — increment the count if the entry already exists.

## Optimization pass (run weekly, or whenever)

> Read `~/screenwatch/observations.md` and my last 7 days of notes in `~/screenwatch/notes/`. Every entry with count ≥ 3 is a confirmed pattern. For each: give me the specific fix — the exact hotkey, a better/cheaper/faster replacement tool (search the web to check it's current), or an automation you can build for me right now. Rank by estimated time saved per week, show the top 5, and offer to implement the buildable ones.

## Tips

- Run the daily analysis on a schedule if your agent supports it (cron, scheduled agents, or a `/loop`) so the ledger builds itself.
- The suggestions get dramatically better after ~3–5 days of data — repetition is the signal.
- Periodically ask the meta-question: "based on everything in observations.md, what should the capture script record that it currently doesn't?"
