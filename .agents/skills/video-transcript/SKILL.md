---
name: video-transcript
description: "Use when video content needs to be extracted as text: pasted YouTube links or IDs, requests to transcribe, summarize, quote, translate, convert video to text, or extract information from video content. Also use when a user shares a video URL without explanation and wants to know what it says. Not for uploads or account management."
version: "1.5.0"
user-invocable: true
compatibility: Requires internet access to reach transcriptapi.com. No additional runtimes or dependencies needed.
required_environment_variables:
  - name: TRANSCRIPT_API_KEY
    prompt: Your TranscriptAPI key (starts with sk_)
    help: Free account at https://transcriptapi.com — 100 credits, no card required. Or let the agent create one for you.
    required_for: all API requests
metadata: {"openclaw":{"emoji":"▶️","requires":{"env":["TRANSCRIPT_API_KEY"]},"primaryEnv":"TRANSCRIPT_API_KEY","homepage":"https://transcriptapi.com"},"hermes":{"tags":["youtube","transcripts","video","captions","text-extraction","summarization"],"category":"media"}}
---

# Video Transcript

Extract transcripts from videos via [TranscriptAPI.com](https://transcriptapi.com).

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

## GET /api/v2/youtube/transcript

```bash
curl -s "https://transcriptapi.com/api/v2/youtube/transcript\
?video_url=VIDEO_URL&format=text&include_timestamp=true&send_metadata=true" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY" \
  -H "User-Agent: YourAgent/1.0"
```

| Param               | Required | Default | Values                                 |
| ------------------- | -------- | ------- | -------------------------------------- |
| `video_url`         | yes      | —       | YouTube URL or 11-char video ID        |
| `format`            | no       | `json`  | `json` (structured), `text` (readable) |
| `include_timestamp` | no       | `true`  | `true`, `false`                        |
| `send_metadata`     | no       | `false` | `true`, `false`                        |

Accepted URL formats:

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://youtube.com/shorts/VIDEO_ID`
- Bare video ID: `dQw4w9WgXcQ`

**Response** (`format=text&send_metadata=true`):

```json
{
  "video_id": "dQw4w9WgXcQ",
  "language": "en",
  "transcript": "[00:00:18] We're no strangers to love\n[00:00:21] You know the rules...",
  "metadata": {
    "title": "Rick Astley - Never Gonna Give You Up",
    "author_name": "Rick Astley",
    "author_url": "https://www.youtube.com/@RickAstley",
    "thumbnail_url": "https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"
  }
}
```

**Response** (`format=json`):

```json
{
  "video_id": "dQw4w9WgXcQ",
  "language": "en",
  "transcript": [
    { "text": "We're no strangers to love", "start": 18.0, "duration": 3.5 },
    { "text": "You know the rules and so do I", "start": 21.5, "duration": 2.8 }
  ]
}
```

## Tips

- Summarize long transcripts into key points first, offer full text on request.
- Use `format=json` when you need precise timestamps for quoting specific moments.
- Use `send_metadata=true` to get video title and channel for context.
- Works with YouTube Shorts too.

## Errors

| Code     | Meaning          | Action                                         |
| -------- | ---------------- | ---------------------------------------------- |
| 401      | Bad API key      | Check key or re-setup                          |
| 402      | No credits       | Top up at transcriptapi.com/billing            |
| 403/1010 | Cloudflare block | Add or fix User-Agent header                   |
| 404      | No transcript    | Video may not have captions enabled            |
| 408      | Timeout          | Retry once after 2s                            |

1 credit per successful request. Errors don't consume credits. Free tier: 100 credits, 300 req/min.
