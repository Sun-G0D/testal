"""Testal CLI — LLM-powered test generation and commit messages."""

import click

from testal import __version__


@click.group()
@click.version_option(version=__version__, prog_name="testal")
def main() -> None:
    """LLM-powered pytest test generation and commit message tool."""


@main.command()
@click.argument("path", type=click.Path(exists=True))
@click.option("--model", default="gpt-4o-mini", help="LLM model to use for generation.")
@click.option("--output", "-o", default="tests/", help="Output directory for generated tests.")
@click.option("--diff", is_flag=True, help="Only generate tests for functions changed in git diff.")
@click.option("--diff-ref", default=None, help="Git ref range for diff (e.g. 'main..HEAD').")
@click.option("--overwrite", is_flag=True, help="Overwrite existing test files.")
@click.option("--dry-run", is_flag=True, help="Print generated tests to stdout without writing.")
@click.option("--config", type=click.Path(), default=None, help="Path to .testal.yml config file.")
def generate(
    path: str,
    model: str,
    output: str,
    diff: bool,
    diff_ref: str | None,
    overwrite: bool,
    dry_run: bool,
    config: str | None,
) -> None:
    """Generate pytest test suites for Python source files at PATH."""
    click.echo(f"Analyzing: {path}")
    click.echo(f"Model: {model}")
    if diff:
        click.echo(f"Diff mode: ON (ref: {diff_ref or 'staged'})")
    # TODO: Wire up analyzer --> generator --> writer pipeline
    click.echo("Test generation not yet implemented.")


@main.command()
@click.option("--model", default="gpt-4o-mini", help="LLM model to use.")
@click.option(
    "--apply", "apply_commit", is_flag=True, help="Directly run git commit with the message."
)
@click.option("--config", type=click.Path(), default=None, help="Path to .testal.yml config file.")
def commit(model: str, apply_commit: bool, config: str | None) -> None:
    """Generate a Conventional Commit message from staged changes."""
    click.echo(f"Model: {model}")
    # TODO: Wire up diff reader --> prompt --> commit writer
    click.echo("Commit generation not yet implemented.")
