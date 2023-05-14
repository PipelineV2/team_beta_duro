import uuid
from typing import Any

from app.models.exceptions.core_exception import ErrorModel


class DuplicateAccountException(Exception):
    def __init__(
        self,
        current_record_id: uuid.UUID,
        *,
        error_code: str = "duplicate-account",
        message: str = "Account Exists"
    ):
        self.current_record_id = current_record_id
        self.error_code = error_code
        self.message = message


class DuplicateDataException(Exception):
    def __init__(
        self,
        current_record_id: uuid.UUID,
        *,
        error_code: str = "duplicate-data",
        message: str = "Duplicate Data Exists"
    ):
        self.current_record_id = current_record_id
        self.error_code = error_code
        self.message = message


class DuplicateDataError(ErrorModel):
    current_record_id: uuid.UUID


DuplicateAccountError = DuplicateDataError


class NotFoundException(Exception):
    def __init__(
        self,
        *,
        error_code: str = "not-found",
        message: str = "Item Not Found",
        details: Any = None
    ):
        self.error_code = error_code
        self.message = message
        self.details = details


class BadRequestException(Exception):
    def __init__(
        self,
        *,
        error_code: str = "bad-request",
        message: str = "Bad Request",
        details: str = ""
    ):
        self.error_code = error_code
        self.message = message
        self.details = details


class BadRequestError(ErrorModel):
    details: str


class MissingParametersException(Exception):
    def __init__(
        self,
        *,
        error_code: str = "missing-parameters",
        message: str = "There are missing parameters in your request.",
        details: str = ""
    ):
        self.error_code = error_code
        self.message = message
        self.details = details


class InvalidStateException(Exception):
    def __init__(
        self,
        *,
        error_code: str = "invalid-state",
        message: str = "Usable to Proceed because ...."
    ):
        self.error_code = error_code
        self.message = message


class InvalidDeleteStateException(Exception):
    def __init__(
        self,
        *,
        error_code: str = "invalid-delete-state",
        message: str = "Usable to Delete because ...."
    ):
        self.error_code = error_code
        self.message = message


class InvalidInactivateStateException(Exception):
    def __init__(
        self,
        *,
        error_code: str = "invalid-inactive-state",
        message: str = "Usable to Inactivate because ...."
    ):
        self.error_code = error_code
        self.message = message


class InvalidUserAccountStateException(Exception):
    def __init__(
        self,
        *,
        error_code: str = "invalid-user-account-state",
        message: str = "Unable to action. Account might be inactive."
    ):
        self.error_code = error_code
        self.message = message


class MissingCredentialException(Exception):
    def __init__(
        self,
        *,
        error_code: str = "missing-credential",
        message: str = "Missing Credential",
        details: Any = None
    ):
        self.error_code = error_code
        self.message = message
        self.details = details


class MissingCredentialError(ErrorModel):
    details: Any


class NotFoundError(ErrorModel):
    details: Any


InvalidStateError = ErrorModel


class IllegalAccessException(Exception):
    def __init__(
        self,
        *,
        error_code: str = "illegal-access",
        message: str = "Illegal Access Request"
    ):
        self.error_code = error_code
        self.message = message


class IllegalAccessError(ErrorModel):
    ...
