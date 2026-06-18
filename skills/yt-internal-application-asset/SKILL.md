---
name: yt-internal-application-asset
description: >-
  Worker 2 of the yt-reference-pipeline. Takes the External Example asset from
  Worker 1 (title, description, transcript) and produces the linked Internal
  Application asset, a navigable Notion page of what to do and not do from the
  content and the form, reusable procedural templates, and a full link and
  landing-page teardown. Use after the External Example asset exists. Usually
  invoked by the yt-reference-pipeline orchestrator.
---

# yt-internal-application-asset

## Purpose

Turn the External Example asset into action. Produce a second Notion page, the
Internal Application asset, that teaches Tanner and the team how to learn from
and apply the source video. It is insightful, action-oriented, ongoing,
layer-by-layer, and self-supplementing as a knowledge base.

## Inputs

- The External Example asset page id and url from Worker 1.
- The same extract payload Worker 1 used, for the links list. If not provided, fetch the External Example page and read its Links found section.

## Output

- A Notion page in the Reference Assets database, Asset Type Internal Application, linked to the External Example asset through the Paired Asset relation.
- The page id, returned to the caller.

## Read first

- skills/shared/formatting_rules.md
- skills/shared/notion_config.md
- skills/yt-internal-application-asset/references/analysis_frames.md

## Procedure

### Step 1, analyze the source

- Read the External Example asset in full, title, description, and transcript.
- Hold two questions in mind throughout: what does the content teach, and what does the form teach.

### Step 2, write sections A, B, C

- Section A, content DO and DO NOT, from the substance of the video.
- Section B, form DO and DO NOT, from the medium, style, and structure.
- Section C, procedural templates, the reusable how-tos listed in the analysis frames.
- Follow the analysis frames reference for the exact section contents.

### Step 3, run the link teardown engine

- Gather every link from the description and every link or resource named in the transcript. The extract payload links field already has these.
- Write them to a JSON file and run:
- `python3 skills/yt-internal-application-asset/scripts/teardown.py --links /tmp/links.json --outdir /tmp/teardown --out /tmp/teardown.json`
- The script runs the free local-first chain: Jina Reader text plus a local Playwright full-page screenshot, with a hosted screenshot API as the Tier 3 fallback.
- Chromium must be installed once: `python3 -m playwright install chromium`.

### Step 4, escalate only interactive funnels

- Tier 2 is the interactive walk through, and only for links that one screenshot cannot capture, for example a multi-step opt-in funnel or a checkout flow.
- For a flagged link, drive the @playwright/mcp server step by step, capturing a screenshot at each step. Do not do this for every link.
- Only ever send public URLs to any hosted service. Never send anything internal or private.

### Step 5, read both text and image for each link

- For each link, read the Jina text for the copy and the screenshot for the visual flow.
- Analyze through all nine lenses in the analysis frames, then write the one-line verdict: implement, do not implement, adapt, or unreachable.
- A link that is unreachable by every tier is marked unreachable. Continue. Never fail the whole run over one dead link.

### Step 6, build the Notion page

- Create the page in the Reference Assets data source.
- Structure: a top callout banner, a `<table_of_contents/>`, then Section A, Section B, Section C, then Section D with one toggle per link.
- Use the same verified Notion syntax as Worker 1: `<table_of_contents/>`, `<callout icon="...">`, and toggle blocks.
- Set properties: Name "INT | <cleaned title>", Asset Type Internal Application, Source URL, Video Title, Stage Analyzed.

### Step 7, link the pair and verify

- Set the Paired Asset relation on the Internal Application page to the External Example page. The relation is two-way, so the External Example page gets the back link automatically.
- Fetch the page back once. Confirm the TOC rendered, the link toggles exist, and the Paired Asset relation is set.
- Set Stage to Complete. Return the page id and url.

## Failure rule

- On any hard failure, stop and report what failed and why. Leave completed pages intact. Never half-delete.
