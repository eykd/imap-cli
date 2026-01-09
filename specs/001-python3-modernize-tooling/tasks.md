# Tasks: Python 3 Modernization & Tooling Upgrade

**Input**: Design documents from `/specs/001-python3-modernize-tooling/`
**Prerequisites**: plan.md, spec.md, research.md, quickstart.md

**Tests**: Existing tests will be migrated, no new test tasks needed (tests already exist).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Project root**: `pyproject.toml`, `tox.ini`, `CLAUDE.md`
- **Package**: `imap_cli/` (main package)
- **Tests**: `imap_cli/tests/` (colocated with source)

---

## Phase 1: Setup (Verification)

**Purpose**: Verify current state and prepare for migration

- [x] T001 Verify all existing tests pass with current nose setup: `coverage run $(which nosetests) -v`
- [x] T002 Document current test count and coverage baseline
- [x] T003 [P] Verify all 10 console scripts work: run each `--help` command

**Checkpoint**: Current functionality verified - ready for migration

---

## Phase 2: Foundational - pyproject.toml Creation (Enables All Stories)

**Purpose**: Create the pyproject.toml that all user stories depend on

**⚠️ CRITICAL**: User Stories 1, 2, and 4 cannot begin until this phase is complete

- [x] T004 Create pyproject.toml with [build-system] section using hatchling backend
- [x] T005 Add [project] metadata section (name, version, description, authors, classifiers) from setup.py to pyproject.toml
- [x] T006 Add [project.dependencies] with `docopt>=0.6.2` (note: not docopts) to pyproject.toml
- [x] T007 Add [project.optional-dependencies] dev group with pytest, pytest-cov, ruff, tox, sphinx to pyproject.toml
- [x] T008 Add [project.scripts] with all 10 console scripts to pyproject.toml
- [x] T009 Add [tool.pytest.ini_options] configuration to pyproject.toml
- [x] T010 Add [tool.ruff] and [tool.ruff.lint] configuration to pyproject.toml
- [x] T011 Add [tool.coverage.run] and [tool.coverage.report] configuration to pyproject.toml
- [x] T012 Verify package installs: `uv pip install -e .`
- [x] T013 Verify all 10 console scripts are available after installation

**Checkpoint**: pyproject.toml complete - user story implementation can now begin

---

## Phase 3: User Story 1 - Developer Runs Tests with Modern Tooling (Priority: P1) 🎯 MVP

**Goal**: Developers can run `uv run pytest` and all tests pass with 90%+ coverage

**Independent Test**: Run `uv sync && uv run pytest --cov=imap_cli --cov-report=term-missing` from fresh clone

### Implementation for User Story 1

- [x] T014 [P] [US1] Replace `from six.moves import configparser` with `import configparser` in imap_cli/config.py
- [x] T015 [P] [US1] Remove `import six` and replace `six.string_types` with `str` in imap_cli/search.py
- [x] T016 [P] [US1] Remove `import six` and replace `six.text_type` with `str` in imap_cli/string.py
- [x] T017 [P] [US1] Remove `import six` and replace `six.text_type` with `str` in imap_cli/summary.py
- [x] T018 [P] [US1] Remove `import six` and replace `six.string_types` with `str` in imap_cli/scripts/imap_api.py
- [x] T019 [P] [US1] Remove `from builtins import bytes` (future library) in imap_cli/tests/__init__.py
- [x] T020 [P] [US1] Replace `import mock` with `from unittest.mock import Mock` in imap_cli/tests/__init__.py
- [x] T021 [P] [US1] Update class `ImapConnectionMock(mock.Mock)` to `ImapConnectionMock(Mock)` in imap_cli/tests/__init__.py
- [x] T022 [P] [US1] Replace `from six.moves import configparser` with `import configparser` in imap_cli/tests/test_config.py
- [x] T023 [P] [US1] Remove `import six` and replace `six.string_types` with `str` in imap_cli/tests/test_fetch.py
- [x] T024 [US1] Run `uv run pytest -v` and verify all tests are discovered
- [x] T025 [US1] Run `uv run pytest --cov=imap_cli --cov-report=term-missing` and verify 90%+ coverage
- [x] T026 [US1] Fix any test failures caused by migration (fixed collections.Iterable → collections.abc.Iterable)

**Checkpoint**: User Story 1 complete - `uv run pytest` passes with 91.93% coverage

---

## Phase 4: User Story 2 - Developer Lints Code with Ruff (Priority: P2)

**Goal**: Developers can run `uv run ruff check` with no errors

**Independent Test**: Run `uv run ruff check .` and verify clean output

### Implementation for User Story 2

