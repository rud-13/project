"""
Core AI code review logic for DevFlow AI.
"""

import os
import json
from typing import Optional


class CodeReviewer:
    """
    AI-powered code reviewer that analyzes diffs and provides feedback.
    """

    REVIEW_RULES = [
        {"pattern": "TODO", "severity": "info", "message": "Found a TODO comment — consider resolving before merging."},
        {"pattern": "print(", "severity": "warning", "message": "Debug print statement detected. Remove before production."},
        {"pattern": "password", "severity": "critical", "message": "Possible hardcoded password detected! Use environment variables."},
        {"pattern": "secret", "severity": "critical", "message": "Possible hardcoded secret detected! Use environment variables."},
        {"pattern": "except:", "severity": "warning", "message": "Bare except clause catches all exceptions. Be more specific."},
        {"pattern": "eval(", "severity": "critical", "message": "Use of eval() is dangerous. Avoid if possible."},
        {"pattern": "time.sleep", "severity": "info", "message": "Blocking sleep detected. Consider async alternatives."},
    ]

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

    def review_diff(self, diff_text: str) -> dict:
        """
        Review a git diff and return structured feedback.

        Args:
            diff_text: The git diff string to review.

        Returns:
            dict with 'summary', 'issues', and 'score'.
        """
        issues = []
        lines = diff_text.split("\n")

        for line_num, line in enumerate(lines, 1):
            # Only review added lines (lines starting with +)
            if line.startswith("+") and not line.startswith("+++"):
                code_line = line[1:]  # Remove the leading +
                for rule in self.REVIEW_RULES:
                    if rule["pattern"].lower() in code_line.lower():
                        issues.append({
                            "line": line_num,
                            "severity": rule["severity"],
                            "message": rule["message"],
                            "code": code_line.strip(),
                        })

        score = self._calculate_score(issues)
        summary = self._generate_summary(issues, score)

        return {
            "summary": summary,
            "issues": issues,
            "score": score,
            "total_issues": len(issues),
        }

    def review_file(self, filepath: str) -> dict:
        """
        Review a single source file.

        Args:
            filepath: Path to the file to review.

        Returns:
            dict with review results.
        """
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except FileNotFoundError:
            return {"error": f"File not found: {filepath}"}
        except Exception as e:
            return {"error": str(e)}

        # Convert file content to a fake diff for reuse
        fake_diff = "\n".join(f"+{line}" for line in content.split("\n"))
        return self.review_diff(fake_diff)

    def _calculate_score(self, issues: list) -> int:
        """Calculate a code quality score from 0-100."""
        deductions = {
            "critical": 20,
            "warning": 10,
            "info": 2,
        }
        score = 100
        for issue in issues:
            score -= deductions.get(issue["severity"], 5)
        return max(0, score)

    def _generate_summary(self, issues: list, score: int) -> str:
        """Generate a human-readable summary."""
        critical = sum(1 for i in issues if i["severity"] == "critical")
        warnings = sum(1 for i in issues if i["severity"] == "warning")
        infos = sum(1 for i in issues if i["severity"] == "info")

        if score >= 90:
            rating = "✅ Excellent"
        elif score >= 70:
            rating = "🟡 Good"
        elif score >= 50:
            rating = "🟠 Needs Improvement"
        else:
            rating = "🔴 Poor"

        return (
            f"{rating} — Score: {score}/100\n"
            f"Found {critical} critical issue(s), {warnings} warning(s), {infos} info notice(s)."
        )

    def format_report(self, review_result: dict) -> str:
        """Format the review result as a Markdown report."""
        lines = [
            "# 🤖 DevFlow AI — Code Review Report",
            "",
            f"## Summary",
            review_result.get("summary", "No summary available."),
            "",
            f"**Total Issues:** {review_result.get('total_issues', 0)}",
            "",
            "## Issues Found",
            "",
        ]

        issues = review_result.get("issues", [])
        if not issues:
            lines.append("🎉 No issues found! Great work.")
        else:
            for issue in issues:
                severity_emoji = {
                    "critical": "🔴",
                    "warning": "🟡",
                    "info": "🔵",
                }.get(issue["severity"], "⚪")

                lines.extend([
                    f"### {severity_emoji} Line {issue['line']} — {issue['severity'].upper()}",
                    f"**Message:** {issue['message']}",
                    f"```",
                    issue["code"],
                    "```",
                    "",
                ])

        lines.extend([
            "---",
            "*Generated by [DevFlow AI](https://github.com/rud-13/project)*",
        ])

        return "\n".join(lines)
