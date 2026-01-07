# Migration Research: Python 3 Modernization

**Feature**: 001-python3-modernize-tooling
**Date**: 2026-01-07

## Python 2 Compatibility Code Analysis

### Files Using `six` Library

| File | Usage | Python 3 Replacement |
|------|-------|---------------------|
| `imap_cli/config.py:13` | `from six.moves import configparser` | `import configparser` |
| `imap_cli/tests/test_config.py:9` | `from six.moves import configparser` | `import configparser` |
| `imap_cli/search.py:267` | `six.string_types` | `str` |
| `imap_cli/string.py:16,43` | `six.text_type` | `str` |
| `imap_cli/summary.py:55` | `six.text_type` | `str` |
| `imap_cli/scripts/imap_api.py:125` | `six.string_types` | `str` |
| `imap_cli/tests/test_fetch.py:66,70,80` | `six.string_types` | `str` |

### Files Using `future` Library

| File | Usage | Python 3 Replacement |
|------|-------|---------------------|
| `imap_cli/tests/__init__.py:7` | `from builtins import bytes` | Remove (bytes is builtin) |

### Files Using `mock` Library

| File | Usage | Python 3 Replacement |
|------|-------|---------------------|
| `imap_cli/tests/__init__.py:9` | `import mock` | `from unittest.mock import Mock` |
| `imap_cli/tests/__init__.py:26` | `mock.Mock` | `Mock` |

## Migration Replacements

### Pattern: `six.string_types`
```python
# Before (Python 2/3 compatible)
isinstance(x, six.string_types)

# After (Python 3 only)
isinstance(x, str)
```

### Pattern: `six.text_type`
```python
# Before (Python 2/3 compatible)
six.text_type(x)

# After (Python 3 only)
str(x)
```

### Pattern: `six.moves.configparser`
```python
# Before (Python 2/3 compatible)
from six.moves import configparser

# After (Python 3 only)
import configparser
```

### Pattern: `from builtins import bytes`
```python
# Before (future library for Python 2)
from builtins import bytes

# After (Python 3 only)
# Remove entirely - bytes is builtin
```

### Pattern: `import mock`
```python
# Before (external mock library)
import mock
class Foo(mock.Mock): ...

# After (stdlib unittest.mock)
from unittest.mock import Mock
class Foo(Mock): ...
```

## Dependencies Analysis

### Current Dependencies (setup.py)
```python
install_requires=[
    "docopts>=0.6",
    "mock>=1.0.1",   # REMOVE - use unittest.mock
    "future",         # REMOVE - Python 3 only
]
```

### Current Test Dependencies (test-requirements.txt)
```
tox>=2.9.1
nose>=1.3.7          # REPLACE with pytest
coverage>=4.5.1      # KEEP (used by pytest-cov)
hacking>=1.0.0       # REMOVE - use ruff
pylint>=1.8.2        # REMOVE - use ruff
```

### New Dependencies (pyproject.toml)

```toml
[project]
dependencies = [
    "docopt>=0.6.2",  # Note: docopts is deprecated, use docopt
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "ruff>=0.1.0",
    "tox>=4.0",
]
```

## Build System Decision

**Decision**: Use `hatchling` as the build backend

**Rationale**:
- Modern, fast, well-maintained
- Good defaults for Python packages
- Excellent pyproject.toml support
- No additional configuration needed for simple packages

**Alternatives Considered**:
- `setuptools`: More configuration required, legacy feel
- `flit`: Good but less flexible
- `poetry`: More opinionated, not just a build backend

## Ruff Configuration Strategy

**Decision**: Start with a permissive configuration, equivalent to flake8 defaults

**Rationale**:
- Minimize churn in initial migration
- Can tighten rules incrementally
- Focus on getting tests passing first

**Configuration**:
```toml
[tool.ruff]
line-length = 100
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "W"]  # Equivalent to flake8 defaults
ignore = ["E501"]         # Line too long (handle separately)
```

## Test Configuration

**Decision**: Use pytest with unittest-style tests

**Rationale**:
- pytest natively supports unittest.TestCase
- No test rewrites required
- Can add pytest-style tests later

**Configuration**:
```toml
[tool.pytest.ini_options]
testpaths = ["imap_cli/tests"]
addopts = "-v --cov=imap_cli --cov-report=term-missing"

[tool.coverage.run]
source = ["imap_cli"]
omit = ["imap_cli/tests/*"]

[tool.coverage.report]
fail_under = 90
```

## Unicode Literals Cleanup

The codebase uses `u''` string prefixes extensively (Python 2 unicode literals). In Python 3:
- `u''` prefixes are optional but harmless
- Can be left as-is for minimal churn
- Or removed with `pyupgrade --py310-plus`

**Decision**: Leave unicode prefixes as-is during initial migration to minimize diff size. Can clean up in a follow-up PR if desired.

## Console Scripts Mapping

All 10 console scripts from setup.py must be preserved:

```toml
[project.scripts]
imap-api = "imap_cli.scripts.imap_api:main"
imap-cli-copy = "imap_cli.copy:main"
imap-cli-delete = "imap_cli.delete:main"
imap-cli-flag = "imap_cli.flag:main"
imap-cli-list = "imap_cli.list_mail:main"
imap-cli-read = "imap_cli.fetch:main"
imap-cli-search = "imap_cli.search:main"
imap-cli-status = "imap_cli.summary:main"
imap-notify = "imap_cli.scripts.imap_notify:main"
imap-shell = "imap_cli.scripts.imap_shell:main"
```

## Summary of Changes

| Category | Files Affected | Change Type |
|----------|---------------|-------------|
| six imports | 7 files | Replace imports |
| future imports | 1 file | Remove import |
| mock imports | 1 file | Replace with unittest.mock |
| Build config | 4 files | Delete old, create new |
| Tox config | 1 file | Update environments/commands |
| Documentation | 1 file | Update CLAUDE.md |

**Total files to modify**: ~10 files
**Total lines changed**: ~50-100 lines (mostly import changes)
