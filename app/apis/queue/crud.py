import uuid
from typing import List, Optional

from app.db.repositories import QueueUsersRepository
from app.models.core import IDModelMixin
from app.models.domains.queue_user import QueueUser, NewQueueUser, QueueStatusEnum
from app.models.core import IDModelMixin, UpdatedRecord
from app.models.exceptions.crud_exception import NotFoundException


async def fn_create_queue_user(
    requester_id: uuid.UUID,
    administrator_id: uuid.UUID,
    new_queue_user: NewQueueUser,
    queue_users_repo: QueueUsersRepository,
) -> IDModelMixin:
    return await queue_users_repo.create_queue_user(
        requester_id=requester_id, administrator_id=administrator_id, new_queue_user=new_queue_user
    )


async def fn_get_queue_users(
    requester_id: uuid.UUID,
    administrator_id: uuid.UUID,
    status: QueueStatusEnum, 
    queue_users_repo: QueueUsersRepository,
) -> List[QueueUser]:
    return await queue_users_repo.get_queue_users(
        requester_id=requester_id, administrator_id=administrator_id, status=status
    )
    
    
async def fn_get_queue_user(
    id: uuid.UUID, 
    status:  QueueStatusEnum, 
    queue_users_repo: QueueUsersRepository
) -> Optional[QueueUser]:
    return await queue_users_repo.get_queue_user(id=id, status=status)


async def fn_get_queue_user_telephone(
    telephone: str, 
    queue_users_repo: QueueUsersRepository,
    status: Optional[QueueStatusEnum] = QueueStatusEnum.active, 
) -> Optional[QueueUser]:
    
    return await queue_users_repo.get_queue_user_telephone(telephone=telephone, status=status) 


async def fn_get_queue_users_list(
        device_id: uuid.UUID,
        email: str,
        telephone: str,
        status: QueueStatusEnum,
        queue_users_repo: QueueUsersRepository,
    ) -> List[QueueUser]:
    return await queue_users_repo.get_queue_users_list(
        device_id=device_id, 
        email=email, 
        telephone=telephone, 
        status=status
    ) 


async def fn_inactivate_queue_user_telephone(
        telephone: str, 
        status: QueueStatusEnum, 
        queue_users_repo: QueueUsersRepository,
    ) -> Optional[UpdatedRecord]:

    return await queue_users_repo.inactivate_queue_user_telephone(telephone=telephone, status=status)