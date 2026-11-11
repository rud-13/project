"""
CLI entry point for DevFlow AI.
"""

import sys
import click
from devflow.reviewer import CodeReviewer
from devflow.changelog import ChangelogGenerator
from devflow.analyzer import CodeAnalyzer


@click.group()
@click.version_option(version="1.0.0", prog_name="DevFlow AI")
def main():
    """🤖 DevFlow AI — AI-Powered Code Review & PR Assistant"""
    pass


@main.command()
@click.option("--diff", "-d", type=click.Path(exists=True), help="Path to a git diff file")
@click.option("--file", "-f", type=click.Path(exists=True), help="Path to a source file to review")
@click.option("--output", "-o", type=click.Path(), help="Save report to file")
def review(diff, file, output):
    """Review code from a diff or file and generate an AI report."""
    reviewer = CodeReviewer()

    if not diff and not file:
        click.echo("❌ Please provide --diff or --file. Use --help for usage.", err=True)
        sys.exit(1)

    if diff:
        with open(diff, "r", encoding="utf-8") as f:
            diff_text = f.read()
        result = reviewer.review_diff(diff_text)
    else:
        result = reviewer.review_file(file)

    report = reviewer.format_report(result)

    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(report)
        click.echo(f"✅ Report saved to {output}")
    else:
        click.echo(report)


@main.command()
@click.option("--from", "from_ref", default="HEAD~10", help="Starting git ref (default: HEAD~10)")
@click.option("--to", "to_ref", default="HEAD", help="Ending git ref (default: HEAD)")
@click.option("--version", "-v", default="Unreleased", help="Version label")
@click.option("--output", "-o", default="CHANGELOG.md", help="Output file (default: CHANGELOG.md)")
def changelog(from_ref, to_ref, version, output):
    """Generate a changelog from git commit history."""
    generator = ChangelogGenerator()
    content = generator.generate(version=version, from_ref=from_ref, to_ref=to_ref)
    generator.save(content, output)
    click.echo(content)


@main.command()
@click.argument("path", type=click.Path(exists=True))
@click.option("--output", "-o", type=click.Path(), help="Save report to file")
def analyze(path, output):
    """Analyze code quality of a file or directory."""
    analyzer = CodeAnalyzer()

    import os
    if os.path.isdir(path):
        results = analyzer.analyze_directory(path)
        reports = [analyzer.format_report(r) for r in results]
        full_report = "\n\n---\n\n".join(reports)
    else:
        result = analyzer.analyze_python(path)
        full_report = analyzer.format_report(result)

    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(full_report)
        click.echo(f"✅ Report saved to {output}")
    else:
        click.echo(full_report)


if __name__ == "__main__":
    main()
