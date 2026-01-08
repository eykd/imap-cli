# Quickstart: imap-cli Development (Post-Migration)

This guide describes how to set up and work with imap-cli after the Python 3 modernization.

## Prerequisites

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager

### Installing uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or via pip
pip install uv
```

## Quick Setup

```bash
# Clone the repository
git clone https://github.com/your-org/imap-cli.git
cd imap-cli

# Install dependencies and package in editable mode
uv sync

# Verify installation
uv run imap-cli-status --help
```

## Development Commands

### Running Tests

```bash
# Run all tests with coverage
uv run pytest

# Run specific test file
uv run pytest imap_cli/tests/test_config.py

# Run with verbose output
uv run pytest -v

# Run specific test method
uv run pytest imap_cli/tests/test_config.py::ConfigTest::test_default_config -v
```

### Linting

```bash
# Check for issues
uv run ruff check

# Auto-fix issues
uv run ruff check --fix

# Format code
uv run ruff format
```

### Coverage Report

```bash
# Generate coverage report
uv run pytest --cov=imap_cli --cov-report=html

# View HTML report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

### Running tox

```bash
# Run all environments
uv run tox

# Run specific environment
uv run tox -e py310
uv run tox -e lint
```

## CLI Commands

After installation, the following commands are available:

| Command | Description |
|---------|-------------|
| `imap-cli-status` | Show mailbox status summary |
| `imap-cli-list` | List emails in mailbox |
| `imap-cli-read` | Read email content |
| `imap-cli-search` | Search emails |
| `imap-cli-flag` | Flag/unflag emails |
| `imap-cli-copy` | Copy emails between folders |
| `imap-cli-delete` | Delete emails |
| `imap-api` | REST API server |
| `imap-notify` | Desktop notifications |
| `imap-shell` | Interactive shell |

## Configuration

Create a configuration file at `~/.config/imap-cli`:

```ini
[imap]
hostname = imap.example.org
username = your_username
password = your_password
ssl = True

[display]
limit = 10
format_status = {directory:>20} : {count:>5} Mails

[trash]
trash_directory = Trash
```

See `config-example.ini` for all available options.

## Project Structure

```
imap-cli/
├── pyproject.toml        # Build config, dependencies, tool settings
├── tox.ini               # Multi-version testing
├── imap_cli/             # Main package
│   ├── __init__.py       # Core IMAP functions
│   ├── config.py         # Configuration loading
│   ├── *.py              # CLI modules
│   ├── scripts/          # Additional scripts
│   └── tests/            # Test suite
├── docs/                 # Sphinx documentation
└── examples/             # Example scripts
```

## Migrating from Previous Setup

If you had the project installed with the old setup.py:

```bash
# Remove old installation
pip uninstall Imap-CLI

# Clean up old virtualenv (optional)
rm -rf .venv venv

# Fresh install with uv
uv sync
```

## Troubleshooting

### "command not found: uv"
Install uv following the instructions above, then restart your shell.

### Tests fail with import errors
Ensure you ran `uv sync` to install all dependencies.

### Coverage below 90%
Check which lines are missing coverage:
```bash
uv run pytest --cov=imap_cli --cov-report=term-missing
```

### Ruff finds issues
Run `uv run ruff check --fix` to auto-fix common issues.
