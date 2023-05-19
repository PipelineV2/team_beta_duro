import uuid
from typing import List, Optional

from app.db.repositories import QueueUsersRepository
from app.models.core import IDModelMixin
from app.models.domains.queue_user import QueueUser, NewQueueUser, QueueStatusEnum
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



# async def fn_get_duro_user_by_email(
#     email: str, status: DuroUserStatusEnum, duro_users_repo: DuroUsersRepository, 
# ) -> Optional[DuroUser]:
#     return await duro_users_repo.get_duro_user_by_email(email=email, status=status)


# async def fn_get_duro_user_requester_id(
#     id: uuid.UUID, status: DuroUserStatusEnum, duro_users_repo: DuroUsersRepository
# ) -> Optional[DuroUser]:
#     return await duro_users_repo.get_duro_user(id=id, status=status)


# async def fn_get_duro_user_by_email_requester_id(
#     email: str, status: DuroUserStatusEnum, duro_users_repo: DuroUsersRepository, 
# ) -> Optional[DuroUser]:
#     return await duro_users_repo.get_duro_user_by_email(email=email, status=status)

# async def fn_delete_duro_user(
#     id: uuid.UUID, duro_users_repo: DuroUsersRepository
# ) -> DeletedCount:
#     return await duro_users_repo.delete_duro_user(id=id)


# async def fn_activate_duro_user(
#     id: uuid.UUID,
#     duro_users_repo: DuroUsersRepository,
#     *,
#     raise_not_found_exception: bool = False,
# ) -> Optional[RecordStatus]:
#     record_status = await duro_users_repo.activate_duro_user(id=id)
#     if record_status is None and raise_not_found_exception:
#         raise NotFoundException(message="Duro User not found.")

#     return record_status


# async def fn_inactivate_duro_user(
#     id: uuid.UUID,
#     duro_users_repo: DuroUsersRepository,
#     *,
#     raise_not_found_exception: bool = False,
# ) -> Optional[RecordStatus]:
#     record_status = await duro_users_repo.inactivate_duro_user(id=id)
#     if record_status is None and raise_not_found_exception:
#         raise NotFoundException(message="Duro User not found.")

#     return record_status


# async def fn_set_duro_user_verified(
#     id: uuid.UUID,
#     duro_users_repo: DuroUsersRepository,
#     *,
#     raise_not_found_exception: bool = False,
# ) -> Optional[UpdatedRecord]:
#     updated_record = await duro_users_repo.set_duro_user_verified(id=id)
#     if updated_record is None and raise_not_found_exception:
#         raise NotFoundException(message="Duro User not found.")

#     return updated_record
