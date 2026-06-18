---
name: yt-reference-pipeline
description: >-
  Orchestrator skill. Input is a single YouTube URL and nothing else. It runs
  Worker 1 (yt-external-example-asset) to build the External Example asset, then
  Worker 2 (yt-internal-application-asset) to build the linked Internal
  Application asset, then runs the Actionability Loop against the relevant
  departmental context and handbook section. Each stage writes a Notion page and
  passes its page id to the next. Use whenever Tanner provides a YouTube link and
  wants the full reference-asset pair plus the close-the-loop decision flow.
---

# yt-reference-pipeline

## Purpose

One YouTube link in, a complete set of linked Notion reference assets out. The
only human input is the URL. Everything downstream is automatic.

## Inputs

- A single YouTube URL.

## Output

- External Example asset page (Worker 1).
- Internal Application asset page, linked to it (Worker 2).
- Actionability Loop section or page, linked to both, when the handbook and departmental context can be located.

## Read first

- skills/shared/formatting_rules.md
- skills/shared/notion_config.md

## Pipeline

### Stage 1, run Worker 1

- Invoke yt-external-example-asset with the URL.
- It returns the External Example page id and url.
- If Worker 1 fails, stop. Report what failed and why. Do not start Worker 2.

### Stage 2, run Worker 2

- Invoke yt-internal-application-asset with the External Example page id and the extract payload.
- It returns the Internal Application page id and url, linked to the External Example page.
- If Worker 2 fails, stop. Report what failed and why. Leave the External Example page intact. Never half-delete.

### Stage 3, run the Actionability Loop

- See the dedicated section below. This stage cross-references the Internal Application asset against the relevant departmental context and handbook section.

## Actionability Loop

The loop takes the Internal Application asset and decides what is actually
actionable, when, and where it maps.

### Step 1, locate the context

- Search Notion for the departmental context and the handbook section relevant to this asset.
- As of the last check, a native Notion company handbook and departmental handbook were not yet built. Tanner's own spec page named "Claude skill for youtube link" has an open checkbox for building them. Related material exists as Google Docs named "Launch Sales Handbook" and "BUILD SMALL SALES ONBOARDING AND TRAINING HANDBOOK SYSTEM", plus a Notion page listing departments and the owners Corwin for Delivery, Hunter for Acquisition and Sales, Tanner for Operations.

### Step 2, decide whether to proceed

- If you can confidently locate the handbook and departmental context in Notion, build the full loop in Step 3.
- If you cannot, do not guess. Stop the loop, leave both completed assets intact, and tell Tanner exactly what is missing and where to put it. Write a short callout on the Internal Application asset that says the Actionability Loop is pending the handbook location. This is the deferred default that Tanner selected at build time.

### Step 3, build the decision flow

- Create a clearly sectioned, navigable Notion page named "LOOP | <video title>", or a dedicated section on the Internal Application asset, linked to both prior assets through the Paired Asset relation.
- The decision flow outputs three things for every candidate action from the Internal Application asset.
- Output, what is immediately actionable now.
- Output, for anything not now, when it becomes actionable and under what conditions.
- Output, where each item maps, which department and which handbook section.
- Use `<table_of_contents/>`, headings, and callouts so the page is navigable.

## Cross-cutting requirements

- Every asset is easy to find for humans and AI agents, through consistent EXT, INT, and LOOP naming, the Paired Asset relation, and the single Reference Assets database parent.
- Every asset is interactive, with a table of contents, headings, toggles, and callouts.
- Every asset has stable headings so sections and subsections are easy to reference.
- Every asset earns its space. No filler.

## Stop and report rule

- On any stage failure, stop, report what failed and why, and leave completed stages intact. Never half-delete.
