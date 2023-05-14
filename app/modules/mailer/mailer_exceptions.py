from app.models.exceptions.core_exception import ErrorModel


class SendEmailException(Exception):
    def __init__(
        self,
        *,
        error_code: str = "send-email-error",
        message: str = "Unable to send email.",
        details: str = "",
    ):
        self.error_code = error_code
        self.message = message
        self.details = details


class SendEmailError(ErrorModel):
    details: str
