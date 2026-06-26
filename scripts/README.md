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
```

Accepts full URLs, `youtu.be/<id>`, `youtube.com/shorts/<id>`,
`youtube.com/embed/<id>`, or a bare 11-character video ID.

## Output

`--format json`:

```json
{
  "video_id": "dQw4w9WgXcQ",
  "language": "en",
  "source": "yt-dlp",
  "transcript": [
    { "text": "We're no strangers to love", "start": 18.0, "duration": 3.5 }
  ]
}
```

`source` tells you which path produced the result (`transcriptapi` or `yt-dlp`).

## Requirements & notes

- **Python 3.8+** (uses only the standard library; `yt-dlp` is installed on demand).
- Needs outbound network access to YouTube. In sandboxed environments where
  `youtube.com` is blocked at the proxy, the local path will fail with a clear
  proxy error — run it from a machine with normal egress.
- Exit codes: `0` success, `1` fetch/parse failure, `2` bad video argument.
