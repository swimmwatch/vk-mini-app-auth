---
title: Django
description: Validate VK Mini Apps launch parameters in Django middleware.
icon: material/language-python
---

# Django

Middleware is a practical place to validate VK launch parameters for a group of views.

## Settings

```python
VK_APP_ID = env.int("VK_APP_ID")
VK_SECRET_TOKEN = env.str("VK_SECRET_TOKEN")
```

## Middleware

```python
from datetime import timedelta

from django.conf import settings
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import JsonResponse
from vk_miniapp_auth import VKMiniAppAuthenticator
from vk_miniapp_auth.errors import InvalidInitDataError


class VKMiniAppAuthorizationMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response
        self.authenticator = VKMiniAppAuthenticator(
            app_id=settings.VK_APP_ID,
            app_secret=settings.VK_SECRET_TOKEN,
            ttl=timedelta(hours=1),
        )

    def __call__(self, request: HttpRequest) -> HttpResponse:
        authorization_header = request.headers.get("Authorization")
        if authorization_header is None:
            return JsonResponse({"detail": "Missing authorization header"}, status=401)

        try:
            launch_params = self.authenticator.get_launch_params(authorization_header)
        except InvalidInitDataError:
            return JsonResponse({"detail": "Invalid VK launch parameters"}, status=401)

        if launch_params is None or not self.authenticator.is_signed(launch_params):
            return JsonResponse({"detail": "Invalid VK launch signature"}, status=401)

        request.vk_launch_params = launch_params
        return self.get_response(request)
```

## Register the middleware

```python
MIDDLEWARE = [
    # ...
    "path.to.VKMiniAppAuthorizationMiddleware",
]
```

Views can then read `request.vk_launch_params.vk_user_id` and map it to an internal user.

!!! note
    For public routes that do not require VK authentication, place this middleware only around protected URL groups or add path-based bypass logic.
