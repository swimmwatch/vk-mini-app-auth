# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2026-06-02

### Added

- Added `VKMiniAppAuthenticator.get_verified_launch_params()` for parse-and-verify authentication flows.
- Added a local vendored webchanges GitHub Action for VK documentation monitoring.
- Added polished MkDocs Material documentation, framework examples, API reference metadata, social cards, and project agent guidance.

### Changed

- Updated MkDocs documentation dependencies and Poetry workflow pins to current project tooling.
- Documented the verified launch-params flow and parse-only behavior of `get_launch_params()`.
- Removed the generated GitHub issues archive from the repository.

### Fixed

- Hardened launch parameter parsing, required-field validation, optional field conversion, TTL handling, and signature comparison.
- Fixed local Poetry command execution through the Makefile.
- Fixed the vendored webchanges `between` filter for byte input and line joining.

## [1.0.3] - 2026-01-09

### Changed

- Added Python 3.14 support and dropped Python 3.9 support across package metadata, CI, tooling, and documentation.
- Added a workflow for monitoring VK documentation changes.
- Refreshed development, documentation, test, and GitHub Actions dependencies, including MkDocs, mkdocstrings, pytest tooling, mypy, Black, isort, and core Actions.

## [1.0.2] - 2025-07-02

### Changed

- Optimized signature validation in `is_signed()`.
- Refreshed selected documentation and test tooling dependencies.

## [1.0.1] - 2025-06-26

### Fixed

- Updated the release workflow to use trusted publishing authorization.
- Refreshed the flake8 development dependency.

## [1.0.0] - 2025-06-26

### Added

- Initial `vk-mini-app-auth` package for validating VK Mini Apps launch parameters.
- Added typed launch parameter models, authentication helpers, custom errors, tests, and benchmark coverage.
- Added project documentation, MkDocs configuration, README, contribution metadata, GitHub templates, Dependabot, CI, release, docs, and actionlint workflows.

[Unreleased]: https://github.com/swimmwatch/vk-mini-app-auth/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/swimmwatch/vk-mini-app-auth/compare/v1.0.3...v1.1.0
[1.0.3]: https://github.com/swimmwatch/vk-mini-app-auth/compare/v1.0.2...v1.0.3
[1.0.2]: https://github.com/swimmwatch/vk-mini-app-auth/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/swimmwatch/vk-mini-app-auth/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/swimmwatch/vk-mini-app-auth/releases/tag/v1.0.0
