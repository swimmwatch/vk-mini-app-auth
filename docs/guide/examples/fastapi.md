Here is a Markdown example for using VK Mini App authorization with FastAPI, analogous to the Django and Django Ninja examples.

## Using with FastAPI

Implement a dependency for authorization:
```python
import logging
import os
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from vk_miniapp_auth.auth import VKMiniAppAuthenticator
from vk_miniapp_auth.errors import InvalidInitDataError
from users.services import UserService

logger = logging.getLogger(__name__)

class VKMiniAppAuth(HTTPBearer):
    def __init__(self):
        super().__init__()
        self._vk_miniapp_authenticator = VKMiniAppAuthenticator(
            int(os.environ["VK_APP_ID"]),
            os.environ["VK_SECRET_TOKEN"],
        )

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        token = credentials.credentials if credentials else None
        
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")
        
        try:
            launch_params = self._vk_miniapp_authenticator.get_launch_params(token)
        except InvalidInitDataError:
            logger.warning("Invalid VK init data")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid VK init data")
        
        if not launch_params or not launch_params.vk_user_id:
            logger.warning("Missing VK user ID")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing VK user ID")
        
        if not self._vk_miniapp_authenticator.is_signed(launch_params):
            logger.warning("VK signature check failed")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="VK signature check failed")
        
        user, _ = UserService.get_or_create(launch_params.vk_user_id)
        logger.debug("User was authorized using VK")
        return user
```

Use the dependency in your FastAPI app:
```python
from fastapi import FastAPI, Depends

app = FastAPI()
vk_auth = VKMiniAppAuth()

@app.get("/protected")
async def protected_endpoint(user=Depends(vk_auth)):
    return {"user_id": user.id}
```

This setup secures your FastAPI endpoints using VK Mini App authentication, similar to the Django and Django Ninja approaches.
