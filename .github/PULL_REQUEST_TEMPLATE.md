<!--
Keep pull requests focused. This project is in maintenance mode, so bug fixes,
security fixes, dependency updates, documentation fixes, CI fixes, and small
compatibility improvements are expected. Discuss broad feature work in an issue first.
-->

## Summary

<!-- Briefly describe what changed and why. -->

## Related Issue

<!-- Link the issue if one exists. Use "Closes #123" when appropriate. -->

## Change Type

- [ ] Bug fix
- [ ] Security fix
- [ ] Dependency maintenance
- [ ] Documentation update
- [ ] CI or packaging update
- [ ] Compatibility improvement

## Verification

<!-- List the checks you ran, or explain why they are not applicable. -->

- [ ] `make lint`
- [ ] `make test`
- [ ] `poetry run mkdocs build --strict --site-dir /tmp/vk-mini-app-auth-site`
- [ ] `make actionlint`

## Checklist

- [ ] I kept the change focused and scoped to this pull request.
- [ ] I preserved public API compatibility or documented an accepted breaking change.
- [ ] I updated tests for behavior changes.
- [ ] I updated documentation for public behavior or usage changes.
- [ ] I did not commit generated artifacts, secrets, or unrelated files.
