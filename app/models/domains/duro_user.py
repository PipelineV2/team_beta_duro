import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from app.models.core import IDModelMixin, TimestampsMixin
from app.models.entities.core.email import EmailMixin


class DuroUserStatusEnum(str, Enum):
    active = "active"
    inactive = "inactive"


class DuroUserBase(EmailMixin):
    telephone: str


class DuroUser(TimestampsMixin, DuroUserBase, IDModelMixin):
    verified_at: Optional[datetime]
    status: DuroUserStatusEnum


class DuroUserDBModel(DuroUser):
    created_by_requester_id: uuid.UUID


NewDuroUser = DuroUserBase
