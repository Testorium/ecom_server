from contextlib import contextmanager
from typing import Callable, Generator, Optional

from asyncpg.exceptions import (
    CheckViolationError,
    ForeignKeyViolationError,
    IntegrityConstraintViolationError,
    UndefinedColumnError,
    UndefinedTableError,
    UniqueViolationError,
)
from fastapi import HTTPException
from fastapi import status as status_codes
from loguru import logger

from .exceptions import NotFoundError
from .types import ErrorKey, ErrorMessages


def _resolve_error_message(
    error_messages: ErrorMessages, key: str, exc: Exception
) -> str:
    template: str | Callable[[Exception], str] = error_messages.get(
        key, f"{key} error: {exc}"
    )  # type: ignore[assignment]
    if callable(template):  # pyright: ignore[reportUnknownArgumentType]
        template = template(exc)  # pyright: ignore[reportUnknownVariableType]
    return template  # pyright: ignore[reportUnknownVariableType]


@contextmanager
def handle_asyncpg_exceptions(
    error_messages: Optional[ErrorMessages] = None,
) -> Generator[None, None, None]:
    try:
        yield

    except NotFoundError as exc:
        if error_messages is not None:
            msg = _resolve_error_message(
                error_messages=error_messages,
                key=ErrorKey.NOT_FOUND,
                exc=exc,
            )
        else:
            msg = "The requested resource was not found."
        logger.exception(msg)
        raise HTTPException(
            status_code=status_codes.HTTP_404_NOT_FOUND,
            detail=msg,
        )

    except UniqueViolationError as exc:
        if error_messages is not None:
            msg = _resolve_error_message(
                error_messages=error_messages,
                key=ErrorKey.DUPLICATE_KEY,
                exc=exc,
            )
        else:
            msg = "A record matching the supplied data already exists."
        logger.exception(msg)
        raise HTTPException(
            status_code=status_codes.HTTP_409_CONFLICT,
            detail=msg,
        )

    except ForeignKeyViolationError as exc:
        if error_messages is not None:
            msg = _resolve_error_message(
                error_messages=error_messages,
                key=ErrorKey.FOREIGN_KEY,
                exc=exc,
            )
        else:
            msg = "A foreign key is missing or invalid."
        logger.exception(msg)
        raise HTTPException(
            status_code=status_codes.HTTP_409_CONFLICT,
            detail=msg,
        )

    except CheckViolationError as exc:
        if error_messages is not None:
            msg = _resolve_error_message(
                error_messages=error_messages,
                key=ErrorKey.CHECK_CONSTRAINT,
                exc=exc,
            )
        else:
            msg = "The data failed a check constraint during processing"
        logger.exception(msg)
        raise HTTPException(
            status_code=status_codes.HTTP_409_CONFLICT,
            detail=msg,
        )

    except IntegrityConstraintViolationError as exc:
        if error_messages is not None:
            msg = _resolve_error_message(
                error_messages=error_messages,
                key=ErrorKey.INTEGRITY,
                exc=exc,
            )
        else:
            msg = "There was a data validation error during processing."
        logger.exception(msg)
        raise HTTPException(
            status_code=status_codes.HTTP_409_CONFLICT,
            detail=msg,
        )

    except UndefinedColumnError as exc:
        if error_messages is not None:
            msg = _resolve_error_message(
                error_messages=error_messages,
                key=ErrorKey.UNDEFINED_COLUMN,
                exc=exc,
            )
        else:
            msg = "There is no such column."

        logger.exception(msg)

        raise HTTPException(
            status_code=status_codes.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while processing your request.",
        )

    except UndefinedTableError as exc:
        if error_messages is not None:
            msg = _resolve_error_message(
                error_messages=error_messages,
                key=ErrorKey.UNDEFINED_TABLE,
                exc=exc,
            )
        else:
            msg = "There is no such table."
        logger.exception(msg)

        raise HTTPException(
            status_code=status_codes.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while processing your request.",
        )

    except Exception as exc:
        if error_messages is not None:
            msg = _resolve_error_message(
                error_messages=error_messages,
                key=ErrorKey.UNEXPECTED,
                exc=exc,
            )
        else:
            msg = "Something went wrong while processing your request."
        logger.exception(msg)

        raise HTTPException(
            status_code=status_codes.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=msg,
        )
