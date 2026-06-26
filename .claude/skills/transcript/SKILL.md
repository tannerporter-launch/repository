---
name: transcript
description: "Use when the spoken content of a YouTube video is needed — pasted links or IDs, or requests to summarize, quote, transcribe, translate, or fact-check a video. Alias for the `youtube` skill's transcript flow."
user-invocable: true
allowed-tools: Read, Bash(python3 *)
---

# Transcript (alias)

This is a thin alias. The full implementation lives in the **`youtube`** skill
(`.claude/skills/youtube/SKILL.md`), which covers transcripts, search, channels,
and playlists, with a keyless local `yt-dlp` fallback.

For a transcript with title + description, run from the repository root:

```bash
python3 ".claude/skills/youtube/scripts/yt_transcript.py" "VIDEO_URL_OR_ID" --format json --out ./out
```

It tries TranscriptAPI when `$TRANSCRIPT_API_KEY` is set and automatically falls
back to `yt-dlp` (no account needed). See the `youtube` skill for options,
setup, and the full API reference.
