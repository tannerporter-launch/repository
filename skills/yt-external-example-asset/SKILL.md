---
name: yt-external-example-asset
description: >-
  Worker 1 of the yt-reference-pipeline. Takes a single YouTube URL, extracts
  the full transcript plus the title and full description, fixes typos and
  transcription errors using the reused youtube-transcript-formatter prompt, and
  writes a clean, navigable External Example asset page to the Notion Reference
  Assets database. Use when you have a YouTube link and need the clean source of
  record. Usually invoked by the yt-reference-pipeline orchestrator, but can run
  standalone.
---

# yt-external-example-asset

## Purpose

Turn one YouTube URL into the External Example asset: a single Notion page that
holds the fixed Title, the fixed full Description, and the fixed full
Transcript, structured so a human or an AI agent can jump to any part.

This skill does extraction and faithful cleanup only. It does not analyze or
give recommendations. That is Worker 2's job.

## Inputs

- A single YouTube URL. That is the only required input.
- Optional: an existing External Example page id to update instead of create.

## Output

- A Notion page in the Reference Assets database, Asset Type External Example.
- The page id, returned to the caller so Worker 2 can consume it.

## Read first

- skills/shared/formatting_rules.md
- skills/shared/notion_config.md
- skills/yt-external-example-asset/references/page_structure.md
- skills/yt-external-example-asset/scripts/clean_prompt.md

## Procedure

### Step 1, yt-dlp extraction

- Run the extractor:
- `python3 skills/yt-external-example-asset/scripts/extract.py "<URL>" --out /tmp/yt_payload.json`
- The script uses yt-dlp as the primary method and youtube-transcript-api as the transcript fallback. It never downloads media, so ffmpeg is not needed.
- The script trusts the system CA bundle, so it works behind a TLS-inspecting proxy.
- Read /tmp/yt_payload.json. It contains title, description, uploader, upload_date, duration, chapters, links, transcript_segments, and transcript_text.

### Step 2, handle extraction failure

- Exit code 2 means no metadata at all, usually a blocked IP or a private or removed video. Stop and report the exact stderr line to the caller. Do not write a partial page.
- Exit code 3 means metadata is fine but no transcript was found. Continue, but mark the transcript section as unavailable and set a callout saying so. If the caller can supply a pasted transcript, rerun with `--transcript-file`.
- Exit code 0 means full success.

### Step 3, clean with the reused prompt

- Load the cleaning prompt from scripts/clean_prompt.md. If Notion is reachable, prefer the live version in the Prompt Library page named there, so Tanner's edits flow through.
- Apply the prompt to the transcript_text to produce the fixed transcript.
- Apply the same correction logic to the title and the full description so typos and transcription artifacts are fixed across all three fields.
- Preserve every link in the description exactly. Do not drop or shorten links.
- Do the cleaning yourself as the model. Do not write a script to do it.

### Step 4, build the Notion page

- Create the page in the Reference Assets data source using the structure in references/page_structure.md.
- Use `<table_of_contents/>` for navigation, `<callout icon="...">` for the banner, and toggle blocks for long transcript spans.
- Set properties: Name "EXT | <cleaned title>", Asset Type External Example, Source URL, Video Title, Stage Cleaned.

### Step 5, verify and finish

- Fetch the page back once. Confirm the TOC rendered, the transcript toggles exist, and the description links are clickable.
- Set Stage to Complete.
- Return the page id and url to the caller.

## Failure rule

- On any hard failure, stop and report what failed and why. Leave any page you already created intact. Never half-delete.
