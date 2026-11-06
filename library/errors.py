"""Domain errors. Services raise them; the app turns them into JSON responses."""


class LibraryError(Exception):
    status_code = 500

    def __init__(self, message):
        super().__init__(message)
        self.message = message


class ValidationError(LibraryError):
    status_code = 400


class NotFoundError(LibraryError):
    status_code = 404


class ConflictError(LibraryError):
    """The request is valid but breaks a library rule."""

    status_code = 409
