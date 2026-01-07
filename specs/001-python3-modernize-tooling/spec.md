# Feature Specification: Python 3 Modernization & Tooling Upgrade

**Feature Branch**: `001-python3-modernize-tooling`
**Created**: 2026-01-07
**Status**: Draft
**Input**: User description: "Let's remove Python 2.7 compatibility and go full Python 3, targeting Python 3.10 as minimum version. Priorities: 1) switch to pyproject.toml and uv 2) get tests running. The old suite uses nose as the runner and flake8 as linter, but we should switch to pytest and ruff."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Developer Runs Tests with Modern Tooling (Priority: P1)

A developer clones the repository and wants to run the test suite to verify the code works correctly. They should be able to use modern Python tooling (uv and pytest) without needing to understand or install legacy dependencies.

**Why this priority**: Running tests is the foundational developer workflow. Without working tests, no other development activities can be validated. This is the critical path for any contribution.

**Independent Test**: Can be fully tested by running `uv run pytest` from a fresh clone and verifying all tests pass with proper output.

**Acceptance Scenarios**:

1. **Given** a fresh clone of the repository, **When** a developer runs `uv sync` followed by `uv run pytest`, **Then** all tests execute successfully and output shows test results in pytest format.
2. **Given** a development environment with uv installed, **When** a developer runs pytest directly, **Then** the test suite executes with coverage reporting enabled.
3. **Given** the existing test files, **When** pytest runs, **Then** all existing unittest-style tests are discovered and executed without modification to test structure.

---

### User Story 2 - Developer Lints Code with Ruff (Priority: P2)

A developer wants to check code quality and style before committing changes. They should be able to run a modern, fast linter that catches both style issues and potential bugs.

**Why this priority**: Linting ensures code quality and consistency but is secondary to running tests. Developers need working code before worrying about style.

**Independent Test**: Can be fully tested by running `uv run ruff check .` and verifying it produces appropriate warnings/errors for code style issues.

**Acceptance Scenarios**:

1. **Given** the codebase, **When** a developer runs `uv run ruff check`, **Then** the linter scans all Python files and reports any style or quality issues.
2. **Given** a file with a linting error, **When** ruff check runs, **Then** clear error messages identify the file, line, and issue description.
3. **Given** the ruff configuration, **When** ruff runs, **Then** it uses rules equivalent to or stricter than the previous flake8 configuration.

---

### User Story 3 - Developer Installs Package with pyproject.toml (Priority: P3)

A developer wants to install the imap-cli package for development or as a dependency. The package configuration should use modern Python packaging standards (PEP 517/518) with pyproject.toml.

**Why this priority**: Package installation is essential but developers can work around a non-modernized setup.py temporarily. The pyproject.toml migration is structural work that enables the other improvements.

**Independent Test**: Can be fully tested by running `uv pip install -e .` and verifying all console scripts are available.

**Acceptance Scenarios**:

1. **Given** a pyproject.toml file, **When** a developer runs `uv pip install -e .`, **Then** the package installs in editable mode with all dependencies.
2. **Given** the installed package, **When** a developer runs any imap-cli command (e.g., `imap-cli-status --help`), **Then** the command executes correctly.
3. **Given** the package metadata, **When** inspecting `uv pip show Imap-CLI`, **Then** version, author, and other metadata display correctly.

---

### User Story 4 - CI Pipeline Uses Modern Tooling (Priority: P4)

The continuous integration pipeline should use the new tooling to run tests and linting automatically on pull requests and pushes.

**Why this priority**: CI automation builds on the foundation of working local tooling (P1-P3). It's important for team workflows but can be added after local development works.

**Independent Test**: Can be tested by verifying CI configuration runs pytest and ruff successfully.

**Acceptance Scenarios**:

1. **Given** a tox configuration updated for Python 3.10+, **When** tox runs, **Then** it executes pytest for tests and ruff for linting.
2. **Given** a Python version matrix, **When** CI runs, **Then** tests execute on Python 3.10, 3.11, and 3.12.

---

### Edge Cases

- What happens when a developer has only Python 2.7 installed? The project should clearly indicate Python 3.10+ is required and fail gracefully with a clear error message.
- How does the system handle existing installations with old dependencies? The migration should not break existing virtualenvs; developers may need to recreate their environment.
- What happens if a test relies on Python 2-specific behavior? Such tests should be updated or removed as part of the migration.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Project MUST use `pyproject.toml` as the sole build configuration file, replacing `setup.py` and `setup.cfg`.
- **FR-002**: Project MUST specify Python 3.10 as the minimum required version in pyproject.toml.
- **FR-003**: Project MUST remove all Python 2 compatibility code including the `future` and `six` library dependencies.
- **FR-004**: Project MUST use pytest as the test runner, replacing nose.
- **FR-005**: Project MUST use ruff as the linter/formatter, replacing flake8 and hacking.
- **FR-006**: Project MUST maintain 90% test coverage requirement.
- **FR-007**: All existing CLI entry points MUST continue to function after migration.
- **FR-008**: Project MUST support installation and dependency management via uv.
- **FR-009**: Project MUST update tox.ini to use pytest and ruff instead of nose and flake8.
- **FR-010**: Project MUST update or remove Python 2-specific syntax and patterns in test files (e.g., `six.moves` imports).
- **FR-011**: Project MUST declare all development dependencies (pytest, ruff, coverage) as optional dependency groups in pyproject.toml.

### Key Entities

- **pyproject.toml**: Central configuration file defining project metadata, dependencies, build system, and tool configurations.
- **Console Scripts**: The CLI entry points (imap-cli-status, imap-cli-list, etc.) that must be preserved during migration.
- **Test Suite**: The collection of unittest-style test files that must continue to pass under pytest.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All existing tests pass when run with `uv run pytest`.
- **SC-002**: Test coverage remains at or above 90% as measured by coverage.py.
- **SC-003**: `uv run ruff check` completes without errors on the codebase.
- **SC-004**: Package installs successfully with `uv pip install -e .` and all 10 console scripts are available.
- **SC-005**: No Python 2 compatibility libraries (six, future, mock) remain in dependencies.
- **SC-006**: The setup.py file is removed (or contains only a shim for legacy tools if needed).
- **SC-007**: tox runs successfully with pytest and ruff on Python 3.10+.

## Assumptions

- The existing unittest-style tests are compatible with pytest without rewriting (pytest supports unittest natively).
- Python's standard library `unittest.mock` will replace the third-party `mock` library.
- The `docopts` dependency remains compatible with Python 3.10+.
- Developers using this project have access to uv or can install it easily.
- The project does not require backward compatibility with Python 2.7 installations.
