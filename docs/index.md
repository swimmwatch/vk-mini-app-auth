---
title: VK Mini Apps authentication for Python
description: Validate signed VK Mini Apps launch parameters in Python without runtime dependencies.
icon: material/shield-check
---

# VK Mini Apps authentication for Python

`vk-mini-app-auth` validates signed VK Mini Apps launch parameters in Python backends.
It keeps the runtime package small, typed, and dependency-free, while still covering the critical checks a backend needs before trusting a VK user ID.

<div class="grid cards" markdown>

-   :material-shield-check:{ .lg .middle } **Verify signatures**

    Compare VK's `sign` value against an HMAC-SHA256 signature built from the received `vk_*` parameters.

-   :material-clock-check:{ .lg .middle } **Reject stale launches**

    Use the built-in TTL check to avoid accepting old launch payloads indefinitely.

-   :material-package-variant-closed:{ .lg .middle } **No runtime dependencies**

    Install a lightweight package that depends only on the Python standard library at runtime.

-   :material-code-braces:{ .lg .middle } **Framework friendly**

    Use the same authenticator in FastAPI, Django, Django Ninja, or any custom HTTP stack.

</div>

## Install

```bash
pip install vk-mini-app-auth
```

## Minimal backend check

```python
from datetime import timedelta

from vk_miniapp_auth import VKMiniAppAuthenticator
from vk_miniapp_auth.errors import InvalidInitDataError

authenticator = VKMiniAppAuthenticator(
    app_id=53377165,
    app_secret="secure-key-from-vk-settings",
    ttl=timedelta(hours=1),
)


def authenticate_vk_request(authorization_header: str) -> int:
    try:
        launch_params = authenticator.get_launch_params(authorization_header)
    except InvalidInitDataError as exc:
        raise PermissionError("Invalid VK launch parameters") from exc

    if launch_params is None or not authenticator.is_signed(launch_params):
        raise PermissionError("VK launch signature check failed")

    return launch_params.vk_user_id
```

!!! tip "Start with the quickstart"
    The [quickstart](guide/quickstart.md) shows the full flow from receiving an authorization header to trusting `vk_user_id`.

## How it fits into a backend

1. The mini app opens with VK launch parameters in the URL.
2. The client sends the launch URL to your backend as the authorization value expected by your application.
3. The backend decodes and parses the launch parameters.
4. `VKMiniAppAuthenticator` checks the app ID, TTL, and VK signature.
5. Your application maps the verified `vk_user_id` to an internal user.

## Next steps

<div class="grid cards" markdown>

-   **Set up the package**

    Install the package and configure VK app credentials.

    [:octicons-arrow-right-24: Installation](guide/install.md)

-   **Understand the signature**

    Learn what gets signed and why only `vk_*` parameters are trusted.

    [:octicons-arrow-right-24: Launch parameters](guide/launch-parameters.md)

-   **Use a web framework**

    Adapt the authenticator to FastAPI, Django, or Django Ninja.

    [:octicons-arrow-right-24: Framework examples](guide/examples/index.md)

-   **Inspect the API**

    Review the public classes, enums, and exceptions.

    [:octicons-arrow-right-24: API reference](references/auth.md)

</div>
