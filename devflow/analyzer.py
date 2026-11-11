"""
Code quality analyzer for DevFlow AI.
Provides static analysis metrics for source files.
"""

import os
import ast
from typing import List, Optional


class CodeAnalyzer:
    """
    Analyzes source code files for quality metrics.
    """

    def analyze_python(self, filepath: str) -> dict:
        """
        Analyze a Python file for quality metrics.

        Args:
            filepath: Path to the Python file.

        Returns:
            dict with analysis results.
        """
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                source = f.read()
        except FileNotFoundError:
            return {"error": f"File not found: {filepath}"}

        metrics = {
            "filepath": filepath,
            "lines_of_code": 0,
            "blank_lines": 0,
            "comment_lines": 0,
            "functions": [],
            "classes": [],
            "imports": [],
            "complexity_warnings": [],
        }

        lines = source.split("\n")
        metrics["lines_of_code"] = len(lines)
        metrics["blank_lines"] = sum(1 for l in lines if l.strip() == "")
        metrics["comment_lines"] = sum(1 for l in lines if l.strip().startswith("#"))

        # Parse AST
        try:
            tree = ast.parse(source)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    metrics["functions"].append(node.name)
                    # Warn about very long functions
                    func_lines = node.end_lineno - node.lineno if hasattr(node, "end_lineno") else 0
                    if func_lines > 50:
                        metrics["complexity_warnings"].append(
                            f"Function '{node.name}' is {func_lines} lines long. Consider splitting it."
                        )
                elif isinstance(node, ast.ClassDef):
                    metrics["classes"].append(node.name)
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        metrics["imports"].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    metrics["imports"].append(node.module or "")
        except SyntaxError as e:
            metrics["syntax_error"] = str(e)

        return metrics

    def analyze_directory(self, directory: str, extension: str = ".py") -> List[dict]:
        """
        Analyze all files in a directory with the given extension.

        Args:
            directory: Path to the directory.
            extension: File extension to analyze (default: .py).

        Returns:
            List of analysis results for each file.
        """
        results = []
        for root, _, files in os.walk(directory):
            # Skip hidden dirs and common non-source dirs
            if any(part.startswith(".") or part in ("node_modules", "__pycache__", "venv")
                   for part in root.split(os.sep)):
                continue
            for filename in files:
                if filename.endswith(extension):
                    filepath = os.path.join(root, filename)
                    if extension == ".py":
                        results.append(self.analyze_python(filepath))
        return results

    def format_report(self, metrics: dict) -> str:
        """Format analysis metrics as a Markdown report."""
        lines = [
            f"# 📊 Code Analysis Report",
            f"**File:** `{metrics.get('filepath', 'Unknown')}`",
            "",
            "## Metrics",
            f"- **Total Lines:** {metrics.get('lines_of_code', 0)}",
            f"- **Blank Lines:** {metrics.get('blank_lines', 0)}",
            f"- **Comment Lines:** {metrics.get('comment_lines', 0)}",
            f"- **Functions:** {len(metrics.get('functions', []))}",
            f"- **Classes:** {len(metrics.get('classes', []))}",
            "",
        ]

        if metrics.get("functions"):
            lines.append("## Functions")
            for fn in metrics["functions"]:
                lines.append(f"- `{fn}()`")
            lines.append("")

        if metrics.get("classes"):
            lines.append("## Classes")
            for cls in metrics["classes"]:
                lines.append(f"- `{cls}`")
            lines.append("")

        warnings = metrics.get("complexity_warnings", [])
        if warnings:
            lines.append("## ⚠️ Complexity Warnings")
            for w in warnings:
                lines.append(f"- {w}")
            lines.append("")

        if metrics.get("syntax_error"):
            lines.append(f"## ❌ Syntax Error\n```\n{metrics['syntax_error']}\n```")

        return "\n".join(lines)
