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

- [ ] T001 Verify all existing tests pass with current nose setup: `coverage run $(which nosetests) -v`
- [ ] T002 Document current test count and coverage baseline
- [ ] T003 [P] Verify all 10 console scripts work: run each `--help` command

**Checkpoint**: Current functionality verified - ready for migration

---

## Phase 2: Foundational - pyproject.toml Creation (Enables All Stories)

**Purpose**: Create the pyproject.toml that all user stories depend on

**⚠️ CRITICAL**: User Stories 1, 2, and 4 cannot begin until this phase is complete

- [ ] T004 Create pyproject.toml with [build-system] section using hatchling backend
- [ ] T005 Add [project] metadata section (name, version, description, authors, classifiers) from setup.py to pyproject.toml
- [ ] T006 Add [project.dependencies] with `docopt>=0.6.2` (note: not docopts) to pyproject.toml
- [ ] T007 Add [project.optional-dependencies] dev group with pytest, pytest-cov, ruff, tox, sphinx to pyproject.toml
- [ ] T008 Add [project.scripts] with all 10 console scripts to pyproject.toml
- [ ] T009 Add [tool.pytest.ini_options] configuration to pyproject.toml
- [ ] T010 Add [tool.ruff] and [tool.ruff.lint] configuration to pyproject.toml
- [ ] T011 Add [tool.coverage.run] and [tool.coverage.report] configuration to pyproject.toml
- [ ] T012 Verify package installs: `uv pip install -e .`
- [ ] T013 Verify all 10 console scripts are available after installation

**Checkpoint**: pyproject.toml complete - user story implementation can now begin

---

## Phase 3: User Story 1 - Developer Runs Tests with Modern Tooling (Priority: P1) 🎯 MVP

**Goal**: Developers can run `uv run pytest` and all tests pass with 90%+ coverage

**Independent Test**: Run `uv sync && uv run pytest --cov=imap_cli --cov-report=term-missing` from fresh clone

### Implementation for User Story 1

- [ ] T014 [P] [US1] Replace `from six.moves import configparser` with `import configparser` in imap_cli/config.py
- [ ] T015 [P] [US1] Remove `import six` and replace `six.string_types` with `str` in imap_cli/search.py
- [ ] T016 [P] [US1] Remove `import six` and replace `six.text_type` with `str` in imap_cli/string.py
- [ ] T017 [P] [US1] Remove `import six` and replace `six.text_type` with `str` in imap_cli/summary.py
- [ ] T018 [P] [US1] Remove `import six` and replace `six.string_types` with `str` in imap_cli/scripts/imap_api.py
- [ ] T019 [P] [US1] Remove `from builtins import bytes` (future library) in imap_cli/tests/__init__.py
- [ ] T020 [P] [US1] Replace `import mock` with `from unittest.mock import Mock` in imap_cli/tests/__init__.py
- [ ] T021 [P] [US1] Update class `ImapConnectionMock(mock.Mock)` to `ImapConnectionMock(Mock)` in imap_cli/tests/__init__.py
- [ ] T022 [P] [US1] Replace `from six.moves import configparser` with `import configparser` in imap_cli/tests/test_config.py
- [ ] T023 [P] [US1] Remove `import six` and replace `six.string_types` with `str` in imap_cli/tests/test_fetch.py
- [ ] T024 [US1] Run `uv run pytest -v` and verify all tests are discovered
- [ ] T025 [US1] Run `uv run pytest --cov=imap_cli --cov-report=term-missing` and verify 90%+ coverage
- [ ] T026 [US1] Fix any test failures caused by migration

**Checkpoint**: User Story 1 complete - `uv run pytest` passes with 90%+ coverage

---

## Phase 4: User Story 2 - Developer Lints Code with Ruff (Priority: P2)

**Goal**: Developers can run `uv run ruff check` with no errors

**Independent Test**: Run `uv run ruff check .` and verify clean output

### Implementation for User Story 2

