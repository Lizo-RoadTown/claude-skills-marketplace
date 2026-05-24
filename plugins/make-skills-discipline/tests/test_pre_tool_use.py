"""Tests for the pre_tool_use hook's citation + dual-mode logic.

Run from the plugin root:

    python -m unittest plugins/make-skills-discipline/tests/test_pre_tool_use.py

Or via CI: see .github/workflows/validate.yml.

Tests cover the v0.1.3 fixes:

1. Citation regex accepts URLs and bare file paths (not just file:line).
2. Dual-mode trigger does NOT fire on docs/markdown files that merely
   mention the trigger keywords.
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

# Import the hook under test.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import pre_tool_use  # noqa: E402


class TestCitationDetection(unittest.TestCase):
    """has_recent_citation must accept three citation forms."""

    def _check_transcript(self, content: str) -> bool:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".jsonl", delete=False, encoding="utf-8"
        ) as tmp:
            tmp.write(content)
            path = tmp.name
        try:
            return pre_tool_use.has_recent_citation(path)
        finally:
            Path(path).unlink(missing_ok=True)

    def test_file_line_citation_accepted(self):
        """The original form: path/to/file.ext:42."""
        self.assertTrue(
            self._check_transcript("see platform/api/main.py:42 for context")
        )

    def test_url_citation_accepted(self):
        """v0.1.3: https URLs count as citations."""
        self.assertTrue(
            self._check_transcript(
                "per https://grafana.com/docs/loki/latest/ the schema is v13"
            )
        )

    def test_http_url_citation_accepted(self):
        """v0.1.3: http URLs too (not just https)."""
        self.assertTrue(
            self._check_transcript("see http://localhost:3001/dashboards")
        )

    def test_bare_file_path_with_extension_accepted(self):
        """v0.1.3: a file path with extension and a slash counts."""
        self.assertTrue(
            self._check_transcript("matches the pattern in scripts/foo.py exactly")
        )

    def test_plain_prose_not_a_citation(self):
        """No file:line, no URL, no path → no citation."""
        self.assertFalse(
            self._check_transcript("the agent should do the right thing")
        )

    def test_missing_transcript_returns_true(self):
        """Per the existing contract: can't verify → don't false-alarm."""
        self.assertTrue(pre_tool_use.has_recent_citation(""))
        self.assertTrue(
            pre_tool_use.has_recent_citation("/nonexistent/path/transcript.jsonl")
        )


class TestDualModeGating(unittest.TestCase):
    """touches_dual_mode must skip docs and convention files."""

    def test_md_file_with_trigger_keyword_skipped(self):
        """v0.1.3: a .md file mentioning AUTH_SECRET is not a boundary change."""
        self.assertFalse(
            pre_tool_use.touches_dual_mode(
                {
                    "file_path": "docs/plans/something.md",
                    "content": "We use AUTH_SECRET for JWT signing.",
                }
            )
        )

    def test_runtime_py_file_with_trigger_keyword_fires(self):
        """Runtime edits still fire the dual-mode reminder."""
        self.assertTrue(
            pre_tool_use.touches_dual_mode(
                {
                    "file_path": "platform/api/auth.py",
                    "content": "secret = os.environ['AUTH_SECRET']",
                }
            )
        )

    def test_changelog_with_trigger_keyword_skipped(self):
        """CHANGELOG.md mentioning AUTH_SECRET is documentation, not boundary."""
        self.assertFalse(
            pre_tool_use.touches_dual_mode(
                {
                    "file_path": "CHANGELOG.md",
                    "content": "- Added AUTH_SECRET gating",
                }
            )
        )

    def test_readme_skipped(self):
        """Top-level README is documentation."""
        self.assertFalse(
            pre_tool_use.touches_dual_mode(
                {
                    "file_path": "README.md",
                    "content": "Set AUTH_SECRET in your env",
                }
            )
        )

    def test_nested_docs_path_skipped(self):
        """Nested docs paths also skip — not just top-level docs/."""
        self.assertFalse(
            pre_tool_use.touches_dual_mode(
                {
                    "file_path": "platform/api/docs/internal.md",
                    "content": "JWTTenantResolver behavior",
                }
            )
        )

    def test_runtime_ts_file_fires(self):
        """Web runtime edits still fire."""
        self.assertTrue(
            pre_tool_use.touches_dual_mode(
                {
                    "file_path": "web/lib/auth.ts",
                    "content": "tenant_id check",
                }
            )
        )

    def test_no_trigger_keyword_no_fire(self):
        """Runtime edit with no trigger keyword → no fire."""
        self.assertFalse(
            pre_tool_use.touches_dual_mode(
                {
                    "file_path": "platform/api/main.py",
                    "content": "print('hello')",
                }
            )
        )

    def test_empty_target_falls_back_to_keyword_check(self):
        """If no file_path provided, behave like v0.1.2: check the blob."""
        # No file_path → _target_is_docs returns False → keyword check runs.
        self.assertTrue(
            pre_tool_use.touches_dual_mode({"content": "AUTH_SECRET"})
        )


if __name__ == "__main__":
    unittest.main()
