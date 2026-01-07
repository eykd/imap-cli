# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

imap-cli is a command line interface and Python API for interacting with IMAP email accounts. It provides commands for listing, searching, reading, flagging, copying, and deleting emails.

## Common Commands

```bash
# Install dependencies
pip install -r requirements.txt -r test-requirements.txt

# Run all tests with tox (includes py2, py3, pep8, docs)
tox

# Run tests for a specific environment
tox -e py3
tox -e pep8

# Run tests directly with nose (with coverage)
coverage run $(which nosetests) -v
coverage report --fail-under=90 --include=*imap_cli* --omit=*tests*

# Run a single test file
nosetests imap_cli/tests/test_config.py -v

# Run a single test method
nosetests imap_cli/tests/test_config.py:ConfigTest.test_default_config -v

# Lint with flake8
flake8

# Build documentation
cd docs && sphinx-build -W . _build/html
```

## Architecture

### CLI Entry Points

- `imapcli` - Bash wrapper script that dispatches to subcommands
- Subcommands map to individual Python modules via setup.py entry_points:
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

- Follow PEP8 (enforced via flake8/hacking)
- Coverage requirement: 90% minimum (excluding tests)

## Active Technologies
- Python 3.10+ (minimum 3.10, tested on 3.10, 3.11, 3.12) + docopts (CLI argument parsing), existing stdlib dependencies (001-python3-modernize-tooling)
- N/A (CLI tool, no persistent storage) (001-python3-modernize-tooling)

## Recent Changes
- 001-python3-modernize-tooling: Added Python 3.10+ (minimum 3.10, tested on 3.10, 3.11, 3.12) + docopts (CLI argument parsing), existing stdlib dependencies
