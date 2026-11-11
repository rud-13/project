"""
Automatic changelog generator from git commit history.
"""

import subprocess
from datetime import datetime
from typing import List, Optional


class ChangelogGenerator:
    """
    Generates a formatted CHANGELOG.md from git commit history.
    """

    COMMIT_TYPES = {
        "feat": "✨ New Features",
        "fix": "🐛 Bug Fixes",
        "docs": "📚 Documentation",
        "style": "💅 Code Style",
        "refactor": "♻️  Refactoring",
        "test": "✅ Tests",
        "chore": "🔧 Chores",
        "perf": "⚡ Performance",
        "ci": "👷 CI/CD",
        "build": "📦 Build",
    }

    def get_commits(self, from_ref: str = "HEAD~10", to_ref: str = "HEAD") -> List[dict]:
        """
        Get commit messages between two git refs.

        Args:
            from_ref: Starting git ref.
            to_ref: Ending git ref.

        Returns:
            List of commit dicts with 'hash', 'message', 'author', 'date'.
        """
        try:
            result = subprocess.run(
                [
                    "git", "log",
                    f"{from_ref}..{to_ref}",
                    "--pretty=format:%H|%s|%an|%ad",
                    "--date=short",
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            commits = []
            for line in result.stdout.strip().split("\n"):
                if "|" in line:
                    parts = line.split("|", 3)
                    if len(parts) == 4:
                        commits.append({
                            "hash": parts[0][:7],
                            "message": parts[1],
                            "author": parts[2],
                            "date": parts[3],
                        })
            return commits
        except subprocess.CalledProcessError:
            return []

    def categorize_commits(self, commits: List[dict]) -> dict:
        """Categorize commits by conventional commit type."""
        categorized = {label: [] for label in self.COMMIT_TYPES.values()}
        categorized["🔀 Other Changes"] = []

        for commit in commits:
            msg = commit["message"]
            categorized_flag = False
            for prefix, label in self.COMMIT_TYPES.items():
                if msg.lower().startswith(f"{prefix}:") or msg.lower().startswith(f"{prefix}("):
                    categorized[label].append(commit)
                    categorized_flag = True
                    break
            if not categorized_flag:
                categorized["🔀 Other Changes"].append(commit)

        return {k: v for k, v in categorized.items() if v}

    def generate(
        self,
        version: str = "Unreleased",
        from_ref: str = "HEAD~10",
        to_ref: str = "HEAD",
    ) -> str:
        """
        Generate a formatted changelog string.

        Args:
            version: Version label for the changelog section.
            from_ref: Starting git ref.
            to_ref: Ending git ref.

        Returns:
            Formatted Markdown changelog string.
        """
        commits = self.get_commits(from_ref, to_ref)
        if not commits:
            return f"## [{version}] — {datetime.now().strftime('%Y-%m-%d')}\n\nNo changes found.\n"

        categorized = self.categorize_commits(commits)
        today = datetime.now().strftime("%Y-%m-%d")

        lines = [f"## [{version}] — {today}", ""]
        for category, category_commits in categorized.items():
            lines.append(f"### {category}")
            for commit in category_commits:
                lines.append(
                    f"- {commit['message']} ([`{commit['hash']}`]) — {commit['author']}"
                )
            lines.append("")

        return "\n".join(lines)

    def save(self, content: str, output_path: str = "CHANGELOG.md") -> None:
        """Save changelog to a file."""
        try:
            with open(output_path, "r", encoding="utf-8") as f:
                existing = f.read()
        except FileNotFoundError:
            existing = "# Changelog\n\nAll notable changes to this project will be documented here.\n\n"

        # Insert new section after the header
        header_end = existing.find("\n\n") + 2
        new_content = existing[:header_end] + content + "\n" + existing[header_end:]

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(new_content)

        print(f"✅ Changelog saved to {output_path}")