- [x] T027 [US2] Run `uv run ruff check .` and capture initial error count (1 error found)
- [x] T028 [US2] Run `uv run ruff check --fix .` to auto-fix compatible issues
- [x] T029 [P] [US2] Manually fix remaining ruff errors in imap_cli/*.py files (none needed)
- [x] T030 [P] [US2] Manually fix remaining ruff errors in imap_cli/scripts/*.py files (none needed)
- [x] T031 [P] [US2] Manually fix remaining ruff errors in imap_cli/tests/*.py files (none needed)
- [x] T032 [US2] Verify `uv run ruff check` passes with no errors

**Checkpoint**: User Story 2 complete - `uv run ruff check` passes

---

## Phase 5: User Story 3 - Developer Installs Package with pyproject.toml (Priority: P3)

**Goal**: Package installs via `uv pip install -e .` with all console scripts working

**Independent Test**: Fresh install and verify all 10 scripts respond to `--help`

### Implementation for User Story 3

- [x] T033 [US3] Verify `uv pip install -e .` completes without errors
- [x] T034 [US3] Verify `uv pip show Imap-CLI` displays correct metadata
- [x] T035 [P] [US3] Verify imap-cli-status --help works
- [x] T036 [P] [US3] Verify imap-cli-list --help works
- [x] T037 [P] [US3] Verify imap-cli-search --help works
- [x] T038 [P] [US3] Verify imap-cli-read --help works
- [x] T039 [P] [US3] Verify imap-cli-flag --help works
- [x] T040 [P] [US3] Verify imap-cli-copy --help works
- [x] T041 [P] [US3] Verify imap-cli-delete --help works
- [x] T042 [P] [US3] Verify imap-api --help works (with `[api]` optional dependency: webob)
- [x] T043 [P] [US3] Verify imap-notify --help works (with `[notify]` optional dependency: plyer, migrated from pynotify)
- [x] T044 [P] [US3] Verify imap-shell --help works

**Checkpoint**: User Story 3 complete - all 10 console scripts functional

---

## Phase 6: User Story 4 - CI Pipeline Uses Modern Tooling (Priority: P4)

**Goal**: tox runs successfully with pytest and ruff on Python 3.10+

**Independent Test**: Run `uv run tox` and verify all environments pass

### Implementation for User Story 4

- [x] T045 [US4] Update tox.ini: remove py2 environment, add py310, py311, py312
- [x] T046 [US4] Update tox.ini: replace `nosetests` with `pytest` command
- [x] T047 [US4] Update tox.ini: replace `flake8` with `ruff check` command
- [x] T048 [US4] Update tox.ini: update deps to use pyproject.toml optional-dependencies
- [x] T049 [US4] Run `uv run tox -e py311` and verify tests pass
- [x] T050 [US4] Run `uv run tox -e lint` (or equivalent ruff env) and verify it passes

**Checkpoint**: User Story 4 complete - tox runs successfully

---

## Phase 7: Cleanup & Polish

**Purpose**: Remove legacy files and update documentation

- [x] T051 [P] Delete setup.py from repository root
- [x] T052 [P] Delete setup.cfg from repository root
- [x] T053 [P] Delete requirements.txt from repository root
- [x] T054 [P] Delete test-requirements.txt from repository root
- [x] T055 Update CLAUDE.md: replace pip/nose/flake8 commands with uv/pytest/ruff commands
- [x] T056 Verify no six/future/mock imports remain: `grep -r "import six\|import future\|import mock" imap_cli/`
- [x] T057 Verify fresh clone workflow: `git clone ... && cd imap-cli && uv sync && uv run pytest`
- [x] T058 Run final success criteria verification from spec.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational (Phase 2)
- **User Story 2 (Phase 4)**: Depends on Foundational (Phase 2), can run in parallel with US1
- **User Story 3 (Phase 5)**: Depends on Foundational (Phase 2), can run after US1
- **User Story 4 (Phase 6)**: Depends on US1 and US2 completion
- **Cleanup (Phase 7)**: Depends on all user stories complete

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Phase 2 (pyproject.toml) - MVP, highest priority
- **User Story 2 (P2)**: Depends on Phase 2 - can run parallel with US1
- **User Story 3 (P3)**: Depends on Phase 2 - verification only, can overlap with US1/US2
- **User Story 4 (P4)**: Depends on US1 + US2 - tox needs both working

### Parallel Opportunities

Within Phase 3 (US1):
- T014-T023 can all run in parallel (different files)

Within Phase 4 (US2):
- T029-T031 can run in parallel (different directories)

Within Phase 5 (US3):
- T035-T044 can all run in parallel (independent verifications)

Within Phase 7 (Cleanup):
- T051-T054 can all run in parallel (independent deletions)

---

## Success Criteria Verification

| Success Criterion | Status | Notes |
|-------------------|--------|-------|
| SC-001: Tests pass with pytest | ✅ PASS | 49 tests pass |
| SC-002: Coverage ≥ 90% | ✅ PASS | 91.93% coverage |
| SC-003: ruff check passes | ✅ PASS | All checks passed |
| SC-004: All 10 console scripts work | ✅ PASS | All 10 work (imap-api via `[api]`, imap-notify via `[notify]` optional deps) |
| SC-005: No six/future/mock in deps | ✅ PASS | Verified with grep |
| SC-006: setup.py/setup.cfg deleted | ✅ PASS | Deleted |
| SC-007: tox runs successfully | ✅ PASS | py311 and lint pass |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Total: 58 tasks across 7 phases
- **COMPLETED**: All phases implemented successfully
