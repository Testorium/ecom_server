from typing import Callable, TypedDict


class ErrorMessages(TypedDict, total=False):
    """
    Example:

        def duplicate_key_msg(exc: Exception) -> str:
            return f"A record already exists: {exc}"

        error_messages = {
            "duplicate_key": duplicate_key_msg
        }
    """

    not_found: str | Callable[[Exception], str]
    duplicate_key: str | Callable[[Exception], str]
    foreign_key: str | Callable[[Exception], str]
    check_constraint: str | Callable[[Exception], str]
    integrity: str | Callable[[Exception], str]
    undefined_column: str | Callable[[Exception], str]
    undefined_table: str | Callable[[Exception], str]
    unexpected: str | Callable[[Exception], str]


class ErrorKey:
    NOT_FOUND = "not_found"
    DUPLICATE_KEY = "duplicate_key"
    FOREIGN_KEY = "foreign_key"
    CHECK_CONSTRAINT = "check_constraint"
    INTEGRITY = "integrity"
    UNDEFINED_COLUMN = "undefined_column"
    UNDEFINED_TABLE = "undefined_table"
    UNEXPECTED = "unexpected"
