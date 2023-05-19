import uuid
from datetime import datetime
from enum import Enum
from typing import Optional, List

from app.models.core import IDModelMixin
from app.models.entities.core.email import EmailMixin
from app.models.entities.person import PersonBase


class QueueStatusEnum(str, Enum):
    active = "active"
    inactive = "inactive"


class QueueBase(PersonBase):
    ...
    
    
class QueueUser(QueueBase):
    status: QueueStatusEnum
    time_queued: Optional[datetime]
    time_dequeued: Optional[datetime]


class QueueUserDBModel(QueueUser, IDModelMixin):
    created_by_requester_id: uuid.UUID
    created_by_administrator_id: uuid.UUID
    device_id: uuid.UUID
    

class NewQueueUser(QueueBase):
    location: List[float]
    device_id: uuid.UUID
    
