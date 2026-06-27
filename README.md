# YouTube & Transcript Skills (Claude Code)

Internal Claude Code skills for YouTube and transcripts:

- **`youtube`** — fetch transcripts, video/channel search, channel browsing, and
  playlists via [transcriptapi.com](https://transcriptapi.com) with a **keyless
  local `yt-dlp` fallback**. Auto-fixes known mis-transcriptions.
- **`reconstruct-transcript`** — turn any pasted/auto-generated transcript
  (meeting, sales call, interview) into a faithful **reconstructed transcript**
  plus summary, sequential **action items by role**, objections/risks, sales
  insights, and key facts. **Learns** the corrections you provide over time.

## Layout

```
.claude/skills/
  youtube/                       # fetch + correct transcripts
    SKILL.md
    scripts/yt_transcript.py     # API → yt-dlp fallback; applies corrections.json
    corrections.json             # term glossary (misheard → correct) — MEMORY
  transcript/ , youtube-full/    # thin aliases → youtube
  reconstruct-transcript/        # clean + analyze a pasted transcript
    SKILL.md
    learned_rules.md             # non-term learnings (roles, formatting) — MEMORY
    scripts/correct_text.py      # apply the glossary to any text
tests/                           # offline unit tests
.github/workflows/ci.yml         # runs the tests on push/PR
requirements.txt                 # yt-dlp floor pin
```

Skills live under `.claude/skills/` because that is where **Claude Code
discovers project skills** (verified: see CHANGELOG). They load automatically in
any session opened on this repo.

## Remembering corrections (the learning loop)

Fixes you provide are stored in committed files, so they persist across sessions:

- **Term fixes** (a word/name/tool/acronym consistently misheard → correct form)
  go in **`.claude/skills/youtube/corrections.json`**. These are applied
  automatically to both fetched and pasted transcripts (whole-word,
  case-insensitive). Edit it directly or just tell me "X should be Y".
- **Rules & preferences** (participant↔role, speaker patterns, formatting,
  recurring structural fixes) go in
  **`.claude/skills/reconstruct-transcript/learned_rules.md`**.

When you paste a corrected transcript or say "remember that …", I identify the
fix, store it in the right place, and confirm what I saved.

## Setup

1. **(Optional) API key.** The script works without one via the `yt-dlp`
   fallback. To use the faster API path, get a free key at
   https://transcriptapi.com and add it to **`.claude/settings.local.json`**
   (gitignored — never commit it, never paste it into chat):

   ```json
   { "env": { "TRANSCRIPT_API_KEY": "sk_..." } }
   ```

2. **(Optional) Pin the fallback dependency** for reproducibility:

   ```bash
   python3 -m pip install -r requirements.txt
   ```

   Otherwise the script installs `yt-dlp` on first use.

3. **Network access.** In restricted environments (e.g. Claude Code on the web),
   allowlist these hosts in the environment's network policy:
   - `transcriptapi.com` (API)
   - `youtube.com`, `googlevideo.com`, `ytimg.com` (yt-dlp fallback)

## Usage

In Claude Code, just reference a video/channel/playlist (the `youtube` skill
triggers automatically), or invoke `/youtube`. Direct script use:

```bash
SCRIPT=.claude/skills/youtube/scripts/yt_transcript.py

# Transcript + title + description as JSON, also saving .txt files to ./out
python3 "$SCRIPT" "https://youtu.be/dQw4w9WgXcQ" --format json --out ./out

# Clean reading text, specific language
python3 "$SCRIPT" dQw4w9WgXcQ --no-timestamps --lang en

# What caption languages exist?
python3 "$SCRIPT" dQw4w9WgXcQ --list-langs

# Force the keyless local path / never auto-install yt-dlp
python3 "$SCRIPT" dQw4w9WgXcQ --no-api
python3 "$SCRIPT" dQw4w9WgXcQ --no-install

# Transcription fixes: applied automatically; disable or use a custom glossary
python3 "$SCRIPT" dQw4w9WgXcQ --no-fix
python3 "$SCRIPT" dQw4w9WgXcQ --glossary my_terms.json
```

### Fixing transcription errors

Auto-captions mishear jargon ("rorwaz" → **ROAS**, "VSSL" → **VSL**). The script
applies `.claude/skills/youtube/corrections.json` automatically (whole-word,
case-insensitive) and reports a `corrections` summary in its JSON. **Edit that
file to add your own domain terms** (`"misheard": "Correct"`). The skill also
instructs the agent to proofread remaining context-specific errors after
fetching. Use `--no-fix` to get the raw transcript.

`source` in the JSON tells you which path produced the result (`transcriptapi`
or `yt-dlp`). `description` is only available via the `yt-dlp` path — the API's
transcript metadata returns title/author but not a description.

For search, channels, and playlists (API only), see the reference in
`.claude/skills/youtube/SKILL.md`. Always verify parameters against the live
spec: https://transcriptapi.com/openapi.json

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `proxy 403` / `connect_rejected` | Host blocked by network policy | Allowlist `transcriptapi.com` / `youtube.com` etc. |
| API returns `401` | Bad/expired key | Fix `TRANSCRIPT_API_KEY`; script auto-falls back to yt-dlp |
| API returns `402` | Out of credits | Top up, or rely on the keyless fallback |
| `403` error code `1010` | Missing User-Agent (Cloudflare) | Send a `User-Agent` header |
| "No captions available" | Video has no CC | Nothing to fetch; try another video |
| yt-dlp fetch fails after a while | Stale yt-dlp vs. YouTube change | `python3 -m pip install -U yt-dlp` |

## Testing

```bash
python3 -m unittest discover -s tests -v
```

Offline only (no network/key needed). CI runs them on Python 3.9/3.11/3.12.

## Maintenance

- **Keep `yt-dlp` fresh** — YouTube extractor fixes ship in new releases.
- **Verify API params** against `openapi.json` before relying on them; the
  upstream skill docs drift (e.g. search/channel pagination is `continuation`,
  not a `limit` parameter).
- This build no longer uses the `npx skills` lockfile flow; skills are managed
  directly here under `.claude/skills/`.

## Uninstall / rollback

- Remove the skill: delete `.claude/skills/youtube`, `.claude/skills/transcript`,
  `.claude/skills/youtube-full`.
- Roll back a change: `git revert <commit>` or check out a previous tag.

See `CHANGELOG.md` for version history.
