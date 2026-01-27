from typing import Optional, cast

from .exceptions import DEFAULT_ERROR_MESSAGES, ErrorMessages


class BaseService:
    error_messages: Optional[ErrorMessages] = None

    @staticmethod
    def _get_error_messages(
        error_messages: Optional[ErrorMessages | None] = None,
        default_messages: Optional[ErrorMessages | None] = None,
    ) -> ErrorMessages:
        messages = cast("ErrorMessages", dict(DEFAULT_ERROR_MESSAGES))

        if default_messages:
            messages.update(default_messages)

        if error_messages:
            messages.update(error_messages)

        return messages
