"""Offline tests for the standalone text corrector used by reconstruct-transcript.

Verifies it reuses the canonical corrections.json glossary and applies
whole-word fixes. Run with: python3 -m unittest discover -s tests
"""

import importlib.util
import pathlib
import unittest

_SCRIPT = (
    pathlib.Path(__file__).resolve().parent.parent
    / ".claude" / "skills" / "reconstruct-transcript" / "scripts" / "correct_text.py"
)
_spec = importlib.util.spec_from_file_location("correct_text", _SCRIPT)
ct = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ct)


class TestCorrectText(unittest.TestCase):
    def test_resolves_canonical_glossary(self):
        gloss, src = ct.load_glossary(None)
        self.assertTrue(src and src.endswith("corrections.json"))
        self.assertEqual(gloss.get("rorwaz"), "ROAS")
        self.assertNotIn("_comment", gloss)

    def test_applies_fixes_whole_word(self):
        gloss = {"rorwaz": "ROAS", "vssl": "VSL"}
        out, counts = ct.apply_corrections("our rorwaz on VSSL ads", gloss)
        self.assertEqual(out, "our ROAS on VSL ads")
        self.assertEqual(counts, {"ROAS": 1, "VSL": 1})

    def test_substring_safe(self):
        out, counts = ct.apply_corrections("a broast", {"roas": "ROAS"})
        self.assertEqual(out, "a broast")
        self.assertEqual(counts, {})

    def test_empty_glossary_noop(self):
        out, counts = ct.apply_corrections("unchanged", {})
        self.assertEqual(out, "unchanged")
        self.assertEqual(counts, {})


if __name__ == "__main__":
    unittest.main()
