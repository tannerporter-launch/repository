#!/usr/bin/env python3
"""
yt_transcript.py — fetch a YouTube transcript with an automatic local fallback.

Why this exists
---------------
The installed `*-skills` bundle reaches out to the third-party service
transcriptapi.com. This script gives you a self-hosted fallback that needs no
account and no API key, so you are never fully dependent on that service.

Attempt order (the fallback "steps in" automatically):
  1. TranscriptAPI (https://transcriptapi.com) — ONLY if $TRANSCRIPT_API_KEY is
     set. Skipped entirely otherwise, and skipped on any error.
  2. yt-dlp — local, no key, no third-party account. yt-dlp downloads the
     caption track YouTube already serves and we parse it here. If yt-dlp is not
     installed, the script installs it into the current Python environment on
     first use (disable with --no-install).

Usage
-----
  python3 scripts/yt_transcript.py "https://youtu.be/dQw4w9WgXcQ"
  python3 scripts/yt_transcript.py dQw4w9WgXcQ --format json
  python3 scripts/yt_transcript.py <id> --lang es --no-timestamps
  python3 scripts/yt_transcript.py <id> --no-api      # force local yt-dlp
  python3 scripts/yt_transcript.py <id> --no-install  # never auto-install yt-dlp

Output mirrors the API's shape:
  {"video_id","language","source","transcript":[{"text","start","duration"}...]}
or, with --format text, the joined caption lines (with [HH:MM:SS] unless
--no-timestamps).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request

API_BASE = "https://transcriptapi.com/api/v2/youtube/transcript"
USER_AGENT = "yt-transcript-fallback/1.0"


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def extract_video_id(value: str) -> str:
    """Accept a full URL, short URL, shorts URL, or a bare 11-char video ID."""
    value = value.strip()
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", value):
        return value
    parsed = urllib.parse.urlparse(value)
    if parsed.netloc.endswith("youtu.be"):
        candidate = parsed.path.lstrip("/").split("/")[0]
        if candidate:
            return candidate
    if "youtube.com" in parsed.netloc:
        qs = urllib.parse.parse_qs(parsed.query)
        if "v" in qs and qs["v"]:
            return qs["v"][0]
        # /shorts/<id>, /embed/<id>, /live/<id>
        parts = [p for p in parsed.path.split("/") if p]
        if len(parts) >= 2 and parts[0] in {"shorts", "embed", "live", "v"}:
            return parts[1]
    raise ValueError(f"Could not extract a YouTube video ID from: {value!r}")


def seconds_to_hms(seconds: float) -> str:
    seconds = int(seconds)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def render(result: dict, fmt: str, timestamps: bool) -> str:
    if fmt == "json":
        return json.dumps(result, ensure_ascii=False, indent=2)
    lines = []
    for seg in result["transcript"]:
        text = seg["text"]
        if timestamps:
            lines.append(f"[{seconds_to_hms(seg['start'])}] {text}")
        else:
            lines.append(text)
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# Source 1: TranscriptAPI (only when a key is present)
# --------------------------------------------------------------------------- #
def try_api(video_id: str, key: str, lang: str | None) -> dict | None:
    params = {
        "video_url": video_id,
        "format": "json",
        "include_timestamp": "true",
        "send_metadata": "false",
    }
    url = f"{API_BASE}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {key}", "User-Agent": USER_AGENT},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except Exception as exc:  # noqa: BLE001 - any failure means fall back
        print(f"[fallback] TranscriptAPI unavailable ({exc}); using yt-dlp.",
              file=sys.stderr)
        return None

    transcript = payload.get("transcript")
    if not isinstance(transcript, list) or not transcript:
        print("[fallback] TranscriptAPI returned no transcript; using yt-dlp.",
              file=sys.stderr)
        return None
    return {
        "video_id": payload.get("video_id", video_id),
        "language": payload.get("language", lang or "unknown"),
        "source": "transcriptapi",
        "transcript": [
            {
                "text": s.get("text", ""),
                "start": float(s.get("start", 0.0)),
                "duration": float(s.get("duration", 0.0)),
            }
            for s in transcript
        ],
    }


# --------------------------------------------------------------------------- #
# Source 2: local yt-dlp
# --------------------------------------------------------------------------- #
def ensure_ytdlp(auto_install: bool) -> list[str]:
    """Return the command prefix used to invoke yt-dlp, installing if needed."""
    if shutil.which("yt-dlp"):
        return ["yt-dlp"]
    try:
        import yt_dlp  # noqa: F401
        return [sys.executable, "-m", "yt_dlp"]
    except ImportError:
        pass
    if not auto_install:
        raise RuntimeError(
            "yt-dlp is not installed. Install it with "
            "`python3 -m pip install yt-dlp` or rerun without --no-install."
        )
    print("[fallback] Installing yt-dlp into the current environment...",
          file=sys.stderr)
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "--quiet", "yt-dlp"],
        check=True,
    )
    return [sys.executable, "-m", "yt_dlp"]


def _parse_json3(text: str) -> list[dict]:
    data = json.loads(text)
    out = []
    for event in data.get("events", []):
        segs = event.get("segs")
        if not segs:
            continue
        line = "".join(seg.get("utf8", "") for seg in segs).strip()
        if not line:
            continue
        start = event.get("tStartMs", 0) / 1000.0
        dur = event.get("dDurationMs", 0) / 1000.0
        out.append({"text": line, "start": start, "duration": dur})
    return out


_VTT_TS = re.compile(
    r"(\d{2}):(\d{2}):(\d{2})\.(\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2})\.(\d{3})"
)


def _vtt_ts_to_seconds(h, m, s, ms) -> float:
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0


def _parse_vtt(text: str) -> list[dict]:
    out = []
    blocks = re.split(r"\n\s*\n", text)
    for block in blocks:
        m = _VTT_TS.search(block)
        if not m:
            continue
        start = _vtt_ts_to_seconds(*m.group(1, 2, 3, 4))
        end = _vtt_ts_to_seconds(*m.group(5, 6, 7, 8))
        lines = block.splitlines()
        body = []
        for line in lines:
            if _VTT_TS.search(line) or line.strip().upper() == "WEBVTT":
                continue
            cleaned = re.sub(r"<[^>]+>", "", line).strip()
            if cleaned:
                body.append(cleaned)
        caption = " ".join(body).strip()
        if caption:
            out.append({"text": caption, "start": start,
                        "duration": max(0.0, end - start)})
    # yt-dlp auto-captions repeat rolling lines; drop consecutive duplicates.
    deduped = []
    for seg in out:
        if deduped and deduped[-1]["text"] == seg["text"]:
            continue
        deduped.append(seg)
    return deduped


def try_ytdlp(video_id: str, lang: str, auto_install: bool) -> dict:
    cmd_prefix = ensure_ytdlp(auto_install)
    url = f"https://www.youtube.com/watch?v={video_id}"
    with tempfile.TemporaryDirectory() as tmp:
        out_tmpl = os.path.join(tmp, "%(id)s.%(ext)s")
        cmd = cmd_prefix + [
            "--skip-download",
            "--write-subs",
            "--write-auto-subs",
            "--sub-langs", f"{lang}.*,{lang},en.*,en",
            "--sub-format", "json3/vtt/best",
            "-o", out_tmpl,
            url,
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            raise RuntimeError(
                "yt-dlp failed to fetch subtitles:\n" + (proc.stderr or proc.stdout)
            )
        files = sorted(os.listdir(tmp))
        sub_files = [f for f in files if f.endswith((".json3", ".vtt"))]
        if not sub_files:
            raise RuntimeError(
                f"No captions available for {video_id} via yt-dlp."
            )
        # Prefer the requested language, then json3 (has timing), then anything.
        sub_files.sort(key=lambda f: (lang not in f, not f.endswith(".json3")))
        chosen = sub_files[0]
        detected_lang = chosen.split(".")[-2] if chosen.count(".") >= 2 else lang
        raw = open(os.path.join(tmp, chosen), encoding="utf-8").read()
        segments = _parse_json3(raw) if chosen.endswith(".json3") else _parse_vtt(raw)
    if not segments:
        raise RuntimeError(f"Captions for {video_id} parsed to empty transcript.")
    return {
        "video_id": video_id,
        "language": detected_lang,
        "source": "yt-dlp",
        "transcript": segments,
    }


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("video", help="YouTube URL, short URL, shorts URL, or 11-char ID")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--lang", default="en", help="preferred caption language (default: en)")
    parser.add_argument("--no-timestamps", dest="timestamps", action="store_false",
                        help="omit [HH:MM:SS] prefixes in --format text")
    parser.add_argument("--no-api", action="store_true",
                        help="skip TranscriptAPI even if a key is set; use yt-dlp directly")
    parser.add_argument("--no-install", dest="auto_install", action="store_false",
                        help="do not auto-install yt-dlp if it is missing")
    args = parser.parse_args(argv)

    try:
        video_id = extract_video_id(args.video)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    result = None
    key = os.environ.get("TRANSCRIPT_API_KEY")
    if key and not args.no_api:
        result = try_api(video_id, key, args.lang)

    if result is None:
        try:
            result = try_ytdlp(video_id, args.lang, args.auto_install)
        except Exception as exc:  # noqa: BLE001
            print(f"error: {exc}", file=sys.stderr)
            return 1

    print(render(result, args.format, args.timestamps))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
