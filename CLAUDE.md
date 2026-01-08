# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

imap-cli is a command line interface and Python API for interacting with IMAP email accounts. It provides commands for listing, searching, reading, flagging, copying, and deleting emails.

## Common Commands

```bash
# Install dependencies (with dev tools)
uv pip install -e ".[dev]"

# Run all tests with tox (py310, py311, py312, lint, docs)
uv run tox

# Run tests for a specific environment
uv run tox -e py311
uv run tox -e lint

# Run tests directly with pytest (with coverage)
uv run pytest --cov=imap_cli --cov-report=term-missing

# Run a single test file
uv run pytest imap_cli/tests/test_config.py -v

# Run a single test method
uv run pytest imap_cli/tests/test_config.py::ConfigTest::test_default_config -v

# Lint with ruff
uv run ruff check .

# Auto-fix lint issues
uv run ruff check --fix .

# Build documentation
cd docs && sphinx-build -W . _build/html
```

## Architecture

### CLI Entry Points

- `imapcli` - Bash wrapper script that dispatches to subcommands
- Subcommands map to individual Python modules via pyproject.toml scripts:
  - `imap-cli-status` → `imap_cli/summary.py`
  - `imap-cli-list` → `imap_cli/list_mail.py`
  - `imap-cli-search` → `imap_cli/search.py`
  - `imap-cli-read` → `imap_cli/fetch.py`
  - `imap-cli-flag` → `imap_cli/flag.py`
  - `imap-cli-copy` → `imap_cli/copy.py`
  - `imap-cli-delete` → `imap_cli/delete.py`

### Core Modules

- `imap_cli/__init__.py` - Core IMAP functions: `connect()`, `disconnect()`, `change_dir()`, `status()`, `list_dir()`
- `imap_cli/config.py` - Configuration loading from INI files or programmatic dicts
- `imap_cli/const.py` - IMAP constants (flags, ports, search criteria per RFC 3501)

### Configuration

Default config file: `~/.config/imap-cli` (INI format)

Sections:
- `[imap]` - hostname, username, password/SASL auth, ssl
- `[display]` - format_list, format_status, limit
- `[trash]` - trash_directory, delete_method

See `config-example.ini` for all options.

## Code Style

- Follow PEP8 (enforced via ruff)
- Coverage requirement: 90% minimum (excluding tests)
- Python 3.10+ required

## Active Technologies
- Python 3.10+ (minimum 3.10, tested on 3.10, 3.11, 3.12)
- docopt for CLI argument parsing
- pytest for testing, ruff for linting
- uv for package management
