---
title: Installation
description: Install vk-mini-app-auth and configure the VK app credentials required for backend validation.
icon: material/download
---

# Installation

`vk-mini-app-auth` supports Python 3.10 and newer. The runtime package has no external dependencies.

## Install the package

=== "pip"

    ```bash
    python -m pip install --upgrade vk-mini-app-auth
    ```

=== "Poetry"

    ```bash
    poetry add vk-mini-app-auth
    ```

=== "uv"

    ```bash
    uv add vk-mini-app-auth
    ```

## Prepare a project environment

For a new project, create and activate a virtual environment first:

```bash
mkdir vk-mini-app-backend
cd vk-mini-app-backend
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Configure VK credentials

Your backend needs two values from VK app settings:

- `VK_APP_ID`: the numeric application ID.
- `VK_SECRET_TOKEN`: the secure key used to validate launch parameter signatures.

Store them outside source control:

```bash
export VK_APP_ID=53377165
export VK_SECRET_TOKEN="secure-key-from-vk-settings"
```

!!! warning "Never expose the secure key"
    The secure key belongs on the backend only. Do not send it to the mini app frontend and do not commit it to the repository.

## Verify the installation

```bash
python - <<'PY'
from vk_miniapp_auth import VKMiniAppAuthenticator

authenticator = VKMiniAppAuthenticator(53377165, "secure-key")
print(type(authenticator).__name__)
PY
```

You should see:

```text
VKMiniAppAuthenticator
```

Continue with the [quickstart](quickstart.md).
