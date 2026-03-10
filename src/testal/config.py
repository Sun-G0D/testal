"""Configuration loading with precedence:
defaults --> .testal.yml --> env vars --> CLI flags."""

from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class TestalConfig:
    """Resolved configuration for a Testal run."""

    model: str = "gpt-4o-mini"
    output_dir: str = "tests/"
    test_style: str = "pytest"  # future: unittest support
    exclude_patterns: list[str] = field(
        default_factory=lambda: ["__pycache__", ".venv", "migrations"]
    )
    commit_format: str = "conventional"  # conventional | simple
    max_retries: int = 3


def load_config(config_path: Path | None = None) -> TestalConfig:
    """Load config from .testal.yml if it exists, with defaults as fallback."""
    defaults = TestalConfig()

    search_path = config_path or Path.cwd() / ".testal.yml"
    if not search_path.exists():
        return defaults

    raw = yaml.safe_load(search_path.read_text()) or {}

    return TestalConfig(
        model=raw.get("model", defaults.model),
        output_dir=raw.get("output_dir", defaults.output_dir),
        test_style=raw.get("test_style", defaults.test_style),
        exclude_patterns=raw.get("exclude_patterns", defaults.exclude_patterns),
        commit_format=raw.get("commit_format", defaults.commit_format),
        max_retries=raw.get("max_retries", defaults.max_retries),
    )
