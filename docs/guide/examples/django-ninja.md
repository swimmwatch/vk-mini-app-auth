Here is an example of using VK Mini App authorization with Django Ninja, analogous to the Django middleware example.

## Using with Django Ninja

First, add variables to your `settings.py`:
```python
# other settings...

VK_SECRET_TOKEN = env.str("VK_SECRET_TOKEN")
VK_APP_ID = env.int("VK_APP_ID")
```

Then, implement a dependency for authorization:
```python
import logging

from django.conf import settings
from django.http import HttpRequest
from ninja.security import HttpBearer
from vk_miniapp_auth.auth import VKMiniAppAuthenticator
from vk_miniapp_auth.errors import InvalidInitDataError

from users.services import UserService

logger = logging.getLogger(__name__)

class VKMiniAppAuth(HttpBearer):
    def __init__(self):
        self._vk_miniapp_authenticator = VKMiniAppAuthenticator(
            settings.VK_APP_ID,
            settings.VK_SECRET_TOKEN,
        )

    def authenticate(self, request: HttpRequest, token: str):
        try:
            launch_params = self._vk_miniapp_authenticator.get_launch_params(token)
        except InvalidInitDataError:
            logger.warning("Invalid VK init data")
            return None

        if not launch_params or not launch_params.vk_user_id:
            logger.warning("Missing VK user ID")
            return None

        if not self._vk_miniapp_authenticator.is_signed(launch_params):
            logger.warning("VK signature check failed")
            return None

        user, _ = UserService.get_or_create(launch_params.vk_user_id)
        logger.debug("User was authorized using VK")
        return user
```

Use the dependency in your Ninja API:
```python
from ninja import NinjaAPI

api = NinjaAPI()
vk_auth = VKMiniAppAuth()

@api.get(
    "/protected",
    auth=[vk_auth],
)
def protected_endpoint(request):
    return {"user_id": request.user.id}
```

Add the API to your `urls.py`:
```python
from django.urls import path
from .api import api

urlpatterns = [
    path("api/", api.urls),
]
```

This setup secures your Ninja endpoints using VK Mini App authentication, similar to the Django middleware approach.