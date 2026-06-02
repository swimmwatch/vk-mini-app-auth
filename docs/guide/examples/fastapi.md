---
title: FastAPI
description: Validate VK Mini Apps launch parameters with a FastAPI dependency.
icon: simple/fastapi
---

# FastAPI

Use a dependency to parse and validate the authorization header before the endpoint runs.

```python
import os
from datetime import timedelta

from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Request
from fastapi import status
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer
from vk_miniapp_auth import VKMiniAppAuthenticator
from vk_miniapp_auth.data import VkLaunchParams
from vk_miniapp_auth.errors import InvalidInitDataError


app = FastAPI()
security = HTTPBearer(auto_error=False)

authenticator = VKMiniAppAuthenticator(
    app_id=int(os.environ["VK_APP_ID"]),
    app_secret=os.environ["VK_SECRET_TOKEN"],
    ttl=timedelta(hours=1),
)


async def verified_vk_launch_params(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> VkLaunchParams:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
        )

    try:
        launch_params = authenticator.get_verified_launch_params(credentials.credentials)
    except InvalidInitDataError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid VK launch parameters",
        ) from exc

    if launch_params is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid VK launch signature",
        )

    return launch_params


@app.get("/me")
async def read_current_user(
    launch_params: VkLaunchParams = Depends(verified_vk_launch_params),
) -> dict[str, int]:
    return {"vk_user_id": launch_params.vk_user_id}
```

!!! tip
    Replace the `/me` response with your own user lookup or account linking logic after the launch parameters are verified.
