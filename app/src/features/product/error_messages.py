from src.service.exceptions import ErrorMessages

PRODUCT_ERROR_MESSAGES: ErrorMessages = {
    "not_found": "The requested product was not found.",
    "duplicate_key": "A product with the same details already exists.",
    "foreign_key": "A foreign key for the product is missing or invalid.",
    "check_constraint": "The product data failed a validation check.",
    "integrity": "There was a data validation error while processing the product.",
    "undefined_column": "There is no such column.",
    "undefined_table": "There is no such table.",
    "unexpected": "Something went wrong while processing the product request.",
}
