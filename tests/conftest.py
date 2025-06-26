import pytest

from vk_miniapp_auth.auth import VKMiniAppAuthenticator
from vk_miniapp_auth.data import VkLaunchParams

_TEST_INIT_DATA = (
    "P3ZrX2FjY2Vzc190b2tlbl9zZXR0aW5ncz12aWRlbyZ2a19hcHBfaWQ9NTMzNzcxNjUmdmtfYXJlX25vdGlmaWNhdGlvbnNfZW5hYmxlZD0wJnZr"
    "X2lzX2FwcF91c2VyPTEmdmtfaXNfZmF2b3JpdGU9MCZ2a19sYW5ndWFnZT1lbiZ2a19wbGF0Zm9ybT1kZXNrdG9wX3dlYiZ2a19yZWY9b3RoZXIm"
    "dmtfdHM9MTc1MDk0NjE1MiZ2a191c2VyX2lkPTEwMzQzMTQ0NzImc2l"
    "nbj12SmZweFh1ejhVN2xKeXJXcUgyZTNtd215UlNsT2l1MjRXS1daTGdVSHlV"
)
_TEST_PARSED_INIT_DATA = VkLaunchParams(
    **{
        "sign": "vJfpxXuz8U7lJyrWqH2e3mwmyRSlOiu24WKWZLgUHyU",
        "vk_access_token_settings": "video",
        "vk_app_id": "53377165",
        "vk_are_notifications_enabled": False,
        "vk_is_app_user": True,
        "vk_is_favorite": False,
        "vk_language": "en",
        "vk_platform": "desktop_web",
        "vk_ts": "1750946152",
        "vk_user_id": "1034314472",
        "vk_chat_id": None,
        "vk_group_id": None,
        "vk_has_profile_button": None,
        "vk_is_play_machine": None,
        "vk_is_recommended": None,
        "vk_is_widescreen": None,
        "vk_profile_id": None,
        "vk_request_key": None,
        "vk_testing_group_id": None,
        "vk_ref": "other",
        "vk_viewer_group_role": None,
    }
)
_TEST_VK_APP_ID = 53377165
_TEST_VK_SECRET_TOKEN = "qjtLSPSxPQ6HdlZOvilz"  # noqa: S105


@pytest.fixture()
def authenticator() -> VKMiniAppAuthenticator:
    return VKMiniAppAuthenticator(
        _TEST_VK_APP_ID,
        _TEST_VK_SECRET_TOKEN,
    )
