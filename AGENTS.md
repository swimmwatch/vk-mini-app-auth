# AGENTS.md

Operating manual for AI coding agents working in this repository.

## About The Project

`vk-mini-app-auth` is a lightweight Python package that implements VK Mini Apps launch parameter authentication.

- Runtime: Python `3.10+`.
- Runtime dependencies: none.
- Packaging and development tooling: Poetry.
- Public entry point: `VKMiniAppAuthenticator` from `vk_miniapp_auth`.
- Core modules: `auth`, `data`, `errors`, and `types`.
- Documentation: MkDocs Material site under `docs/`, configured by `mkdocs.yml`.

## Golden Rules

1. Keep changes small, focused, and directly tied to the request.
2. Preserve public API compatibility unless a breaking change is explicitly requested.
3. Keep the runtime package dependency-free unless a new runtime dependency is explicitly justified.
4. Use `context7` when you need current documentation for external libraries or tools.
5. Keep repository text, code comments, docs, commit messages, and PR text in English.

## Project Layout

```text
vk_miniapp_auth/
  __init__.py             public package exports
  auth.py                 launch parameter extraction, expiration, and signature validation
  data.py                 launch parameter dataclass and enums
  errors.py               package exceptions
  types.py                shared typing aliases
tests/
  conftest.py             shared fixtures and sample VK launch data
  test_validate.py        parser, expiration, and signature validation tests
docs/
  guide/                  user guide and framework examples
  references/             mkdocstrings API reference pages
mkdocs.yml                documentation site configuration
formatters-cfg.toml       Black, isort, flake8, mypy, and Bandit configuration
.github/workflows/        CI for linting, tests, docs, releases, and actionlint
```

## Daily Commands

```bash
make install
make lint
make test
make format
make mkdocs-serve
make actionlint
```

Useful direct commands:

```bash
poetry lock
poetry run mkdocs build --strict --site-dir /tmp/vk-mini-app-auth-site
poetry run black --check --config formatters-cfg.toml .
poetry run isort --check-only --settings-path formatters-cfg.toml .
```

`make lint` and `make test` should pass before code changes are considered done. For docs-only changes, run the strict MkDocs build when the changed content affects documentation.

## Python And API Rules

- Keep supported Python versions aligned with `pyproject.toml` and CI.
- Treat `VKMiniAppAuthenticator` as the main public API.
- Keep signature generation and validation behavior compatible with VK Mini Apps launch parameter rules.
- Add or update focused pytest coverage for parser, expiration, and signature logic when behavior changes.
- Keep type hints precise and compatible with the existing mypy configuration.
- Do not silence checks with broad ignores unless the reason is narrow and documented in code.
- Use `formatters-cfg.toml` as the source of truth for Black, isort, flake8, mypy, and Bandit settings.

## Dependency Rules

- Runtime dependencies belong under `[tool.poetry.dependencies]`; avoid adding any unless explicitly required.
- Development-only tools belong under `[tool.poetry.group.dev.dependencies]`.
- Update `poetry.lock` whenever dependency constraints change.
- Do not manually edit `poetry.lock`; use Poetry.
- Keep dependency changes separate from unrelated code or docs changes when practical.

## Documentation

- Update `README.md` and `docs/` when public behavior, installation guidance, examples, or API usage changes.
- API reference pages under `docs/references/` use mkdocstrings directives.
- Verify documentation changes with:

```bash
poetry run mkdocs build --strict --site-dir /tmp/vk-mini-app-auth-site
```

- Use `make mkdocs-serve` for local preview on `localhost:8008`.
- Do not commit the generated `site/` directory.

## Tests And CI

- Tests use pytest.
- `make test` runs pytest with coverage and benchmark autosave.
- CI runs linting and tests across Python `3.10` through `3.14`.
- GitHub Actions workflow checks are linted by `make actionlint`.
- For auth behavior changes, prefer deterministic fixtures over network calls.

## Commit And PR Hygiene

- Do not touch unrelated untracked files unless explicitly asked.
- Do not commit generated artifacts such as `.coverage`, `.benchmarks/`, `.mypy_cache/`, `.pytest_cache/`, `site/`, `dist/`, virtualenvs, or IDE files.
- Keep commits scoped to one logical change.
- Commit messages should follow Conventional Commits, for example `fix: handle invalid launch timestamp`.
- Do not bump the package version unless explicitly requested.
- The project is in maintenance mode; bug fixes, dependency maintenance, documentation fixes, and CI fixes are the expected change types.

## Things Not To Do

- Do not add new framework integrations to the runtime package.
- Do not add network access to tests for VK validation behavior.
- Do not weaken lint, type-check, or formatting configuration to make a change pass.
- Do not introduce generated documentation output into version control.
- Do not rewrite the public data model or exception hierarchy without explicit approval.
