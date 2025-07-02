"""VK Mini App Authenticator utilities."""

import base64
import hashlib
import hmac
import logging
import typing
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from urllib.parse import parse_qs
from urllib.parse import urlencode
from urllib.parse import urlparse

from .data import VkLaunchParams
from .errors import InvalidInitDataError
from .types import QueryParams

logger = logging.getLogger(__name__)


class VKMiniAppAuthenticator:
    """VK Mini App Authenticator for validating launch parameters.

    This class provides methods to extract, validate, and check the expiration of launch parameters.
    It uses the VK application ID and secret key to verify the signature of the parameters.
    The launch parameters are expected to be provided in the authorization header as a base64 encoded URL.
    """

    def __init__(self, app_id: int, app_secret: str, ttl: typing.Optional[timedelta] = None):
        """Initializes the VK Mini App Authenticator.

        Args:
            app_id (int): The VK application ID.
            app_secret (str): The VK application secret key.
            ttl (timedelta, optional): Time to live for the launch parameters. Defaults to 1 hour.
        """
        self._app_id = app_id
        self._app_secret = app_secret
        self._ttl = ttl or timedelta(hours=1)

    def get_launch_params(self, authorization_header: str) -> typing.Optional[VkLaunchParams]:
        """Extracts and validates launch parameters from the authorization header.

        Args:
            authorization_header (str): The authorization header containing the launch parameters.

        Returns:
            VkLaunchParams: An instance of VkLaunchParams if valid, otherwise None.
        """
        query_params_url = self.extract_query_params_as_url(authorization_header)
        query_params = self.extract_query_params_as_dict(query_params_url)
        if not query_params:
            return None

        return VkLaunchParams(**query_params)

    @staticmethod
    def extract_query_params_as_url(authorization_header: str) -> str:
        """Extracts the query parameters from the authorization header.

        Args:
            authorization_header (str): The authorization header containing the base64 encoded query parameters.

        Returns:
            str: The decoded query parameters as a URL.
        """
        if not authorization_header:
            raise ValueError("Missing authorization header value")

        authorization_header = authorization_header.strip()

        try:
            return base64.b64decode(authorization_header).decode("utf-8")
        except ValueError as err:
            logger.error("Failed to decode authorization header: %s", err)
            raise InvalidInitDataError("Invalid authorization header format") from err

    @staticmethod
    def extract_query_params_as_dict(query_params_url: str) -> QueryParams:
        """Extracts query parameters from a URL and returns them as a dictionary.

        Args:
            query_params_url (str): The URL containing the query parameters.

        Returns:
            QueryParams: A dictionary containing the query parameters.
        """
        query_string = urlparse(query_params_url).query
        query_params = parse_qs(query_string, keep_blank_values=True)
        return {k: v[0] if isinstance(v, list) else "" for k, v in query_params.items()}

    def is_signed(self, launch_params: VkLaunchParams) -> bool:
        """Validates the signature of the launch parameters. Also checks if the parameters are not expired.

        Args:
            launch_params (VkLaunchParams): The launch parameters to validate.

        Returns:
            bool: True if the launch parameters are valid and signed correctly, False otherwise.
        """
        if self._app_id != launch_params.vk_app_id:
            logger.debug("Invalid VK app ID. Expected: %s, got: %s", self._app_id, launch_params.vk_app_id)
            return False

        if self.is_expired(launch_params):
            logger.debug(
                "Launch parameters are expired. Timestamp: %s, TTL: %s",
                launch_params.vk_ts,
                self._ttl,
            )
            return False

        vk_params = {k: v for k, v in launch_params.get_data().items() if k.startswith("vk_")}
        sorted_vk_params = dict(sorted(vk_params.items()))

        sign_params_query = urlencode(sorted_vk_params)
        sign = (
            base64.urlsafe_b64encode(
                hmac.new(
                    self._app_secret.encode(),
                    sign_params_query.encode(),
                    hashlib.sha256,
                ).digest()
            )
            .decode()
            .rstrip("=")
        )

        return sign == launch_params.sign

    def is_expired(self, launch_params: VkLaunchParams) -> bool:
        """Checks if the launch parameters are expired based on the TTL.

        Args:
            launch_params (VkLaunchParams): The launch parameters to check.

        Returns:
            bool: True if the launch parameters are expired, False otherwise.
        """
        now = datetime.now(timezone.utc)
        return (now - launch_params.vk_ts) > self._ttl
