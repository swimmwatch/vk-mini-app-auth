# Contributing

Thank you for taking the time to improve `vk-mini-app-auth`.

This project is maintained as a small, dependency-free Python package for VK Mini Apps launch parameter authentication.
Please keep contributions focused and consistent with that scope.

## Project Status

The project is in maintenance mode. The expected contribution types are:

- bug fixes;
- security fixes;
- dependency maintenance;
- documentation fixes;
- CI and packaging fixes;
- small compatibility improvements for VK Mini Apps authentication behavior.

New framework integrations or broad feature additions should be discussed in an issue before implementation.

## Development Workflow

We use GitHub issues for public bug reports and GitHub pull requests for code changes.

1. Fork the repository.
2. Create a branch from `dev`.
3. Keep the change focused on one issue or maintenance task.
4. Add or update tests when behavior changes.
5. Update `README.md` and `docs/` when public behavior or usage changes.
6. Open a pull request against `dev`.

Commit messages should follow Conventional Commits, for example:

```text
fix: handle invalid launch timestamp
docs: update installation guide
ci: adjust docs monitoring workflow
```

## Local Setup

Install development dependencies:

```bash
make install
```

Useful checks:

```bash
make lint
make test
make actionlint
poetry run mkdocs build --strict --site-dir /tmp/vk-mini-app-auth-site
```

For documentation-only changes, run the strict MkDocs build when the changed content affects rendered docs.

## Reporting Bugs

Use [GitHub issues](https://github.com/swimmwatch/vk-mini-app-auth/issues/new/choose) for public bugs.

Good bug reports include:

- a concise summary;
- package version and Python version;
- operating system;
- minimal input or code that reproduces the problem;
- expected behavior;
- actual behavior;
- any traceback or logs.

Do not report security vulnerabilities publicly. Use the process in [SECURITY.md](SECURITY.md).

## Pull Request Checklist

Before opening or updating a pull request:

- keep runtime dependencies unchanged unless explicitly justified;
- preserve public API compatibility unless a breaking change was discussed and accepted;
- keep auth and signature logic covered by focused tests;
- ensure generated artifacts are not committed;
- run the relevant local checks and mention them in the pull request.

## References

This guide is intentionally project-specific. For repository-specific operating notes, see [AGENTS.md](AGENTS.md).