- [ ] T027 [US2] Run `uv run ruff check .` and capture initial error count
- [ ] T028 [US2] Run `uv run ruff check --fix .` to auto-fix compatible issues
- [ ] T029 [P] [US2] Manually fix remaining ruff errors in imap_cli/*.py files
- [ ] T030 [P] [US2] Manually fix remaining ruff errors in imap_cli/scripts/*.py files
- [ ] T031 [P] [US2] Manually fix remaining ruff errors in imap_cli/tests/*.py files
- [ ] T032 [US2] Verify `uv run ruff check` passes with no errors

**Checkpoint**: User Story 2 complete - `uv run ruff check` passes

---

## Phase 5: User Story 3 - Developer Installs Package with pyproject.toml (Priority: P3)

**Goal**: Package installs via `uv pip install -e .` with all console scripts working

**Independent Test**: Fresh install and verify all 10 scripts respond to `--help`

### Implementation for User Story 3

- [ ] T033 [US3] Verify `uv pip install -e .` completes without errors
- [ ] T034 [US3] Verify `uv pip show Imap-CLI` displays correct metadata
- [ ] T035 [P] [US3] Verify imap-cli-status --help works
- [ ] T036 [P] [US3] Verify imap-cli-list --help works
- [ ] T037 [P] [US3] Verify imap-cli-search --help works
- [ ] T038 [P] [US3] Verify imap-cli-read --help works
- [ ] T039 [P] [US3] Verify imap-cli-flag --help works
- [ ] T040 [P] [US3] Verify imap-cli-copy --help works
- [ ] T041 [P] [US3] Verify imap-cli-delete --help works
- [ ] T042 [P] [US3] Verify imap-api --help works
- [ ] T043 [P] [US3] Verify imap-notify --help works
- [ ] T044 [P] [US3] Verify imap-shell --help works

**Checkpoint**: User Story 3 complete - all console scripts functional

---

## Phase 6: User Story 4 - CI Pipeline Uses Modern Tooling (Priority: P4)

**Goal**: tox runs successfully with pytest and ruff on Python 3.10+

**Independent Test**: Run `uv run tox` and verify all environments pass

### Implementation for User Story 4

- [ ] T045 [US4] Update tox.ini: remove py2 environment, add py310, py311, py312
- [ ] T046 [US4] Update tox.ini: replace `nosetests` with `pytest` command
- [ ] T047 [US4] Update tox.ini: replace `flake8` with `ruff check` command
- [ ] T048 [US4] Update tox.ini: update deps to use pyproject.toml optional-dependencies
- [ ] T049 [US4] Run `uv run tox -e py310` and verify tests pass
- [ ] T050 [US4] Run `uv run tox -e lint` (or equivalent ruff env) and verify it passes

**Checkpoint**: User Story 4 complete - tox runs successfully

---

## Phase 7: Cleanup & Polish

**Purpose**: Remove legacy files and update documentation

- [ ] T051 [P] Delete setup.py from repository root
- [ ] T052 [P] Delete setup.cfg from repository root
- [ ] T053 [P] Delete requirements.txt from repository root
- [ ] T054 [P] Delete test-requirements.txt from repository root
- [ ] T055 Update CLAUDE.md: replace pip/nose/flake8 commands with uv/pytest/ruff commands
- [ ] T056 Verify no six/future/mock imports remain: `grep -r "import six\|import future\|import mock" imap_cli/`
- [ ] T057 Verify fresh clone workflow: `git clone ... && cd imap-cli && uv sync && uv run pytest`
- [ ] T058 Run final success criteria verification from spec.md

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

## Parallel Example: User Story 1 Implementation

```bash
# All Python 2 compat removal tasks can run in parallel:
Task: "Replace six.moves import in imap_cli/config.py"
Task: "Replace six import in imap_cli/search.py"
Task: "Replace six import in imap_cli/string.py"
Task: "Replace six import in imap_cli/summary.py"
Task: "Replace six import in imap_cli/scripts/imap_api.py"
Task: "Remove future import in imap_cli/tests/__init__.py"
Task: "Replace mock import in imap_cli/tests/__init__.py"
Task: "Replace six.moves import in imap_cli/tests/test_config.py"
Task: "Replace six import in imap_cli/tests/test_fetch.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (verify current state)
2. Complete Phase 2: Foundational (create pyproject.toml)
3. Complete Phase 3: User Story 1 (tests working with pytest)
4. **STOP and VALIDATE**: Run `uv run pytest` - all tests pass with 90%+ coverage
5. This is a functional MVP - tests work with modern tooling

### Incremental Delivery

1. Phase 1 + 2 → pyproject.toml ready
2. Add User Story 1 → Tests work → Validate
3. Add User Story 2 → Linting works → Validate
4. Add User Story 3 → Console scripts verified → Validate
5. Add User Story 4 → tox works → Validate
6. Phase 7 → Cleanup legacy files → Final validation

---

## Success Criteria Mapping

| Success Criterion | Task(s) |
|-------------------|---------|
| SC-001: Tests pass with pytest | T024-T026 |
| SC-002: Coverage ≥ 90% | T025 |
| SC-003: ruff check passes | T032 |
| SC-004: All 10 console scripts work | T035-T044 |
| SC-005: No six/future/mock in deps | T056 |
| SC-006: setup.py/setup.cfg deleted | T051-T052 |
| SC-007: tox runs successfully | T049-T050 |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Total: 58 tasks across 7 phases
