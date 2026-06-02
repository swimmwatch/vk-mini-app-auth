# Security Policy

## Supported Versions

Security updates are provided for the latest stable release of `vk-mini-app-auth`.
Older versions may not receive patches.

## Reporting a Vulnerability

Please do not disclose security vulnerabilities publicly until they have been reviewed and patched.

Report vulnerabilities through one of these private channels:

- Email: <contact.vasiliev.dmitry@gmail.com>
- Telegram: <https://t.me/contact_vasiliev_dmitry>
- GitHub private vulnerability report: <https://github.com/swimmwatch/vk-mini-app-auth/security/advisories/new>

Include as much detail as possible:

- affected package version;
- Python version;
- a minimal reproduction or proof of concept;
- expected impact;
- any relevant logs or traceback.

We will review the report, confirm the impact, and coordinate a fix before public disclosure.

## Security Practices

- All code changes should be reviewed before merging.
- Dependencies are updated regularly to address known vulnerabilities.
- Secrets, credentials, and private tokens must not be committed.
- Tests for authentication behavior should be deterministic and should not call VK over the network.

## Questions

For security-related questions, contact the maintainers at the email address above.
