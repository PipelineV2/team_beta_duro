import uuid
from typing import List, Optional

from app.db.base import BaseRepository
from app.db.repositories.helpers.crud_helper import delete_by_id
from app.models.core import DeletedCount, IDModelMixin, RecordStatus, UpdatedRecord
from app.models.domains.queue_user import (
    QueueUser,
    QueueStatusEnum,
    NewQueueUser,
)


UPSERT_QUEUE_USER = """
    INSERT INTO queue_users(email, phone, device_id, time_queued, created_by_requester_id, created_by_administrator_id)
    VALUES(:email, :phone, :device_id, CURRENT_TIMESTAMP, :created_by_requester_id, :created_by_administrator_id)
    ON CONFLICT(email, phone, device_id) DO UPDATE
    SET created_by_requester_id=EXCLUDED.created_by_requester_id, 
    created_by_administrator_id=EXCLUDED.created_by_administrator_id, time_queued=CURRENT_TIMESTAMP, status=EXCLUDED.status
    RETURNING email, phone, device_id, time_queued;
"""



class QueueUsersRepository(BaseRepository):
    async def create_queue_user(
        self,
        *, 
        requester_id: uuid.UUID, 
        administrator_id: uuid.UUID, 
        new_Duro_user: NewQueueUser,
        status: Optional[QueueStatusEnum] = QueueStatusEnum.active,
    ) -> IDModelMixin:
        query_values = new_Duro_user.dict()
        query_values["created_by_requester_id"] = requester_id
        query_values["created_by_administrator_id"] = administrator_id
        query_values["status"] = status
        created_queue_user = await self.db.fetch_one(
            query=UPSERT_QUEUE_USER, values=query_values
        )
        return IDModelMixin(**created_queue_user)