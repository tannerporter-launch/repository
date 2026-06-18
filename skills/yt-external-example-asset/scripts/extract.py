#!/usr/bin/env python3
"""
extract.py

Worker 1 extractor for the yt-reference-pipeline.

Takes a single YouTube URL and produces a JSON payload containing:
- title
- full description (raw text, links preserved)
- uploader, channel, upload date, duration, view count, tags, chapters
- every link found in the description
- the full transcript as both clean text and timestamped segments

Extraction strategy (documented choice):
- Primary path is yt-dlp. It returns the richest metadata (title, full
  description, chapters, tags) in one call and exposes both manual and
  automatic caption tracks. This is the most reliable free local method
  because it follows the same routes the site itself uses.
- Transcript fallback is youtube-transcript-api. It is used only when
  yt-dlp returns no usable caption track, because it covers some videos
  where yt-dlp caption URLs are throttled.

The script never downloads media. It only pulls metadata and caption text,
so ffmpeg is not required.

Usage:
    python3 extract.py "https://www.youtube.com/watch?v=VIDEO_ID" --out payload.json
    python3 extract.py "https://youtu.be/VIDEO_ID"   # prints JSON to stdout

Exit codes:
    0 success
    2 could not extract metadata (hard failure)
    3 metadata ok but no transcript by any method (soft, payload still written)
"""

import argparse
import json
import os
import re
import sys
import urllib.request

# URL pattern used for description and transcript link harvesting.
URL_RE = re.compile(r"https?://[^\s)\]<>\"']+")

# yt-dlp player clients tried in order. Different clients survive different
# blocks, so the extractor walks the list until one returns a player response.
PLAYER_CLIENTS = [None, ["android"], ["ios"], ["tv"], ["mweb"], ["web_safari"]]


def log(msg):
    """Write progress to stderr so stdout stays pure JSON."""
    print(f"[extract] {msg}", file=sys.stderr, flush=True)


def trust_system_ca():
    """Make certifi consumers trust the active system CA bundle.

    Some environments route traffic through a TLS-inspecting proxy whose CA
    lives in the system store but not in certifi's vendored bundle. Pointing
    certifi at the system bundle keeps verification ON while trusting the
    proxy chain. In a normal environment the system bundle works too, so this
    is safe everywhere.
    """
    candidates = [
        os.environ.get("YT_PIPELINE_CA_BUNDLE"),
        os.environ.get("SSL_CERT_FILE"),
        os.environ.get("REQUESTS_CA_BUNDLE"),
        "/etc/ssl/certs/ca-certificates.crt",
    ]
    bundle = next((c for c in candidates if c and os.path.exists(c)), None)
    if not bundle:
        return
    os.environ.setdefault("SSL_CERT_FILE", bundle)
    try:
        import certifi

        certifi.where = lambda: bundle  # noqa: E731
    except Exception:  # noqa: BLE001
        pass


def fetch_text(url):
    """Fetch a caption file with a browser-like agent. Returns text or None."""
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0 (compatible; yt-reference-pipeline)"}
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as exc:  # noqa: BLE001
        log(f"caption fetch failed: {exc}")
        return None


def parse_json3(raw):
    """Parse a YouTube json3 caption file into timestamped segments."""
    segments = []
    try:
        data = json.loads(raw)
    except Exception:  # noqa: BLE001
        return segments
    for event in data.get("events", []):
        segs = event.get("segs")
        if not segs:
            continue
        text = "".join(s.get("utf8", "") for s in segs).strip()
        if not text:
            continue
        start_ms = event.get("tStartMs", 0)
        segments.append({"start": round(start_ms / 1000.0, 2), "text": text})
    return segments


def parse_vtt(raw):
    """Parse a WebVTT caption file into timestamped segments."""
    segments = []
    cue_time = None
    buffer = []
    time_re = re.compile(r"(\d{2}:\d{2}:\d{2}\.\d{3})\s+-->")

    def flush():
        if cue_time is not None and buffer:
            text = " ".join(buffer).strip()
            text = re.sub(r"<[^>]+>", "", text)  # strip inline timing tags
            if text:
                segments.append({"start": cue_time, "text": text})

    def to_seconds(stamp):
        h, m, s = stamp.split(":")
        return round(int(h) * 3600 + int(m) * 60 + float(s), 2)

    for line in raw.splitlines():
        line = line.strip()
        match = time_re.search(line)
        if match:
            flush()
            cue_time = to_seconds(match.group(1))
            buffer = []
        elif line and not line.startswith(("WEBVTT", "Kind:", "Language:", "NOTE")):
            buffer.append(line)
    flush()
    # Collapse consecutive duplicate lines that auto-captions repeat.
    deduped = []
    for seg in segments:
        if deduped and deduped[-1]["text"] == seg["text"]:
            continue
        deduped.append(seg)
    return deduped


def pick_caption_track(info):
    """Choose the best English caption track from a yt-dlp info dict.

    Prefers a manual track over an automatic one, and a json3 format over vtt.
    Returns (segments, kind) or (None, None).
    """
    manual = info.get("subtitles") or {}
    auto = info.get("automatic_captions") or {}

    def lang_keys(table):
        return [k for k in table if k.lower().startswith("en")]

    for table, kind in ((manual, "manual"), (auto, "automatic")):
        for key in lang_keys(table):
            formats = table[key]
            ordered = sorted(
                formats,
                key=lambda f: 0 if f.get("ext") == "json3" else 1,
            )
            for fmt in ordered:
                raw = fetch_text(fmt.get("url", ""))
                if not raw:
                    continue
                if fmt.get("ext") == "json3":
                    segs = parse_json3(raw)
                else:
                    segs = parse_vtt(raw)
                if segs:
                    log(f"transcript via yt-dlp {kind} track ({key}, {fmt.get('ext')})")
                    return segs, kind
    return None, None


