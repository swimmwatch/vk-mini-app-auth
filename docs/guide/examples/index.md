---
title: Framework Examples
description: Use vk-mini-app-auth in FastAPI, Django, and Django Ninja backends.
icon: material/application-braces
---

# Framework examples

The authenticator is framework-agnostic. Each example follows the same pattern:

1. Read the authorization value from the incoming request.
2. Parse launch parameters with `get_launch_params()`.
3. Validate the signature and TTL with `is_signed()`.
4. Use the verified `vk_user_id` in application-specific user lookup logic.

<div class="grid cards" markdown>

-   **FastAPI**

    Dependency-based authentication for route handlers.

    [:octicons-arrow-right-24: FastAPI](fastapi.md)

-   **Django**

    Middleware-based authentication for Django views.

    [:octicons-arrow-right-24: Django](django.md)

-   **Django Ninja**

    `HttpBearer` integration for Ninja API endpoints.

    [:octicons-arrow-right-24: Django Ninja](django-ninja.md)

</div>
