---
title: Quickstart
description: Validate a VK Mini Apps launch payload and extract a trusted VK user ID.
icon: material/rocket-launch
---

# Quickstart

This page shows the smallest useful backend flow.

## Create an authenticator

```python
from datetime import timedelta

from vk_miniapp_auth import VKMiniAppAuthenticator

authenticator = VKMiniAppAuthenticator(
    app_id=53377165,
    app_secret="secure-key-from-vk-settings",
    ttl=timedelta(hours=1),
)
```

The default TTL is one hour. Pass a custom `datetime.timedelta` when your application needs a shorter or longer acceptance window.

## Validate a request

```python
from vk_miniapp_auth.errors import InvalidInitDataError


def get_verified_vk_user_id(authorization_header: str) -> int:
    try:
        launch_params = authenticator.get_launch_params(authorization_header)
    except InvalidInitDataError as exc:
        raise PermissionError("Invalid VK launch parameters") from exc

    if launch_params is None:
        raise PermissionError("Missing VK launch parameters")

    if not authenticator.is_signed(launch_params):
        raise PermissionError("Invalid VK launch signature")

    return launch_params.vk_user_id
```

Use the returned `vk_user_id` only after `is_signed()` returns `True`.

## Send launch data from the client

The package expects the authorization value to contain a base64-encoded URL with the VK launch query string.
Keep the secure key on the backend; the client only forwards launch data it received from VK.

```javascript
const launchUrl = window.location.href
const token = btoa(launchUrl)

await fetch("/api/me", {
  headers: {
    Authorization: token,
  },
})
```

!!! note
    If your frontend framework already provides a backend token transport, you can use that instead. The backend still needs the original VK launch parameters to verify the signature.

## Handle failures consistently

Treat all validation failures as authentication failures:

- malformed base64 or query string;
- missing required launch parameters;
- wrong `vk_app_id`;
- expired `vk_ts`;
- mismatched `sign`.

Avoid returning detailed signature errors to end users. Detailed logs are useful internally, but public responses should stay generic.
