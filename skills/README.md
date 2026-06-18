# yt-reference-pipeline skills

One YouTube link in, a set of linked, navigable Notion reference assets out.
The only human input is the URL. Everything downstream is automatic.

## What is in here

- yt-reference-pipeline, the orchestrator. Runs Worker 1, then Worker 2, then the Actionability Loop.
- yt-external-example-asset, Worker 1. Extracts the transcript, title, and full description, fixes typos with the reused transcript-formatter prompt, and writes the External Example asset to Notion.
- yt-internal-application-asset, Worker 2. Analyzes the External Example asset and writes the linked Internal Application asset, including the Step 5 link and landing-page teardown.
- shared, the formatting rules and the Notion configuration both workers read.

## How the pieces connect

- The orchestrator passes each stage's Notion page id to the next stage.
- Worker 1 writes "EXT | <title>". Worker 2 writes "INT | <title>" and links it back through the Paired Asset relation. The Actionability Loop writes "LOOP | <title>".
- All pages live in one Notion database, Reference Assets, under the Personal Operating System page, so humans and AI agents always find the pair together.

## Install

- Copy the three skill folders into your skills directory, for example ~/.claude/skills, keeping the shared folder alongside them.
- The skills reference each other by name, so keep the folder names as they are.

## Invoke

- Give Claude the orchestrator and one URL, for example: run yt-reference-pipeline on https://www.youtube.com/watch?v=VIDEO_ID
- Worker 1 and Worker 2 can also be run on their own if you only need one asset.

## Setup you still need

- Python packages, already used by the scripts: yt-dlp, youtube-transcript-api, playwright.
- Install the Playwright browser once: python3 -m playwright install chromium
- Notion MCP must be connected, which it is in this workspace.
- Optional, for the Tier 3 hosted screenshot fallback: set SCREENSHOTONE_API_KEY. The free tier is fine. Only public URLs are ever sent to it.
- Optional, for the Tier 2 interactive funnel walk through: the @playwright/mcp server, used only for links flagged interactive.

## Network egress requirements

- The scripts need outbound access to these hosts. In a restricted or allowlist network, add them.
- youtube.com and www.youtube.com
- googlevideo.com and the youtube caption hosts
- r.jina.ai, for the Tier 1 clean page text
- api.screenshotone.com, only if you use the Tier 3 hosted fallback
- yt-dlp can be blocked when run from a cloud or datacenter IP. Run the pipeline from a residential connection, or pass cookies to yt-dlp, or supply a manual transcript with the extractor's --transcript-file flag.

## TLS note

- Both scripts trust the active system CA bundle, so they work behind a TLS-inspecting proxy while keeping certificate verification on.

## Formatting rules

- See shared/formatting_rules.md. No em dashes, flat bullets, and section titles that lead with the tool or feature name. These apply to every output the pipeline produces.
