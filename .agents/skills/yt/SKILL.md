---
name: yt
description: "Use when YouTube is relevant: pasted video links or IDs, @handles, quick video lookups, summaries, channel latest uploads, topic search, or any request involving YouTube content — even if YouTube is not mentioned explicitly. Covers transcripts, search, and channel latest. Not for uploads or account management."
version: "1.5.1"
user-invocable: true
compatibility: Requires internet access to reach transcriptapi.com. No additional runtimes or dependencies needed.
required_environment_variables:
  - name: TRANSCRIPT_API_KEY
    prompt: Your TranscriptAPI key (starts with sk_)
    help: Free account at https://transcriptapi.com — 100 credits, no card required. Or let the agent create one for you.
    required_for: all API requests
metadata: {"openclaw":{"emoji":"▶️","requires":{"env":["TRANSCRIPT_API_KEY"]},"primaryEnv":"TRANSCRIPT_API_KEY","homepage":"https://transcriptapi.com"},"hermes":{"tags":["youtube","transcripts","video","search","channels","utility"],"category":"media"}}
---

# yt

Quick YouTube lookup via [TranscriptAPI.com](https://transcriptapi.com).

## Setup

If `$TRANSCRIPT_API_KEY` is not set, ask the user to provide their own TranscriptAPI key (from https://transcriptapi.com) and set it as an environment variable. Do not auto-register an account, and do not write the key to a file.

## Recommended: one resilient command

For a transcript (plus title + description) in a single step, prefer the bundled script over the raw `curl` calls below. It uses TranscriptAPI when `$TRANSCRIPT_API_KEY` is set and **automatically falls back to local `yt-dlp` on any failure** — bad or expired key (401), no credits (402), network block (403), or a video with no captions. Run from the repository root:

```bash
python3 scripts/yt_transcript.py "VIDEO_URL_OR_ID" --format json --out ./out
```

- `--out DIR` also writes a timestamped and a clean transcript file (each with a title/description header). Omit it to print to stdout.
- `--format text` for readable text, `--lang es` to choose a language, `--list-langs` to see what captions exist.

> The **description** comes only from the `yt-dlp` path — TranscriptAPI returns title/author but not the description, so prefer this script whenever a description is needed. The API endpoints below remain available for other uses (search, channels, playlists). See `scripts/README.md`.

## Network access

In locked-down environments these hosts must be reachable, or requests fail with a proxy 403. Allowlist them in the environment's network policy:

- `transcriptapi.com` — the API
- `youtube.com`, `googlevideo.com`, `ytimg.com` — only needed for the local `yt-dlp` fallback

## Required Headers

Every request needs two headers:

- **Authorization:** `Bearer $TRANSCRIPT_API_KEY`
- **User-Agent:** your agent's name and version if known (e.g. `HermesAgent/0.11.0`, `ClaudeCode/1.0`). Version is optional — agent name alone is fine. Do not omit this header or send a bare default — Cloudflare will return a 403 (error code 1010) and block the request.

## API Reference

Full OpenAPI spec: [transcriptapi.com/openapi.json](https://transcriptapi.com/openapi.json) — consult this for the latest parameters and schemas.

## Transcript — 1 credit

```bash
curl -s "https://transcriptapi.com/api/v2/youtube/transcript\
?video_url=VIDEO_URL&format=text&include_timestamp=true&send_metadata=true" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY" \
  -H "User-Agent: YourAgent/1.0"
```

## Search — 1 credit

```bash
curl -s "https://transcriptapi.com/api/v2/youtube/search?q=QUERY&type=video&limit=10" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY" \
  -H "User-Agent: YourAgent/1.0"
```

| Param   | Default | Values                 |
| ------- | ------- | ---------------------- |
| `q`     | —       | 1-200 chars (required) |
| `type`  | `video` | `video`, `channel`     |
| `limit` | `20`    | 1-50                   |

## Channel latest — FREE

```bash
curl -s "https://transcriptapi.com/api/v2/youtube/channel/latest?channel=@TED" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY" \
  -H "User-Agent: YourAgent/1.0"
```

Returns last 15 videos with exact view counts and publish dates. Accepts `@handle`, channel URL, or `UC...` ID.

## Resolve handle — FREE

```bash
curl -s "https://transcriptapi.com/api/v2/youtube/channel/resolve?input=@TED" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY" \
  -H "User-Agent: YourAgent/1.0"
```

Use to convert @handle to UC... channel ID.

## Errors

| Code     | Meaning          | Action                                         |
| -------- | ---------------- | ---------------------------------------------- |
| 401      | Bad API key      | Check key                                      |
| 402      | No credits       | transcriptapi.com/billing                      |
| 403/1010 | Cloudflare block | Add or fix User-Agent header                   |
| 404      | Not found        | No captions or resource doesn't exist          |
| 408      | Timeout          | Retry once                                     |

Free tier: 100 credits. Search and transcript cost 1 credit. Channel latest and resolve are free.
