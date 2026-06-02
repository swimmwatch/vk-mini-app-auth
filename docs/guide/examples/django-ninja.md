---
title: Django Ninja
description: Validate VK Mini Apps launch parameters with a Django Ninja HttpBearer class.
icon: material/api
---

# Django Ninja

Django Ninja can validate VK launch parameters through an `HttpBearer` security class.

## Settings

```python
VK_APP_ID = env.int("VK_APP_ID")
VK_SECRET_TOKEN = env.str("VK_SECRET_TOKEN")
```

## Auth class

```python
from datetime import timedelta

from django.conf import settings
from django.http import HttpRequest
from ninja.security import HttpBearer
from vk_miniapp_auth import VKMiniAppAuthenticator
from vk_miniapp_auth.data import VkLaunchParams
from vk_miniapp_auth.errors import InvalidInitDataError


class VKMiniAppAuth(HttpBearer):
    def __init__(self) -> None:
        super().__init__()
        self.authenticator = VKMiniAppAuthenticator(
            app_id=settings.VK_APP_ID,
            app_secret=settings.VK_SECRET_TOKEN,
            ttl=timedelta(hours=1),
        )

    def authenticate(self, request: HttpRequest, token: str) -> VkLaunchParams | None:
        try:
            launch_params = self.authenticator.get_launch_params(token)
        except InvalidInitDataError:
            return None

        if launch_params is None or not self.authenticator.is_signed(launch_params):
            return None

        return launch_params
```

## Protected endpoint

```python
from ninja import NinjaAPI

api = NinjaAPI()
vk_auth = VKMiniAppAuth()


@api.get("/me", auth=vk_auth)
def read_current_user(request):
    return {"vk_user_id": request.auth.vk_user_id}
```

Returning `None` from `authenticate()` makes Django Ninja reject the request with an unauthorized response.
