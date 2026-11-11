"""
GitHub API integration for DevFlow AI.
Handles PR comments, issue creation, and repo interactions.
"""

import os
from typing import Optional


class GitHubClient:
    """
    Wrapper around the GitHub API for DevFlow AI operations.
    """

    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.base_url = "https://api.github.com"
        self._headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def get_pr_diff(self, owner: str, repo: str, pr_number: int) -> str:
        """
        Fetch the diff of a Pull Request.

        Args:
            owner: Repository owner username.
            repo: Repository name.
            pr_number: Pull Request number.

        Returns:
            The raw diff string.
        """
        try:
            import requests
            url = f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}"
            headers = {**self._headers, "Accept": "application/vnd.github.diff"}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.text
        except Exception as e:
            return f"Error fetching PR diff: {e}"

    def post_review_comment(
        self,
        owner: str,
        repo: str,
        pr_number: int,
        body: str,
    ) -> bool:
        """
        Post a review comment on a Pull Request.

        Args:
            owner: Repository owner username.
            repo: Repository name.
            pr_number: Pull Request number.
            body: Markdown body of the comment.

        Returns:
            True if successful, False otherwise.
        """
        try:
            import requests
            url = f"{self.base_url}/repos/{owner}/{repo}/issues/{pr_number}/comments"
            payload = {"body": body}
            response = requests.post(url, headers=self._headers, json=payload)
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Error posting comment: {e}")
            return False

    def get_repo_info(self, owner: str, repo: str) -> dict:
        """
        Get basic repository information.

        Args:
            owner: Repository owner username.
            repo: Repository name.

        Returns:
            dict with repo details.
        """
        try:
            import requests
            url = f"{self.base_url}/repos/{owner}/{repo}"
            response = requests.get(url, headers=self._headers)
            response.raise_for_status()
            data = response.json()
            return {
                "name": data.get("name"),
                "description": data.get("description"),
                "stars": data.get("stargazers_count"),
                "language": data.get("language"),
                "open_issues": data.get("open_issues_count"),
            }
        except Exception as e:
            return {"error": str(e)}
