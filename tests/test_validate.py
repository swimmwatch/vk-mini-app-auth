import base64
from datetime import datetime
from datetime import timedelta

import freezegun
import pytest

from vk_miniapp_auth.auth import VKMiniAppAuthenticator
from vk_miniapp_auth.data import VkLaunchParams
from vk_miniapp_auth.errors import InvalidInitDataError

from .conftest import _TEST_INIT_DATA
from .conftest import _TEST_PARSED_INIT_DATA
from .conftest import _TEST_VK_APP_ID
from .conftest import _TEST_VK_SECRET_TOKEN


def test_parse(authenticator: VKMiniAppAuthenticator) -> None:
    launch_params = authenticator.get_launch_params(_TEST_INIT_DATA)
    assert launch_params is not None
    assert _TEST_PARSED_INIT_DATA == launch_params


def test_is_signed_accepts_valid_launch_params(authenticator: VKMiniAppAuthenticator) -> None:
    launch_params = authenticator.get_launch_params(_TEST_INIT_DATA)
    assert launch_params is not None

    with freezegun.freeze_time(launch_params.vk_ts):
        assert authenticator.is_signed(launch_params)


def test_is_signed_rejects_wrong_app_id(authenticator: VKMiniAppAuthenticator) -> None:
    launch_params = authenticator.get_launch_params(_TEST_INIT_DATA)
    assert launch_params is not None

    authenticator = VKMiniAppAuthenticator(_TEST_VK_APP_ID + 1, _TEST_VK_SECRET_TOKEN)

    with freezegun.freeze_time(launch_params.vk_ts):
        assert not authenticator.is_signed(launch_params)


def test_is_signed_rejects_wrong_secret(authenticator: VKMiniAppAuthenticator) -> None:
    launch_params = authenticator.get_launch_params(_TEST_INIT_DATA)
    assert launch_params is not None

    authenticator = VKMiniAppAuthenticator(_TEST_VK_APP_ID, "wrong-secret")

    with freezegun.freeze_time(launch_params.vk_ts):
        assert not authenticator.is_signed(launch_params)


def test_get_verified_launch_params(authenticator: VKMiniAppAuthenticator) -> None:
    with freezegun.freeze_time(_TEST_PARSED_INIT_DATA.vk_ts):
        launch_params = authenticator.get_verified_launch_params(_TEST_INIT_DATA)

    assert launch_params == _TEST_PARSED_INIT_DATA


def test_get_verified_launch_params_rejects_invalid_signature() -> None:
    authenticator = VKMiniAppAuthenticator(_TEST_VK_APP_ID, "wrong-secret")

    with freezegun.freeze_time(_TEST_PARSED_INIT_DATA.vk_ts):
        assert authenticator.get_verified_launch_params(_TEST_INIT_DATA) is None


def test_extract_query_params_as_url_rejects_invalid_base64() -> None:
    with pytest.raises(InvalidInitDataError, match="Invalid authorization header format"):
        VKMiniAppAuthenticator.extract_query_params_as_url("%%%")


def test_extract_query_params_as_url_rejects_missing_header() -> None:
    with pytest.raises(InvalidInitDataError, match="Missing authorization header value"):
        VKMiniAppAuthenticator.extract_query_params_as_url("")


def test_extract_query_params_as_url_accepts_missing_padding() -> None:
    encoded_query = base64.b64encode(b"?vk_app_id=1").decode().rstrip("=")

    assert VKMiniAppAuthenticator.extract_query_params_as_url(encoded_query) == "?vk_app_id=1"


def test_get_launch_params_rejects_missing_required_fields(authenticator: VKMiniAppAuthenticator) -> None:
    encoded_query = base64.b64encode(b"?vk_app_id=1").decode()

    with pytest.raises(InvalidInitDataError, match="Missing launch parameters"):
        authenticator.get_launch_params(encoded_query)


def test_launch_params_reject_invalid_required_values() -> None:
    with pytest.raises(InvalidInitDataError, match="Missing launch parameters"):
        VkLaunchParams(
            sign="sign",
            vk_access_token_settings=None,
            vk_app_id=None,
            vk_are_notifications_enabled=None,
            vk_is_app_user=None,
            vk_is_favorite=None,
            vk_language=None,
            vk_platform=None,
            vk_ts=None,
            vk_user_id=None,
        )


def test_launch_params_convert_optional_integer_fields() -> None:
    launch_params = VkLaunchParams(
        **{
            "sign": "sign",
            "vk_access_token_settings": "video",
            "vk_app_id": "53377165",
            "vk_are_notifications_enabled": "0",
            "vk_is_app_user": "1",
            "vk_is_favorite": "0",
            "vk_language": "en",
            "vk_platform": "desktop_web",
            "vk_ts": "1750946152",
            "vk_user_id": "1034314472",
            "vk_group_id": "11",
            "vk_profile_id": "22",
            "vk_testing_group_id": "33",
        }
    )

    assert launch_params.vk_group_id == 11
    assert launch_params.vk_profile_id == 22
    assert launch_params.vk_testing_group_id == 33


def test_zero_ttl_is_preserved() -> None:
    authenticator = VKMiniAppAuthenticator(
        _TEST_VK_APP_ID,
        _TEST_VK_SECRET_TOKEN,
        timedelta(0),
    )

    with freezegun.freeze_time(_TEST_PARSED_INIT_DATA.vk_ts):
        assert not authenticator.is_expired(_TEST_PARSED_INIT_DATA)

    with freezegun.freeze_time(_TEST_PARSED_INIT_DATA.vk_ts + timedelta(microseconds=1)):
        assert authenticator.is_expired(_TEST_PARSED_INIT_DATA)


@pytest.mark.parametrize(
    "expr_in,now,expected",
    [
        # Test case 1: valid input data
        (
            timedelta(hours=1),
            _TEST_PARSED_INIT_DATA.vk_ts,
            False,
        ),
        # Test case 2: expired on 1 second
        (
            timedelta(hours=1),
            _TEST_PARSED_INIT_DATA.vk_ts + timedelta(hours=1, seconds=1),
            True,
        ),
        # Test case 3: not expired
        (
            timedelta(hours=1),
            _TEST_PARSED_INIT_DATA.vk_ts + timedelta(seconds=10),
            False,
        ),
    ],
)
def test_expire(
    authenticator: VKMiniAppAuthenticator,
    expr_in: timedelta,
    now: datetime,
    expected: bool,
) -> None:
    with freezegun.freeze_time(now):
        authenticator = VKMiniAppAuthenticator(
            _TEST_VK_APP_ID,
            _TEST_VK_SECRET_TOKEN,
            expr_in,
        )
        actual = authenticator.is_expired(_TEST_PARSED_INIT_DATA)
        assert actual == expected


@pytest.mark.benchmark
def test_validate_performance(benchmark, authenticator: VKMiniAppAuthenticator):
    launch_params = authenticator.get_launch_params(_TEST_INIT_DATA)
    benchmark.pedantic(
        authenticator.is_signed,
        args=(launch_params,),
        rounds=100,
        iterations=10,
        warmup_rounds=10,
    )
