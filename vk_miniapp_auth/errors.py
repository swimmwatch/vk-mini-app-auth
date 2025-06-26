class BaseVMAError(Exception):
    """Base class for all VK Mini App related exceptions."""

    pass


class InvalidInitDataError(BaseVMAError):
    """Raised when the initialization data is invalid."""

    pass
