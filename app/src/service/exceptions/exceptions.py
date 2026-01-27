class ServiceError(Exception):
    """Base service exception type."""


class NotFoundError(ServiceError):
    """Not found error.

    This exception is raised when a requested resource is not found.
    """
