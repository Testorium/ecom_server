from .types import ErrorMessages

DEFAULT_ERROR_MESSAGES: ErrorMessages = {
    "not_found": "The requested resource was not found.",
    "duplicate_key": "A record matching the supplied data already exists.",
    "foreign_key": "A foreign key is missing or invalid.",
    "check_constraint": "The data failed a check constraint during processing.",
    "integrity": "There was a data validation error during processing.",
    "undefined_column": "There is no such column.",
    "undefined_table": "There is no such table.",
    "unexpected": "Something went wrong while processing your request.",
}
