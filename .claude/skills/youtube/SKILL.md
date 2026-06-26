---
name: youtube
description: "Use when YouTube content is or could be relevant — pasted video/channel/playlist links, video IDs, @handles, or requests to summarize, quote, transcribe, translate, fact-check, or research a video, channel, or playlist. Covers transcripts, video/channel search, channel browsing, and playlists via transcriptapi.com, with a keyless local yt-dlp fallback. Not for uploads or account management."
user-invocable: true
allowed-tools: Read, Bash(python3 *), Bash(curl *)
---

# YouTube

Full YouTube toolkit: transcripts, search, channel browsing, and playlists via
[TranscriptAPI.com](https://transcriptapi.com), with a **keyless local fallback**
(`yt-dlp`) so transcripts work even with no API key or when the API is down.

## Recommended: one resilient command (transcripts)

For a transcript **plus title + description** in one step, prefer the bundled
script over raw `curl`. It uses TranscriptAPI when `$TRANSCRIPT_API_KEY` is set
and **automatically falls back to local `yt-dlp` on any failure** — bad/expired
key (401), no credits (402), network block (403), or no captions.

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/yt_transcript.py" "VIDEO_URL_OR_ID" --format json --out ./out
```

- `--out DIR` also writes `transcript_timestamped.txt` + `transcript_clean.txt`
  (each with a title/description header). Omit to print to stdout.
- `--format text` for readable text, `--lang es` to choose a language,
  `--list-langs` to see available captions.
- `${CLAUDE_SKILL_DIR}` resolves to this skill's directory; the command works
  from any working directory.

> The **description** field comes only from the `yt-dlp` path — TranscriptAPI's
> transcript metadata returns `title`/`author` but **not** a description
> (verified against `openapi.json`). The script handles this automatically.

## Setup (API key — optional)

The script works **without a key** via the `yt-dlp` fallback. To use the faster
API path, set `TRANSCRIPT_API_KEY` (free tier at https://transcriptapi.com).

- **Preferred:** put it in `.claude/settings.local.json` (gitignored) so it is
  available across sessions without re-entering it:
  ```json
  { "env": { "TRANSCRIPT_API_KEY": "sk_..." } }
  ```
- Do **not** paste the key into chat, auto-register an account, or write the key
  to a tracked file. If the key is missing, ask the user once or use the
  keyless fallback.

## API reference (transcriptapi.com)

Authoritative, always-current spec: **https://transcriptapi.com/openapi.json** —
check it before relying on any parameter. Base path: `/api/v2/youtube`.

**Auth + headers (every request):**

- `Authorization: Bearer $TRANSCRIPT_API_KEY`
- `User-Agent: ClaudeCode/1.0` — omitting it triggers a Cloudflare 403 (1010).

Channel endpoints accept `channel` = `@handle`, channel URL, or `UC...` ID.
Playlist endpoints accept `playlist` = a playlist URL or ID. **Pagination is
cursor-based via `continuation`** — there is no `limit` parameter; slice
client-side if you need fewer results.

### GET /transcript — 1 credit

```bash
curl -s "https://transcriptapi.com/api/v2/youtube/transcript\
?video_url=VIDEO_URL&format=text&include_timestamp=true&send_metadata=true" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY" -H "User-Agent: ClaudeCode/1.0"
```

| Param | Required | Default | Values |
| --- | --- | --- | --- |
| `video_url` | yes | — | YouTube URL or 11-char ID |
| `format` | no | `json` | `json`, `text` |
| `include_timestamp` | no | `true` | `true`, `false` |
| `send_metadata` | no | `false` | `true`, `false` (adds `title`, `author_name`, `author_url`, `thumbnail_url` — no description) |

### GET /search — 1 credit

```bash
curl -s "https://transcriptapi.com/api/v2/youtube/search?q=QUERY&type=video" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY" -H "User-Agent: ClaudeCode/1.0"
```

| Param | Required | Default | Values |
| --- | --- | --- | --- |
| `q` | yes (for first page) | — | search text |
| `type` | no | `video` | `video`, `channel` |
| `continuation` | no | — | cursor from a previous response for the next page |

### Channels

```bash
# Resolve a handle (free)
curl -s ".../api/v2/youtube/channel/resolve?input=@TED" -H ... -H ...
# Latest uploads (free)
curl -s ".../api/v2/youtube/channel/latest?channel=@TED" -H ... -H ...
# All videos (1 credit/page) — paginate with continuation
curl -s ".../api/v2/youtube/channel/videos?channel=@NASA" -H ... -H ...
# Search within a channel (1 credit)
curl -s ".../api/v2/youtube/channel/search?channel=@TED&q=QUERY" -H ... -H ...
```

| Endpoint | Params | Cost |
| --- | --- | --- |
| `channel/resolve` | `input` (req) | free |
| `channel/latest` | `channel` | free |
| `channel/videos` | `channel` **or** `continuation` | 1/page |
| `channel/search` | `channel`, `q`, `continuation` | 1 |

### GET /playlist/videos — 1 credit/page

```bash
curl -s ".../api/v2/youtube/playlist/videos?playlist=PL_ID" -H ... -H ...
# next page:
curl -s ".../api/v2/youtube/playlist/videos?continuation=TOKEN" -H ... -H ...
```

Provide exactly one of `playlist` or `continuation`. Responses include
`continuation` and `has_more` (or equivalent) for paging.

## Network access

In locked-down environments, allow these hosts in the environment's network
policy or requests fail with a proxy `403`:

- `transcriptapi.com` — the API
- `youtube.com`, `googlevideo.com`, `ytimg.com` — the local `yt-dlp` fallback

## Errors

| Code | Meaning | Action |
| --- | --- | --- |
| 401 | Bad/expired key | Check key; the script auto-falls back to yt-dlp |
| 402 | No credits | Top up, or use the keyless fallback |
| 403 / 1010 | Cloudflare / proxy block | Add `User-Agent`; allowlist the host |
| 404 | Not found / no captions | Video/resource missing or has no CC |
| 408 / 429 / 5xx | Transient | Script retries up to twice, then falls back |

Free tier: 100 credits, 300 req/min. See `README.md` for troubleshooting,
maintenance, and uninstall steps.
