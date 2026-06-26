"""Offline unit tests for the YouTube transcript fallback script.

No network required — they exercise URL parsing, caption parsing (json3 + VTT),
metadata-aware rendering, and file output. Run with:

    python3 -m unittest discover -s tests
"""

import importlib.util
import json
import os
import pathlib
import tempfile
import unittest

# Import the script as a module from its bundled location in the skill.
_SCRIPT = (
    pathlib.Path(__file__).resolve().parent.parent
    / ".claude" / "skills" / "youtube" / "scripts" / "yt_transcript.py"
)
_spec = importlib.util.spec_from_file_location("yt_transcript", _SCRIPT)
ytt = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ytt)


class TestVideoIdExtraction(unittest.TestCase):
    def test_accepts_various_forms(self):
        cases = {
            "dQw4w9WgXcQ": "dQw4w9WgXcQ",
            "https://youtu.be/dQw4w9WgXcQ": "dQw4w9WgXcQ",
            "https://youtu.be/dQw4w9WgXcQ?is=abc": "dQw4w9WgXcQ",
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=10s": "dQw4w9WgXcQ",
            "https://youtube.com/shorts/abc12345678": "abc12345678",
            "https://www.youtube.com/embed/dQw4w9WgXcQ": "dQw4w9WgXcQ",
        }
        for raw, expected in cases.items():
            self.assertEqual(ytt.extract_video_id(raw), expected, raw)

    def test_rejects_garbage(self):
        with self.assertRaises(ValueError):
            ytt.extract_video_id("not a video")


class TestParsers(unittest.TestCase):
    def test_json3(self):
        raw = json.dumps({"events": [
            {"tStartMs": 1000, "dDurationMs": 2000,
             "segs": [{"utf8": "hello "}, {"utf8": "world"}]},
            {"tStartMs": 3000, "dDurationMs": 1000, "segs": [{"utf8": "\n"}]},
        ]})
        self.assertEqual(
            ytt._parse_json3(raw),
            [{"text": "hello world", "start": 1.0, "duration": 2.0}],
        )

    def test_vtt_strips_tags_and_dedupes_rolling_lines(self):
        vtt = (
            "WEBVTT\n\n"
            "00:00:01.000 --> 00:00:03.000\nHello world\n\n"
            "00:00:03.000 --> 00:00:05.000\nHello world\n\n"
            "00:00:05.000 --> 00:00:07.000\n<c>Next</c> line\n"
        )
        self.assertEqual(ytt._parse_vtt(vtt), [
            {"text": "Hello world", "start": 1.0, "duration": 2.0},
            {"text": "Next line", "start": 5.0, "duration": 2.0},
        ])


class TestRender(unittest.TestCase):
    result = {
        "video_id": "x", "language": "en", "source": "yt-dlp",
        "title": "My Title", "description": "A desc", "channel": "Chan",
        "transcript": [{"text": "line one", "start": 1.0, "duration": 2.0}],
    }

    def test_json_includes_metadata(self):
        out = json.loads(ytt.render(self.result, "json", True))
        self.assertEqual(out["title"], "My Title")
        self.assertEqual(out["description"], "A desc")
        self.assertEqual(out["channel"], "Chan")

    def test_text_has_header_and_timestamp(self):
        txt = ytt.render(self.result, "text", True)
        self.assertIn("# My Title", txt)
        self.assertIn("## Description", txt)
        self.assertIn("[00:00:01] line one", txt)

    def test_text_clean_when_no_metadata(self):
        bare = {"video_id": "x", "language": "en", "source": "yt-dlp",
                "title": None, "description": None, "channel": None,
                "transcript": [{"text": "only line", "start": 0.0, "duration": 1.0}]}
        self.assertEqual(ytt.render(bare, "text", False), "only line")

    def test_seconds_to_hms(self):
        self.assertEqual(ytt.seconds_to_hms(3661), "01:01:01")


class TestWriteOutputs(unittest.TestCase):
    def test_writes_both_files_with_header(self):
        res = {"video_id": "abc", "language": "en", "source": "yt-dlp",
               "title": "T", "description": "D", "channel": "C",
               "transcript": [{"text": "a", "start": 1.0, "duration": 2.0},
                              {"text": "b", "start": 3.0, "duration": 1.0}]}
        with tempfile.TemporaryDirectory() as d:
            paths = ytt.write_outputs(res, d)
            self.assertEqual(len(paths), 2)
            self.assertTrue(all(os.path.exists(p) for p in paths))
            ts = pathlib.Path(paths[0]).read_text(encoding="utf-8")
            clean = pathlib.Path(paths[1]).read_text(encoding="utf-8")
            self.assertIn("Video ID: abc", ts)
            self.assertIn("[00:00:01] a", ts)
            self.assertIn("a b", clean)


if __name__ == "__main__":
    unittest.main()
