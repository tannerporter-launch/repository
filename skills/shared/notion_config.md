# Notion configuration (shared across the pipeline)

Every skill reads this file to find the predictable home for reference assets
and to follow one naming convention. This keeps assets easy to find for both
human agents and AI agents.

## Reference Assets database

- Database name: Reference Assets
- Database URL: https://app.notion.com/p/4e0148d9c403459b968217a4fbd83e9b
- Data source id (use this as the parent when creating pages): 345f0fe0-7095-46ab-ac50-d73a6eb6dd02
- Parent location: Personal Operating System (top-level page)

## Schema

- Name: title
- Asset Type: select, one of External Example, Internal Application, Actionability Loop
- Source URL: url
- Stage: select, one of Extracting, Cleaned, Analyzed, Complete, Failed
- Video Title: text
- Paired Asset: relation to the same database (links the EXT and INT pages both ways)
- Asset ID: auto increment, prefix RA
- Created: created time
- Last Edited: last edited time

## Naming convention

- External example asset Name: "EXT | <video title>"
- Internal application asset Name: "INT | <video title>"
- Actionability loop section or page Name: "LOOP | <video title>"
- The shared "<video title>" string is the human-readable video title after cleaning, so a person scanning the database sees the pair next to each other.

## Linking rule

- Worker 1 creates the External Example page and sets Asset Type to External Example, Stage to the current stage, Source URL, and Video Title.
- Worker 2 creates the Internal Application page, sets Asset Type to Internal Application, and sets Paired Asset to the External Example page. Because the relation is two-way, the External Example page shows the back link automatically.
- The Actionability Loop, when built, links to both pages through the same Paired Asset relation or an explicit backlink in the page body.

## Verification rule

- After creating or updating a page, fetch it back once and confirm the title, the Asset Type, and the Paired Asset relation are set before moving to the next stage.
