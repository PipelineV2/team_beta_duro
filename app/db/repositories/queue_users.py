from datetime import datetime
import uuid
from typing import List, Optional

from app.db.base import BaseRepository
from app.db.repositories.helpers.crud_helper import delete_by_id
from app.models.core import IDModelMixin, UpdatedRecord
from app.models.domains.queue_user import (
    QueueUser,
    QueueStatusEnum,
    NewQueueUser,
)


UPSERT_QUEUE_USER = """
    INSERT INTO queue_users(email, telephone, device_id, given_name, family_name, display_name, status, job_title, time_queued, time_dequeued, created_by_requester_id, created_by_administrator_id)
VALUES(:email, :telephone, :device_id, :given_name, :family_name, :display_name, :status, :job_title, :time_queued, :time_dequeued, :created_by_requester_id, :created_by_administrator_id)
ON CONFLICT (email, telephone) DO UPDATE SET status = EXCLUDED.status,  device_id = EXCLUDED.device_id
RETURNING id, email, telephone, device_id, time_queued;
"""

SQL_GET_QUEUE_USERS = """
    SELECT telephone, email, device_id, status, time_queued, created_by_requester_id, created_by_administrator_id FROM queue_users WHERE status=:status AND
    created_by_requester_id=:created_by_requester_id AND created_by_administrator_id=:created_by_administrator_id;
"""

SQL_GET_QUEUE_USER = """
    SELECT telephone, email, device_id, status, time_queued FROM queue_users WHERE id=:id AND status=:status;
"""

SQL_GET_QUEUE_USER_TELEPHONE = """
    SELECT telephone, email, device_id, status, time_queued FROM queue_users WHERE status=:status AND telephone=:telephone;
"""

SQL_GET_QUEUE_USERS_DEVICE_ID_TELEPHONE_EMAIL = """
    SELECT * FROM queue_users WHERE {};
"""

SQL_INACTIVATE_QUEUE_USER_TELEPHONE = """
    UPDATE queue_users
    SET
    status=:status,
    updated_at=now()
    WHERE telephone=:telephone
    RETURNING id, updated_at;
"""
SQL_DELETE_QUEUE_USER= """
    DELETE FROM queue_users
    WHERE device_id=:device_id;
"""

class QueueUsersRepository(BaseRepository):
    async def create_queue_user(
        self,
        *, 
        requester_id: uuid.UUID, 
        administrator_id: uuid.UUID, 
        new_queue_user: NewQueueUser,
        status: Optional[QueueStatusEnum] = QueueStatusEnum.active,
    ) -> IDModelMixin:
        query_values = new_queue_user.dict()
        query_values["created_by_requester_id"] = requester_id
        query_values["created_by_administrator_id"] = administrator_id
        query_values["time_queued"] = datetime.now()
        query_values["status"] = status
        
        del query_values["location"]
        created_queue_user = await self.db.fetch_one(
            query=UPSERT_QUEUE_USER, values=query_values
        )
        return IDModelMixin(**created_queue_user)
    
    async def get_queue_users(
        self,
        *,
        requester_id: uuid.UUID,
        administrator_id: uuid.UUID,
        status: Optional[QueueStatusEnum] = QueueStatusEnum.active,
    ) -> List[QueueUser]:
        query_values = {
            "created_by_requester_id": requester_id,
            "created_by_administrator_id": administrator_id,
            "status": status
        }
        queue_users = await self.db.fetch_all(
            query=SQL_GET_QUEUE_USERS, values=query_values
        )
        
        return (
            [QueueUser(**queue_user) for queue_user in queue_users] 
            if queue_users else []
        )
        
    
    async def get_queue_user(
        self,
        *,
        id: uuid.UUID, 
        status: QueueStatusEnum, 
    ) -> Optional[QueueUser]:
        query_values = {
            "id": str(id),
            "status": status
        }
        queue_user = await self.db.fetch_one(
            query=SQL_GET_QUEUE_USER, values=query_values
        )
        return QueueUser(**queue_user) if queue_user else None
    
    
    async def get_queue_user_telephone(
        self,
        *,
        telephone: str, 
        status: QueueStatusEnum, 
    ) -> Optional[QueueUser]:
        query_values = {
            "telephone": telephone,
            "status": status
        }
        
        queue_user = await self.db.fetch_one(
            query=SQL_GET_QUEUE_USER_TELEPHONE, values=query_values
        )
        
        return QueueUser(**queue_user) if queue_user else None
    
    
    async def get_queue_users_list(
        self,
        *,
        device_id: uuid.UUID,
        email: str,
        telephone: str,
        status: QueueStatusEnum,
    ) -> List[QueueUser]:

        conditions = []
        if device_id is not None:
            conditions.append("( device_id='{}'".format(device_id))
        if email is not None:
            conditions.append("email='{}'".format(email))
        if telephone is not None:
            conditions.append("telephone='{}')".format(telephone))

        condition_str = "TRUE" if not conditions else " OR ".join(conditions)
        if status is not None:
            condition_str = condition_str + " AND status='{}'".format(status)
        query = SQL_GET_QUEUE_USERS_DEVICE_ID_TELEPHONE_EMAIL.format(condition_str)
        queue_user = await self.db.fetch_one(query=query)
        return  QueueUser(**queue_user) if queue_user else None
        
        
    async def inactivate_queue_user_telephone(
        self,
        *,
        telephone: str, 
        status: QueueStatusEnum, 
    ) -> Optional[UpdatedRecord]:
        query_values = {
            "telephone": telephone,
            "status": status
        }
        queue_user = await self.db.fetch_one(
            query=SQL_INACTIVATE_QUEUE_USER_TELEPHONE, values=query_values
        )
        return None if queue_user  is None else UpdatedRecord(**queue_user)
    
    
    
    async def delete_queue(self, *, device_id: uuid.UUID):
        query_values = {
        "device_id": device_id,
    }
        deleted_count = await self.db.fetch_one(query=SQL_DELETE_QUEUE_USER, values=query_values)
        print("delete_queue: ", deleted_count)
        return deleted_count