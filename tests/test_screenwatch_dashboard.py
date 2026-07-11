"""Offline tests for screenwatch-kit/scripts/dashboard.py.

Covers the pure view-building and HTML rendering: duration formatting, fixed
palette-slot assignment (with 'Other' overflow), single- vs multi-day views, and
that the rendered document is self-contained, escapes untrusted text, and holds
the expected data. Also guards the kit vs skill copy against drift.

Run with: python3 -m unittest discover -s tests
"""

import importlib.util
import pathlib
import unittest

_ROOT = pathlib.Path(__file__).resolve().parent.parent
_KIT = _ROOT / "screenwatch-kit" / "scripts" / "dashboard.py"
_SKILL = _ROOT / ".claude" / "skills" / "screenwatch" / "scripts" / "dashboard.py"

_spec = importlib.util.spec_from_file_location("swdash", _KIT)
dash = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dash)


def _agg(per_app, *, tracked=None, idle=0, switches=0, blocks=None, revisits=None,
         churn=None):
    if tracked is None:
        tracked = sum(per_app.values())
    return {
        "per_app_seconds": per_app,
        "tracked_seconds": tracked,
        "idle_seconds": idle,
        "context_switches": switches,
        "activity_blocks": blocks or [],
        "revisits": revisits or {"apps": {}, "urls": {}},
        "churn_bursts": churn or [],
    }


class TestFormatting(unittest.TestCase):
    def test_fmt_dur(self):
        self.assertEqual(dash._fmt_dur(45), "45s")
        self.assertEqual(dash._fmt_dur(300), "5m")
        self.assertEqual(dash._fmt_dur(4500), "1h 15m")
        self.assertEqual(dash._fmt_dur(3600), "1h")


class TestColorAssignment(unittest.TestCase):
    def test_fixed_slots_by_rank(self):
        out = dash.assign_app_colors({"A": 10, "B": 30, "C": 20})
        self.assertEqual([(o["app"], o["slot"]) for o in out],
                         [("B", 0), ("C", 1), ("A", 2)])

    def test_overflow_folds_into_other(self):
        apps = {f"App{i}": (20 - i) for i in range(11)}  # 11 apps
        out = dash.assign_app_colors(apps)
        slots = [o["slot"] for o in out]
        self.assertEqual(slots[:8], list(range(8)))       # first 8 get slots
        self.assertEqual(out[-1]["app"], "Other")          # rest merged
        self.assertEqual(out[-1]["slot"], -1)
        # Other bucket sums the tail (apps ranked 9,10,11 -> secs 12,11,10).
        self.assertEqual(out[-1]["seconds"], 12 + 11 + 10)


class TestBuildView(unittest.TestCase):
    def test_single_day_has_timeline_and_revisits(self):
        agg = _agg(
            {"Chrome": 60, "Slack": 30},
            blocks=[{"app": "Chrome", "start_t": "09-00-00", "end_t": "09-00-55",
                     "duration_s": 60, "window": "Gmail", "url": "mail.google.com"}],
            revisits={"apps": {"Chrome": 4}, "urls": {"mail.google.com": 4}},
            churn=[{"start_epoch": 1, "end_epoch": 2, "switches": 8}],
        )
        view = dash.build_view([("2026-07-08", agg)])
        self.assertEqual(view["n_days"], 1)
        self.assertEqual(view["subtitle"], "2026-07-08")
        self.assertTrue(view["timeline"])
        self.assertEqual(view["timeline"][0]["app"], "Chrome")
        self.assertEqual(view["churn_bursts"], 1)
        labels = {c["label"] for c in view["revisits"]}
        self.assertIn("mail.google.com", labels)

    def test_multi_day_has_trend_and_merges_totals(self):
        days = [
            ("2026-07-06", _agg({"Code": 100, "Chrome": 20})),
            ("2026-07-07", _agg({"Code": 50, "Slack": 40})),
        ]
        view = dash.build_view(days)
        self.assertEqual(view["n_days"], 2)
        self.assertIn("trend", view)
        self.assertEqual(len(view["trend"]), 2)
        # Code time merged across both days: 100 + 50.
        code = next(a for a in view["apps"] if a["app"] == "Code")
        self.assertEqual(code["seconds"], 150)
        self.assertNotIn("timeline", view)


class TestRender(unittest.TestCase):
    def test_self_contained_and_has_data(self):
        agg = _agg({"Code": 3600, "Chrome": 1800})
        view = dash.build_view([("2026-07-08", agg)])
        doc = dash.render_dashboard(view)
        self.assertTrue(doc.startswith("<!doctype html>"))
        # No external resources.
        for needle in ("http://", "https://", "<script", "cdn", "src="):
            self.assertNotIn(needle, doc)
        # Theme-aware.
        self.assertIn("prefers-color-scheme:dark", doc)
        # Data present.
        self.assertIn("Code", doc)
        self.assertIn("1h", doc)          # 3600s formatted
        self.assertIn("Time per app", doc)
        self.assertIn("table", doc)       # accessibility table view

    def test_escapes_untrusted_window_titles(self):
        # A window title with HTML must not break out of an attribute/markup.
        agg = _agg(
            {"Evil": 60},
            blocks=[{"app": "Evil", "start_t": "09-00-00", "end_t": "09-00-55",
                     "duration_s": 60, "window": '<img src=x onerror=alert(1)>',
                     "url": ""}],
        )
        view = dash.build_view([("2026-07-08", agg)])
        doc = dash.render_dashboard(view)
        self.assertNotIn("<img src=x", doc)
        self.assertIn("&lt;img", doc)


class TestCopiesInSync(unittest.TestCase):
    def test_kit_and_skill_copies_identical(self):
        self.assertTrue(_SKILL.exists(), "skill copy of dashboard.py is missing")
        self.assertEqual(_KIT.read_bytes(), _SKILL.read_bytes(),
                         "dashboard.py kit and skill copies have drifted")


if __name__ == "__main__":
    unittest.main()
