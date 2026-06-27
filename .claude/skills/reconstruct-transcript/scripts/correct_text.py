#!/usr/bin/env python3
"""Apply the remembered transcription glossary to an arbitrary text file.

Deterministic, whole-word, case-insensitive term fixes — the SAME glossary the
`youtube` fetch script uses (corrections.json) — so remembered fixes also apply
to pasted transcripts, not just freshly fetched ones.

Usage:
  python3 correct_text.py transcript.txt                 # corrected text to stdout
  python3 correct_text.py transcript.txt --glossary x.json
  cat transcript.txt | python3 correct_text.py -         # read from stdin

A "[corrections] N fix(es) …" summary is written to stderr. Requires Python 3.9+.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

# Where to look for the shared glossary, in order, when --glossary is not given.
_HERE = os.path.dirname(__file__)
GLOSSARY_CANDIDATES = [
    os.path.join(_HERE, os.pardir, "corrections.json"),                  # own skill
    os.path.join(_HERE, os.pardir, os.pardir, "youtube", "corrections.json"),  # canonical
]


def load_glossary(path: str | None):
    """Return (glossary dict, source path). Empty dict if none found/parseable."""
    candidates = [path] if path else GLOSSARY_CANDIDATES
    for cand in candidates:
        if not cand or not os.path.exists(cand):
            continue
        try:
            with open(cand, encoding="utf-8") as fh:
                data = json.load(fh)
        except (OSError, ValueError):
            continue
        if isinstance(data, dict) and "corrections" in data:
            data = data["corrections"]
        if isinstance(data, dict):
            gloss = {str(k): str(v) for k, v in data.items()
                     if not str(k).startswith("_")}
            return gloss, cand
    return {}, None


def apply_corrections(text: str, glossary: dict):
    """Whole-word, case-insensitive replacement. Returns (text, {term: count})."""
    if not glossary:
        return text, {}
    repl = {k.lower(): v for k, v in glossary.items()}
    keys = sorted(glossary, key=len, reverse=True)  # multi-word phrases win
    pattern = re.compile(r"\b(" + "|".join(re.escape(k) for k in keys) + r")\b",
                         re.IGNORECASE)
    counts: dict = {}

    def _sub(m):
        out = repl[m.group(0).lower()]
        if out != m.group(0):
            counts[out] = counts.get(out, 0) + 1
        return out

    return pattern.sub(_sub, text), counts


def main(argv: list) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", help="text file to correct, or - for stdin")
    ap.add_argument("--glossary", metavar="FILE",
                    help="glossary JSON (default: the skill's corrections.json)")
    args = ap.parse_args(argv)

    try:
        text = sys.stdin.read() if args.file == "-" else \
            open(args.file, encoding="utf-8").read()
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    glossary, src = load_glossary(args.glossary)
    out, counts = apply_corrections(text, glossary)
    sys.stdout.write(out)
    if counts:
        total = sum(counts.values())
        print(f"\n[corrections] {total} fix(es) from {src}: "
              + ", ".join(f"{k}×{v}" for k, v in sorted(counts.items())),
              file=sys.stderr)
    elif not glossary:
        print("[corrections] no glossary found; text unchanged", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
