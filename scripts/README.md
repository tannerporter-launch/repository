# scripts/yt_transcript.py — local YouTube transcript fallback

A self-contained fallback for the `*-skills` bundle (which depends on the
third-party service transcriptapi.com). This script lets you fetch a transcript
with **no API key and no third-party account** by using `yt-dlp` locally.

## How it chooses a source (automatic fallback)

1. **TranscriptAPI** (`https://transcriptapi.com`) — used **only** if
   `$TRANSCRIPT_API_KEY` is set. Skipped entirely otherwise, and skipped on any
   error.
2. **yt-dlp** (local) — downloads the caption track YouTube already serves and
   parses it here. If `yt-dlp` is missing it is installed into the current
   Python environment on first use (disable with `--no-install`).

So if the API is down, rate-limited, or unconfigured, the local path steps in
automatically.

## Usage

```bash
# Default: text output with [HH:MM:SS] timestamps
python3 scripts/yt_transcript.py "https://youtu.be/dQw4w9WgXcQ"

# JSON output (mirrors the API shape: text/start/duration per segment)
python3 scripts/yt_transcript.py dQw4w9WgXcQ --format json

# Clean text for reading/translation
python3 scripts/yt_transcript.py dQw4w9WgXcQ --no-timestamps

# Pick a language, force the local path, or forbid auto-install
python3 scripts/yt_transcript.py <id> --lang es
python3 scripts/yt_transcript.py <id> --no-api
python3 scripts/yt_transcript.py <id> --no-install

# Also save files: transcript_timestamped.txt + transcript_clean.txt into ./out
python3 scripts/yt_transcript.py <id> --out ./out

# List the caption languages available for a video, then exit
python3 scripts/yt_transcript.py <id> --list-langs
```

### Flags

| Flag | Effect |
| --- | --- |
| `--format text\|json` | Output shape (default `text`). |
| `--lang CODE` | Preferred caption language (default `en`). |
| `--no-timestamps` | Omit `[HH:MM:SS]` prefixes in text output. |
| `--out DIR` | Also write `transcript_timestamped.txt` + `transcript_clean.txt` (each with a title/description header) into `DIR`. |
| `--list-langs` | Print available manual + auto caption languages as JSON, then exit. |
| `--no-api` | Skip TranscriptAPI even if a key is set; go straight to `yt-dlp`. |
| `--no-install` | Never auto-install `yt-dlp`. |

The API path automatically retries transient failures (HTTP 408/429/5xx, up to
two retries with backoff) before falling back to `yt-dlp`.

Accepts full URLs, `youtu.be/<id>`, `youtube.com/shorts/<id>`,
`youtube.com/embed/<id>`, or a bare 11-character video ID.

## Output

`--format json`:

```json
{
  "video_id": "dQw4w9WgXcQ",
  "language": "en",
  "source": "yt-dlp",
  "title": "Rick Astley - Never Gonna Give You Up",
  "description": "The official video for ...",
  "channel": "Rick Astley",
  "transcript": [
    { "text": "We're no strangers to love", "start": 18.0, "duration": 3.5 }
  ]
}
```

`source` tells you which path produced the result (`transcriptapi` or `yt-dlp`).
`title`/`description`/`channel` come from the video metadata; they may be `null`
when the source can't supply them (TranscriptAPI does not always return a
description). In `--format text` they render as a header above the transcript.

## Requirements & notes

- **Python 3.8+** (uses only the standard library; `yt-dlp` is installed on demand).
- Needs outbound network access to YouTube. In sandboxed environments where
  `youtube.com` is blocked at the proxy, the local path will fail with a clear
  proxy error — run it from a machine with normal egress.
- Exit codes: `0` success, `1` fetch/parse failure, `2` bad video argument.

## Network access (allowlist)

In restricted environments (e.g. Claude Code on the web), outbound traffic is
filtered. Allow these hosts in the environment's network policy or every request
fails with a proxy `403`:

- `transcriptapi.com` — the API path
- `youtube.com`, `googlevideo.com`, `ytimg.com` — the `yt-dlp` fallback path

## Maintenance note — `skills-lock.json`

`skills-lock.json` (repo root) records the **original upstream hashes** of the
12 installed skills. Because the skills were hardened locally (the
`references/auth-setup.md` token-bypass files were removed and the setup
sections rewritten), those hashes no longer match the working copies. This is
expected. Be aware that running `npx skills update` may flag the drift and try
to restore the upstream versions — **including the removed auth-bypass file** —
so review any such update before accepting it.
