from typing import Optional

from app.models.core import IDModelMixin, TimestampsMixin
from app.models.entities.core.email import EmailMixin


class PersonBase(EmailMixin):
    given_name: Optional[str]
    family_name: Optional[str]
    display_name: Optional[str]
    telephone: str
    job_title: Optional[str]


class Person(PersonBase):
    status: str


class PersonDBModel(TimestampsMixin, Person, IDModelMixin):
    ...
