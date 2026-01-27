from src.service.exceptions import ErrorMessages

CATEGORY_ERROR_MESSAGES: ErrorMessages = {
    "not_found": "The requested category was not found.",
    "duplicate_key": "A category with the same details already exists.",
    "foreign_key": "A foreign key for the category is missing or invalid.",
    "check_constraint": "The category data failed a validation check.",
    "integrity": "There was a data validation error while processing the category.",
    "undefined_column": "There is no such column.",
    "undefined_table": "There is no such table.",
    "unexpected": "Something went wrong while processing the category request.",
}
