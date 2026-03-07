# Testal

LLM-powered CLI tool that autonomously generates comprehensive `pytest` test suites and Conventional Commit messages from your Python source code. Designed to plug directly into CI/CD pipelines via a custom GitHub Action.

---

## Features

- **AST-Based Code Analysis** — Parses Python source at the abstract syntax tree level to extract function signatures, type hints, docstrings, and decorators for precise prompt construction.
- **Multi-Provider LLM Backend** — Supports OpenAI, Anthropic, and Google Gemini through a unified LiteLLM interface with automatic retry and provider fallback.
- **Diff-Aware Generation** — In `--diff` mode, only generates tests for functions modified in the current git diff, making CI runs fast and cost-efficient.
- **Commit Message Generation** — Reads staged changes and produces Conventional Commit–formatted messages.
- **GitHub Action** — Ships as a publishable GitHub Action for automated test generation on pull requests.
- **Configurable** — Per-repo `.testal.yml` config with full CLI flag overrides.

---

## Requirements

- Python 3.11+
- Git
- At least one LLM API key (OpenAI, Anthropic, or Google Gemini)

---

## Installation

### From Source (Development)

```bash
git clone https://github.com/YOUR_USERNAME/testal.git
cd testal
pip install -e ".[dev]"
```

This installs Testal in editable mode with all development dependencies (pytest, ruff, mypy, pre-commit).

### Verify Installation

```bash
testal --version
testal --help
```

---

## Quick Start

### Generate Tests

```bash
# Generate tests for a single file
testal generate app/utils.py

# Generate tests for an entire directory
testal generate src/

# Only generate tests for functions changed in your current diff
testal generate src/ --diff

# Use a specific model
testal generate src/ --model claude-sonnet-4-20250514

# Preview output without writing files
testal generate src/ --dry-run
```

### Generate Commit Messages

```bash
# Generate a commit message from staged changes
git add .
testal commit

# Generate and immediately apply the commit
testal commit --apply
```

---

## Configuration

Create a `.testal.yml` in your project root:

```yaml
model: gpt-4o-mini
output_dir: tests/
test_style: pytest
commit_format: conventional
max_retries: 3
exclude_patterns:
  - __pycache__
  - .venv
  - migrations
```

**Precedence order:** defaults → `.testal.yml` → environment variables → CLI flags.

---

## Environment Variables

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | API key for OpenAI models |
| `ANTHROPIC_API_KEY` | API key for Anthropic models |
| `GEMINI_API_KEY` | API key for Google Gemini models |

LiteLLM handles provider routing automatically based on the model name passed to `--model`.

---

## GitHub Action Usage

Add to your workflow (`.github/workflows/testal.yml`):

```yaml
name: Testal Test Generation

on:
  pull_request:
    branches: [main]

jobs:
  generate-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: evan-sun/testal-action@v1
        with:
          model: gpt-4o-mini
          config: .testal.yml
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

---

## Development

### Run Tests

```bash
pytest
```

### Lint and Format

```bash
ruff check src/ tests/
ruff format src/ tests/
```

### Type Check

```bash
mypy src/testal/
```

---

## Architecture

```
testal/
├── src/testal/
│   ├── cli.py                 # Click CLI entry points
│   ├── config.py              # YAML config loading + precedence
│   ├── analyzer/
│   │   ├── ast_parser.py      # AST walking, function extraction
│   │   ├── models.py          # FunctionContext dataclasses
│   │   └── diff_engine.py     # Git diff parsing, function-level filtering
│   ├── generator/
│   │   ├── prompt_builder.py  # Prompt construction from FunctionContext
│   │   ├── llm_client.py      # LiteLLM wrapper with retry/fallback
│   │   ├── test_writer.py     # Validates + writes generated test files
│   │   └── commit_writer.py   # Commit message generation + git apply
│   └── utils/
│       ├── git.py             # Git operations (diff, staged files, commit)
│       └── validation.py      # Syntax checking, import verification
├── tests/
│   ├── fixtures/              # Deterministic sample files for testing
│   └── test_*.py              # Test modules
├── .github/
│   ├── workflows/ci.yml       # CI pipeline
│   └── actions/testal-action/ # Custom GitHub Action
├── pyproject.toml
├── .testal.yml
└── README.md
```

---

## License

MIT