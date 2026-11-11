"""
Unit tests for DevFlow AI reviewer module.
"""

import pytest
from devflow.reviewer import CodeReviewer


class TestCodeReviewer:
    """Tests for the CodeReviewer class."""

    def setup_method(self):
        self.reviewer = CodeReviewer()

    def test_review_diff_no_issues(self):
        """Clean diff should have no issues and score of 100."""
        diff = """+def hello_world():
+    return "Hello, World!"
"""
        result = self.reviewer.review_diff(diff)
        assert result["score"] == 100
        assert result["total_issues"] == 0

    def test_review_diff_detects_print(self):
        """Diff with print() should detect a warning."""
        diff = """+def debug_me():
+    print("debugging this value")
+    return 42
"""
        result = self.reviewer.review_diff(diff)
        assert result["total_issues"] >= 1
        assert any(i["severity"] == "warning" for i in result["issues"])

    def test_review_diff_detects_hardcoded_password(self):
        """Diff with hardcoded password should raise critical issue."""
        diff = """+password = "super_secret_123"
"""
        result = self.reviewer.review_diff(diff)
        assert result["total_issues"] >= 1
        assert any(i["severity"] == "critical" for i in result["issues"])

    def test_review_diff_detects_eval(self):
        """Diff with eval() should raise a critical issue."""
        diff = """+result = eval(user_input)
"""
        result = self.reviewer.review_diff(diff)
        assert any(i["severity"] == "critical" for i in result["issues"])

    def test_score_decreases_with_issues(self):
        """Score should decrease when issues are found."""
        clean_diff = "+x = 1 + 2\n"
        dirty_diff = '+password = "1234"\n+eval(user_input)\n'

        clean_result = self.reviewer.review_diff(clean_diff)
        dirty_result = self.reviewer.review_diff(dirty_diff)

        assert clean_result["score"] > dirty_result["score"]

    def test_score_never_negative(self):
        """Score should never go below 0."""
        many_issues = (
            '+password = "1234"\n'
            '+secret = "abc"\n'
            '+eval(x)\n'
            '+eval(y)\n'
            '+eval(z)\n'
            '+eval(a)\n'
            '+eval(b)\n'
        )
        result = self.reviewer.review_diff(many_issues)
        assert result["score"] >= 0

    def test_format_report_returns_string(self):
        """format_report should return a non-empty string."""
        diff = "+x = 1\n"
        result = self.reviewer.review_diff(diff)
        report = self.reviewer.format_report(result)
        assert isinstance(report, str)
        assert len(report) > 0
        assert "DevFlow AI" in report

    def test_ignores_removed_lines(self):
        """Lines starting with - (removed) should not be reviewed."""
        diff = '-password = "old_secret"\n+x = 1\n'
        result = self.reviewer.review_diff(diff)
        # The removed password line should not trigger an issue
        assert result["total_issues"] == 0
