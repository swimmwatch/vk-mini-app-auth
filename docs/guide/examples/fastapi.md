## Using with FastAPI
Let's create some useful stuff according to [OAuth2 tutorial](https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/?h=auth).

File `auth.py`:

```python
import http

from fastapi import Depends
from fastapi import HTTPException
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.security.http import HTTPBase

from vk_miniapp_auth.auth import VkMiniAppAuthenticator
from vk_miniapp_auth.auth import WebAppUser
from vk_miniapp_auth.errors import InvalidInitDataError

from .config import VkMiniAppSettings  # Vk Mini App configuration

vk_miniapp_authentication_schema = HTTPBase()


def get_vk_miniapp_authenticator() -> VkMiniAppAuthenticator:
    settings = VkMiniAppSettings()
    return VkMiniAppAuthenticator(settings.secret_token)


def get_current_user(
    auth_cred: HTTPAuthorizationCredentials = Depends(vk_miniapp_authentication_schema),
    vk_miniapp_authenticator: VkMiniAppAuthenticator = Depends(get_vk_miniapp_authenticator),
) -> WebAppUser:
    try:
        launch_params = self._vk_miniapp_authenticator.get_launch_params(request)
    except InvalidInitDataError:
        # TODO: handle error
        pass

    if not launch_params or not launch_params.user_id:
        # TODO: handle error
        pass

    is_signed = self._vk_miniapp_authenticator.is_signed(launch_params)
    if not is_signed:
        # TODO: handle error
        pass
    else:
        user, _ = UserService.get_or_create(launch_params.user_id)

        logger.debug("User was authorized using VK")
    
    try:
        init_data = vk_miniapp_authenticator.validate(auth_cred.credentials)
    except InvalidInitDataError:
        raise HTTPException(
            status_code=http.HTTPStatus.FORBIDDEN,
            detail="Forbidden access.",
        )
    except Exception:
        raise HTTPException(
            status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Internal error.",
        )

    if init_data.user is None:
        raise HTTPException(
            status_code=http.HTTPStatus.FORBIDDEN,
            detail="Forbidden access.",
        )

    return init_data.user
```

Finally, we can use it as usual.

File `app.py`:

```python
from fastapi import Depends
from fastapi import FastAPI
from pydantic import BaseModel

from vk_miniapp_auth.auth import VkLaunchParams

from .auth import get_current_user

app = FastAPI()


class Message(BaseModel):
    text: str


@app.post("/message")
async def send_message(
    message: Message,
    user: VkLaunchParams = Depends(get_current_user),
):
    """
    Some logic...
    """
    ...
```
