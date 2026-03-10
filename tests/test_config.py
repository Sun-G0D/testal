"""Tests for the config module."""

from testal.config import TestalConfig, load_config


class TestLoadConfig:
    def test_returns_defaults_when_no_file(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        config = load_config()
        assert config.model == "gpt-4o-mini"
        assert config.output_dir == "tests/"

    def test_loads_from_yaml(self, tmp_path):
        cfg_file = tmp_path / ".testal.yml"
        cfg_file.write_text("model: claude-sonnet-4-20250514\nmax_retries: 5\n")
        config = load_config(cfg_file)
        assert config.model == "claude-sonnet-4-20250514"
        assert config.max_retries == 5

    def test_yaml_partial_override(self, tmp_path):
        cfg_file = tmp_path / ".testal.yml"
        cfg_file.write_text("model: gpt-4o\n")
        config = load_config(cfg_file)
        assert config.model == "gpt-4o"
        assert config.output_dir == "tests/"  # default preserved

    def test_empty_yaml_returns_defaults(self, tmp_path):
        cfg_file = tmp_path / ".testal.yml"
        cfg_file.write_text("")
        config = load_config(cfg_file)
        assert config == TestalConfig()