def transcript_api_fallback(video_id):
    """Last-resort transcript using youtube-transcript-api.

    Handles both the modern instance API (fetch) and the legacy classmethod
    (get_transcript) so the script works across library versions.
    """
    if not video_id:
        return None, None
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except Exception as exc:  # noqa: BLE001
        log(f"youtube-transcript-api unavailable: {exc}")
        return None, None
    rows = None
    # Modern instance API.
    try:
        fetched = YouTubeTranscriptApi().fetch(video_id)
        rows = fetched.to_raw_data() if hasattr(fetched, "to_raw_data") else list(fetched)
    except Exception as exc:  # noqa: BLE001
        log(f"transcript-api fetch() failed: {str(exc)[:120]}")
    # Legacy classmethod API.
    if rows is None and hasattr(YouTubeTranscriptApi, "get_transcript"):
        try:
            rows = YouTubeTranscriptApi.get_transcript(video_id)
        except Exception as exc:  # noqa: BLE001
            log(f"transcript-api get_transcript() failed: {str(exc)[:120]}")
    if not rows:
        return None, None
    segs = [
        {"start": round(float(r["start"]), 2), "text": r["text"].strip()}
        for r in rows
        if r.get("text", "").strip()
    ]
    if segs:
        log("transcript via youtube-transcript-api fallback")
        return segs, "automatic"
    return None, None


def segments_to_text(segments):
    """Join caption segments into readable paragraphs."""
    return " ".join(s["text"] for s in segments).strip()


def harvest_links(description, segments, chapters):
    """Collect unique links from the description and the transcript text."""
    found = []
    seen = set()

    def add(url, source):
        url = url.rstrip(".,);")
        if url not in seen:
            seen.add(url)
            found.append({"url": url, "source": source})

    for match in URL_RE.findall(description or ""):
        add(match, "description")
    transcript_text = segments_to_text(segments) if segments else ""
    for match in URL_RE.findall(transcript_text):
        add(match, "transcript")
    for chap in chapters or []:
        for match in URL_RE.findall(chap.get("title", "")):
            add(match, "chapter")
    return found


def extract_info_resilient(url):
    """Try each player client until one returns a usable info dict."""
    import yt_dlp

    last_error = None
    for clients in PLAYER_CLIENTS:
        opts = {
            "skip_download": True,
            "quiet": True,
            "no_warnings": True,
            "writesubtitles": False,
            "writeautomaticsub": False,
        }
        if clients:
            opts["extractor_args"] = {"youtube": {"player_client": clients}}
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)
            if info:
                if clients:
                    log(f"metadata via player_client={clients}")
                return info
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            log(f"player_client={clients or 'default'} failed: {str(exc)[:100]}")
    if last_error:
        raise last_error
    return None


def build_payload(url, transcript_file=None):
    """Run extraction and return the full payload dict plus a status code."""
    trust_system_ca()
    try:
        import yt_dlp  # noqa: F401
    except Exception as exc:  # noqa: BLE001
        log(f"yt-dlp import failed: {exc}")
        return None, 2

    try:
        info = extract_info_resilient(url)
    except Exception as exc:  # noqa: BLE001
        log(f"metadata extraction failed for every player client: {exc}")
        log(
            "If you are on a cloud or datacenter IP, YouTube may be blocking it. "
            "Run this skill from a residential connection, or supply cookies via "
            "yt-dlp, or pass a manual transcript with --transcript-file."
        )
        return None, 2

    segments, kind = pick_caption_track(info)
    if not segments:
        segments, kind = transcript_api_fallback(info.get("id", ""))
    if not segments and transcript_file and os.path.exists(transcript_file):
        with open(transcript_file, encoding="utf-8") as handle:
            pasted = handle.read().strip()
        if pasted:
            segments = [{"start": 0.0, "text": pasted}]
            kind = "manual"
            log(f"transcript loaded from manual file {transcript_file}")

    chapters = info.get("chapters") or []
    description = info.get("description") or ""

    payload = {
        "source_url": url,
        "video_id": info.get("id"),
        "title": info.get("title"),
        "description": description,
        "uploader": info.get("uploader"),
        "channel": info.get("channel"),
        "channel_url": info.get("channel_url"),
        "upload_date": info.get("upload_date"),
        "duration_seconds": info.get("duration"),
        "view_count": info.get("view_count"),
        "like_count": info.get("like_count"),
        "tags": info.get("tags") or [],
        "categories": info.get("categories") or [],
        "chapters": [
            {"title": c.get("title"), "start": c.get("start_time")} for c in chapters
        ],
        "thumbnail": info.get("thumbnail"),
        "webpage_url": info.get("webpage_url"),
        "transcript_kind": kind,
        "transcript_available": bool(segments),
        "transcript_segments": segments or [],
        "transcript_text": segments_to_text(segments) if segments else "",
        "links": harvest_links(description, segments, chapters),
    }
    status = 0 if segments else 3
    return payload, status


def main():
    parser = argparse.ArgumentParser(description="Extract YouTube reference payload.")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("--out", help="Write JSON to this path instead of stdout")
    parser.add_argument(
        "--transcript-file",
        help="Optional path to a manually pasted transcript, used only if "
        "automatic transcript extraction returns nothing.",
    )
    args = parser.parse_args()

    payload, status = build_payload(args.url, transcript_file=args.transcript_file)
    if payload is None:
        log("hard failure: no metadata, nothing written")
        sys.exit(status)

    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write(text)
        log(f"payload written to {args.out}")
    else:
        print(text)

    if status == 3:
        log("metadata ok but no transcript was available by any method")
    sys.exit(status)


if __name__ == "__main__":
    main()
