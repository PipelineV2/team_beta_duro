from app.models.core import CoreModel


class EmailMixin(CoreModel):
    email: str


Email = EmailMixin
