"""Offline tests for screenwatch-kit/scripts/aggregate.py.

Covers the pure aggregation logic: activity blocks, per-app time, context
switches, churn bursts, revisit (polling) detection, and frame selection. No
network, no filesystem capture — just synthetic tick sequences.

Also asserts the kit's canonical copy and the skill-bundled copy stay
byte-identical (they're distributed through two channels; drift would be a bug).

Run with: python3 -m unittest discover -s tests
"""

import importlib.util
import pathlib
import unittest

_ROOT = pathlib.Path(__file__).resolve().parent.parent
_KIT = _ROOT / "screenwatch-kit" / "scripts" / "aggregate.py"
_SKILL = _ROOT / ".claude" / "skills" / "screenwatch" / "scripts" / "aggregate.py"

_spec = importlib.util.spec_from_file_location("swagg", _KIT)
agg = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(agg)


def _tick(epoch, app, window="", url="", img=False):
    # t is HH-MM-SS derived from epoch offset for realistic, sortable stamps.
    h = (epoch // 3600) % 24
    m = (epoch // 60) % 60
    s = epoch % 60
    return {
        "t": f"{h:02d}-{m:02d}-{s:02d}",
        "epoch": epoch,
        "app": app,
        "window": window,
        "url": url,
        "img": img,
    }


def _run(apps, start=0, interval=5, img_every=6):
    """Build a tick stream from a flat list of app (or (app,window,url)) values.

    ``img_every=None`` means no tick saves an image.
    """
    events = []
    for i, spec in enumerate(apps):
        if isinstance(spec, tuple):
            app, window, url = (list(spec) + ["", ""])[:3]
        else:
            app, window, url = spec, "", ""
        img = img_every is not None and (i % img_every == 0)
        events.append(_tick(start + i * interval, app, window, url, img=img))
    return events


class TestBlocks(unittest.TestCase):
    def test_collapses_consecutive_same_state(self):
        events = _run(["Chrome", "Chrome", "Chrome", "Slack", "Chrome"])
        blocks = agg.build_blocks(events, interval=5)
        self.assertEqual([b["app"] for b in blocks], ["Chrome", "Slack", "Chrome"])
        # First block spans 3 ticks: (10-0)+5 = 15s
        self.assertEqual(blocks[0]["duration_s"], 15)
        # Single-tick block counts as one interval.
        self.assertEqual(blocks[1]["duration_s"], 5)

    def test_window_change_splits_block(self):
        events = _run([("Chrome", "Gmail", ""), ("Chrome", "Docs", "")])
        blocks = agg.build_blocks(events, interval=5)
        self.assertEqual(len(blocks), 2)

    def test_infer_interval(self):
        events = [_tick(0, "A"), _tick(5, "A"), _tick(10, "A")]
        self.assertEqual(agg.infer_interval(events), 5)
        # Idle gaps (>30s) are ignored in the median.
        events = [_tick(0, "A"), _tick(3, "A"), _tick(600, "B"), _tick(603, "B")]
        self.assertEqual(agg.infer_interval(events), 3)


class TestSignals(unittest.TestCase):
    def test_per_app_seconds(self):
        events = _run(["Chrome", "Chrome", "Slack"])
        blocks = agg.build_blocks(events, interval=5)
        secs = agg.per_app_seconds(blocks)
        self.assertEqual(secs["Chrome"], 10)  # (5-0)+5
        self.assertEqual(secs["Slack"], 5)

    def test_context_switches_counts_app_changes_only(self):
        # Chrome window changes don't count; app changes do.
        events = _run(
            [("Chrome", "A", ""), ("Chrome", "B", ""), ("Slack", "", ""), ("Chrome", "", "")]
        )
        blocks = agg.build_blocks(events, interval=5)
        self.assertEqual(agg.context_switches(blocks), 2)  # Chrome->Slack, Slack->Chrome

    def test_revisits_detects_polling(self):
        # Chrome/gmail returned to 3 separate times, interspersed with other apps.
        seq = []
        for _ in range(3):
            seq += [("Chrome", "Gmail", "mail.google.com"), ("Slack", "", "")]
        blocks = agg.build_blocks(_run(seq), interval=5)
        rv = agg.revisits(blocks)
        self.assertEqual(rv["urls"].get("mail.google.com"), 3)
        self.assertEqual(rv["apps"].get("Chrome"), 3)

    def test_revisits_ignores_single_focus_session(self):
        # One long Chrome session = one visit, below the threshold.
        blocks = agg.build_blocks(_run(["Chrome"] * 20), interval=5)
        rv = agg.revisits(blocks)
        self.assertNotIn("Chrome", rv["apps"])

    def test_churn_burst_detected(self):
        # 10 rapid alternations at 5s spacing => >6 switches within 120s.
        apps = ["A", "B"] * 6
        bursts = agg.churn_bursts(_run(apps), window_s=120, threshold=6)
        self.assertTrue(bursts)
        self.assertGreater(bursts[0]["switches"], 6)

    def test_no_churn_when_focused(self):
        bursts = agg.churn_bursts(_run(["A"] * 30), window_s=120, threshold=6)
        self.assertEqual(bursts, [])


class TestFrameSelection(unittest.TestCase):
    def test_selects_and_caps_and_orders(self):
        events = _run(["Chrome", "Slack", "Chrome", "Code", "Chrome"], img_every=1)
        blocks = agg.build_blocks(events, interval=5)
        bursts = agg.churn_bursts(events)
        frames = agg.select_frames(blocks, bursts, max_frames=30)
        self.assertTrue(frames)
        ts = [f["t"] for f in frames]
        self.assertEqual(ts, sorted(ts))  # chronological
        self.assertEqual(len(ts), len(set(ts)))  # deduped
        for f in frames:
            self.assertIn(f["reason"], {"transition", "churn", "long-block"})

    def test_respects_max_frames(self):
        events = _run([f"App{i}" for i in range(50)], img_every=1)
        blocks = agg.build_blocks(events, interval=5)
        frames = agg.select_frames(blocks, [], max_frames=10)
        self.assertLessEqual(len(frames), 10)

    def test_no_frames_when_no_images(self):
        events = _run(["Chrome", "Slack"], img_every=None)  # never img
        blocks = agg.build_blocks(events, interval=5)
        self.assertEqual(agg.select_frames(blocks, []), [])


class TestAggregate(unittest.TestCase):
    def test_end_to_end_shape(self):
        seq = []
        for _ in range(4):
            seq += [("Chrome", "Gmail", "mail.google.com"), ("Slack", "", "")]
        out = agg.aggregate(_run(seq))
        self.assertEqual(out["interval_s"], 5)
        self.assertIn("Chrome", out["per_app_seconds"])
        self.assertEqual(out["revisits"]["urls"].get("mail.google.com"), 4)
        self.assertIsInstance(out["frames_to_review"], list)
        self.assertIsInstance(out["activity_blocks"], list)
        # Report renders without error.
        self.assertIn("Screenwatch aggregate", agg.format_report(out, "2026-07-08"))

    def test_empty_log(self):
        out = agg.aggregate([])
        self.assertEqual(out["ticks"], 0)
        self.assertEqual(out["blocks"], 0)
        self.assertEqual(out["frames_to_review"], [])


class TestCopiesInSync(unittest.TestCase):
    def test_kit_and_skill_copies_identical(self):
        self.assertTrue(_SKILL.exists(), "skill copy of aggregate.py is missing")
        self.assertEqual(
            _KIT.read_bytes(),
            _SKILL.read_bytes(),
            "screenwatch-kit/scripts/aggregate.py and the skill copy have drifted",
        )


if __name__ == "__main__":
    unittest.main()
