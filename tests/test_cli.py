"""Tests for the CLI entry points."""

from click.testing import CliRunner
from testal.cli import main


class TestCLI:
    def test_help(self):
        result = CliRunner().invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "LLM-powered" in result.output

    def test_version(self):
        result = CliRunner().invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output

    def test_generate_help(self):
        result = CliRunner().invoke(main, ["generate", "--help"])
        assert result.exit_code == 0
        assert "--model" in result.output

    def test_commit_help(self):
        result = CliRunner().invoke(main, ["commit", "--help"])
        assert result.exit_code == 0
        assert "--apply" in result.output
