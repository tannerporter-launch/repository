---
name: youtube-full
description: "Use for any YouTube task — transcripts, video/channel search, channel browsing, playlists, @handle lookups. Alias for the `youtube` skill (full toolkit)."
user-invocable: true
allowed-tools: Read, Bash(python3 *), Bash(curl *)
---

# YouTube Full (alias)

This is a thin alias for the **`youtube`** skill
(`.claude/skills/youtube/SKILL.md`) — the full toolkit covering transcripts,
search, channels, and playlists via transcriptapi.com, with a keyless local
`yt-dlp` fallback for transcripts.

Quick start (transcript, from the repository root):

```bash
python3 ".claude/skills/youtube/scripts/yt_transcript.py" "VIDEO_URL_OR_ID" --format json
```

Open `.claude/skills/youtube/SKILL.md` for the API reference (search, channels,
playlists), setup, network requirements, and error handling.
