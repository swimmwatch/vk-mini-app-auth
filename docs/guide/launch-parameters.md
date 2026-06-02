---
title: Launch Parameters
description: Understand how vk-mini-app-auth parses and validates signed VK Mini Apps launch parameters.
icon: material/key-chain
---

# Launch parameters

VK Mini Apps launch data contains user, app, platform, and source information.
The package parses that data into `VkLaunchParams` and verifies that the signed values were not modified.

## What is signed

`VKMiniAppAuthenticator.is_signed()` follows VK's launch parameter signing rules:

1. Read the original launch parameter dictionary.
2. Keep only keys that start with `vk_`.
3. Sort those keys alphabetically.
4. URL-encode the sorted `parameter=value` pairs.
5. Build an HMAC-SHA256 digest with the VK app secure key.
6. Base64url-encode the digest and remove padding.
7. Compare the result with the received `sign` value.

The `sign` field itself is not included in the signed string.

## Important fields

| Field | Meaning |
| --- | --- |
| `vk_app_id` | VK application ID. It must match the `app_id` passed to `VKMiniAppAuthenticator`. |
| `vk_user_id` | VK user ID. Trust it only after signature validation succeeds. |
| `vk_ts` | Launch signature timestamp. It is checked against the configured TTL. |
| `vk_platform` | Platform where the mini app was launched. |
| `vk_language` | User interface language code. |
| `vk_access_token_settings` | Comma-separated permissions granted by the user. |

See the [Launch Data API reference](../references/data.md) for the full parsed model.

## Expiration

The authenticator rejects launch parameters when:

```python
datetime.now(timezone.utc) - launch_params.vk_ts > ttl
```

The default TTL is one hour.

```python
from datetime import timedelta

authenticator = VKMiniAppAuthenticator(
    app_id=53377165,
    app_secret="secure-key-from-vk-settings",
    ttl=timedelta(minutes=15),
)
```

## Unknown parameters

Signature validation uses the original parsed data returned by `VkLaunchParams.get_data()`.
That means additional `vk_*` parameters can still be included in the signature calculation, even when the typed dataclass does not expose a dedicated field yet.

!!! tip
    Keep an eye on VK documentation updates when new launch parameters or enum values appear. Add focused tests before changing signature behavior.
