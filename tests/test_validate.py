from datetime import datetime
from datetime import timedelta

import freezegun
import pytest

from vk_miniapp_auth.auth import VKMiniAppAuthenticator

from .conftest import _TEST_INIT_DATA
from .conftest import _TEST_PARSED_INIT_DATA
from .conftest import _TEST_VK_APP_ID
from .conftest import _TEST_VK_SECRET_TOKEN


def test_parse(authenticator: VKMiniAppAuthenticator) -> None:
    launch_params = authenticator.get_launch_params(_TEST_INIT_DATA)
    assert launch_params is not None
    assert _TEST_PARSED_INIT_DATA == launch_params


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
