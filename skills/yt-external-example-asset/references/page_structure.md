# External example asset, Notion page structure

This is the exact structure Worker 1 builds for the External Example asset.
The goal is a page that both a human and an AI agent can scan and jump around
in. The syntax below is verified to render correctly through the Notion MCP
create-pages tool.

## Verified Notion-flavored markdown

- Table of contents: `<table_of_contents/>` on its own line. This renders a real, clickable TOC that auto-updates from the headings.
- Callout: `<callout icon="📌">text</callout>`. Use a relevant emoji icon.
- Toggle heading: `## Title {toggle="true"}` followed by tab-indented child lines. Best for long collapsible sections like the transcript.
- Toggle block: `<details><summary>Title</summary>` then a blank line, content, blank line, `</details>`.
- Headings: `#`, `##`, `###`. The TOC is built from these, so heading text must be stable and descriptive.
- Bullets: flat only, each `- ` on its own line. No nesting.
- Do not use GitHub-style `> [!NOTE]` callouts. They render as literal text.

## Page property values

- Name: "EXT | <cleaned video title>"
- Asset Type: External Example
- Source URL: the YouTube URL
- Video Title: the cleaned video title
- Stage: set to Cleaned when the page is first written, then Complete after verification

## Page body, in order

- Callout banner at the top with the one-line identity of the asset, for example the channel name, the upload date, and the duration. Icon is a clapper or pin emoji.
- `<table_of_contents/>` right under the banner so every section is one click away.
- `## Overview` section with a short factual orientation: channel, upload date, duration, view count, and the source link. No analysis here, this asset is the clean source of record.
- `## Title` section showing the cleaned title as a quote or bold line, with the raw title in a toggle if it differed.
- `## Description` section with the full cleaned description. Preserve every link as a real link. If the description is long, wrap the back half in a `<details>` toggle so the page stays scannable. Keep all links visible, not hidden.
- `## Links found` section listing every link harvested from the description and transcript as a flat bullet list, each bullet showing the link and where it was found. This section feeds Worker 2.
- `## Chapters` section if the video had chapters, as a flat bullet list of timestamp and title.
- `## Transcript` section. Put the full cleaned transcript inside toggle blocks. Split the transcript into labeled parts of a few minutes each, for example "Transcript 00:00 to 05:00", so a reader can open just the part they want. Inside each toggle the text is the cleaned, paragraph-formatted transcript for that span.
- `## Invitations to act` section at the end, the list the cleaning prompt extracts, as a flat bullet list.

## Cleaning step

- The title, the description, and the transcript are all passed through the reused cleaning prompt at scripts/clean_prompt.md before they go on the page.
- The cleaning is done by Claude reading the prompt and the raw text, not by a script. The script only extracts raw material.

## Verification

- After writing the page, fetch it back once and confirm the TOC rendered, the transcript toggles exist, and the links are clickable. Then set Stage to Complete.
