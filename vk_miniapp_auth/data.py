import dataclasses
import enum
import typing
from datetime import datetime
from datetime import timezone

from .errors import InvalidInitDataError


@dataclasses.dataclass
class VkLaunchParams:
    """Represents passed launch parameters from VK.

    Links:
        https://dev.vk.com/en/mini-apps/development/launch-params
    """

    sign: str
    vk_access_token_settings: typing.List[str]
    vk_app_id: int
    vk_are_notifications_enabled: bool
    vk_is_app_user: bool
    vk_is_favorite: bool
    vk_language: "LanguageEnum"
    vk_platform: "PlatformEnum"
    vk_ts: datetime
    vk_user_id: int
    vk_chat_id: typing.Optional[str] = None
    vk_group_id: typing.Optional[int] = None
    vk_has_profile_button: typing.Optional[bool] = None
    vk_is_play_machine: typing.Optional[bool] = None
    vk_is_recommended: typing.Optional[bool] = None
    vk_is_widescreen: typing.Optional[bool] = None
    vk_profile_id: typing.Optional[int] = None
    vk_request_key: typing.Optional[str] = None
    vk_testing_group_id: typing.Optional[int] = None
    vk_ref: typing.Optional[str] = None
    vk_viewer_group_role: typing.Optional["ViewerGroupRoleEnum"] = None

    _REQUIRED_FIELDS: typing.ClassVar[typing.Tuple[str, ...]] = (
        "sign",
        "vk_access_token_settings",
        "vk_app_id",
        "vk_are_notifications_enabled",
        "vk_is_app_user",
        "vk_is_favorite",
        "vk_language",
        "vk_platform",
        "vk_ts",
        "vk_user_id",
    )
    _OPTIONAL_INT_FIELDS: typing.ClassVar[typing.Tuple[str, ...]] = (
        "vk_group_id",
        "vk_profile_id",
        "vk_testing_group_id",
    )
    _OPTIONAL_BOOL_FIELDS: typing.ClassVar[typing.Tuple[str, ...]] = (
        "vk_has_profile_button",
        "vk_is_play_machine",
        "vk_is_recommended",
        "vk_is_widescreen",
    )

    def __init__(self, **kwargs: typing.Any):
        """Initialize the VkLaunchParams with keyword arguments."""
        self._data = kwargs

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.__post_init__()

    def __post_init__(self):
        """Post-initialization processing to convert types and validate data."""
        missing_fields = [field for field in self._REQUIRED_FIELDS if getattr(self, field, None) is None]
        if missing_fields:
            raise InvalidInitDataError(f"Missing launch parameters: {', '.join(missing_fields)}")

        try:
            self.vk_app_id = int(self.vk_app_id)
            self.vk_user_id = int(self.vk_user_id)
            if isinstance(self.vk_access_token_settings, str):
                self.vk_access_token_settings = self.vk_access_token_settings.split(",")
            self.vk_ts = datetime.fromtimestamp(float(self.vk_ts), timezone.utc)  # type: ignore[arg-type]
            self.vk_are_notifications_enabled = bool(int(self.vk_are_notifications_enabled))
            self.vk_is_app_user = bool(int(self.vk_is_app_user))
            self.vk_is_favorite = bool(int(self.vk_is_favorite))
            self.vk_language = LanguageEnum(self.vk_language)
            self.vk_platform = PlatformEnum(self.vk_platform)

            for field in self._OPTIONAL_INT_FIELDS:
                value = getattr(self, field, None)
                if value is not None:
                    setattr(self, field, int(value))

            for field in self._OPTIONAL_BOOL_FIELDS:
                value = getattr(self, field, None)
                if value is not None:
                    setattr(self, field, bool(int(value)))

            if self.vk_viewer_group_role is not None:
                self.vk_viewer_group_role = ViewerGroupRoleEnum(self.vk_viewer_group_role)
        except (TypeError, ValueError, OverflowError, OSError) as err:
            raise InvalidInitDataError("Invalid launch parameters") from err

    def get_data(self) -> typing.Dict[str, typing.Any]:
        """Return the launch parameters as a dictionary."""
        return self._data


class ViewerGroupRoleEnum(str, enum.Enum):
    """Represents the group role of the viewer in VK launch parameters."""

    NONE = "none"
    ADMIN = "admin"
    EDITOR = "editor"
    MEMBER = "member"
    MODERATOR = "moder"


class PlatformEnum(str, enum.Enum):
    """Represents the platform codes used in VK launch parameters."""

    # The platform on which the application was launched:
    DESKTOP_WEB = "desktop_web"
    MOBILE_WEB = "mobile_web"
    MOBILE_ANDROID = "mobile_android"
    MOBILE_IPAD = "mobile_ipad"
    MOBILE_IPHONE = "mobile_iphone"

    # If the mini app was launched from VK Messenger:
    DESKTOP_APP_MESSENGER = "desktop_app_messenger"
    DESKTOP_WEB_MESSENGER = "desktop_web_messenger"
    MOBILE_ANDROID_MESSENGER = "mobile_android_messenger"
    MOBILE_IPHONE_MESSENGER = "mobile_iphone_messenger"

    # If the mini app was launched from outside VK or VK Messenger
    ANDROID_EXTERNAL = "android_external"
    IPHONE_EXTERNAL = "iphone_external"
    IPAD_EXTERNAL = "ipad_external"
    MVK_EXTERNAL = "mvk_external"
    WEB_EXTERNAL = "web_external"


class LanguageEnum(str, enum.Enum):
    """Represents the language codes used in VK launch parameters."""

    RU = "ru"
    UK = "uk"
    UA = "ua"
    BE = "be"
    KZ = "kz"
    PT = "pt"
    ES = "es"
    EN = "en"
