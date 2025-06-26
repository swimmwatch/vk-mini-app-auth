## Using with Django
Let's create authorization middleware.

Firstly, create variables in your `settings.py`:
```python
# other settings...

VK_SECRET_TOKEN = env.str("VK_SECRET_TOKEN")
VK_APP_ID = env.int("VK_APP_ID")
```

Then implement middleware:

```python
import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.http import HttpResponse
from vk_miniapp_auth.auth import VKMiniAppAuthenticator
from vk_miniapp_auth.errors import InvalidInitDataError

from users.services import UserService

logger = logging.getLogger(__name__)


class VKMiniAppAuthorizationMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response
        self._vk_miniapp_authenticator = VKMiniAppAuthenticator(
            settings.VK_APP_ID,
            settings.VK_SECRET_TOKEN,
        )

    def __call__(self, request: HttpRequest) -> HttpResponse:
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        auth_cred = request.headers.get("Authorization")
        if not auth_cred:
            # TODO: handle error
            pass
        
        try:
            launch_params = self._vk_miniapp_authenticator.get_launch_params(auth_cred)
        except InvalidInitDataError:
            # TODO: handle error
            pass

        if not launch_params or not launch_params.vk_user_id:
            # TODO: handle error
            pass

        is_signed = self._vk_miniapp_authenticator.is_signed(launch_params)
        if not is_signed:
            # TODO: handle error
            pass
        else:
            user, _ = UserService.get_or_create(launch_params.vk_user_id)
            request.user = user
    
            logger.debug("User was authorized using VK")

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
```

To use `VKMiniAppAuthorizationMiddleware`, add it to your `MIDDLEWARE` setting in `settings.py`:
```python
MIDDLEWARE = [
    # other middleware classes
    'path.to.VKMiniAppAuthorizationMiddleware',
]
```
