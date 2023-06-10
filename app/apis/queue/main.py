from __future__ import annotations


import uuid
from typing import Optional, Tuple, List

from app.db.repositories import (
    QueueUsersRepository,
    UsersRepository,
    RequestersRepository,
    RequesterAdministratorsRepository,
    DuroUsersRepository,
)
from app.apis.requesters.crud import (
    validate_coporate_name_and_admin_user_name,
    validate_requester_and_admin,
)
from app.apis.users import fn_get_duro_user
from app.models.domains.queue_user import (
    QueueUser,
    QueueStatusEnum,
    NewQueueUser,
)
from app.models.domains.duro_user import NewDuroUser
from app.models.core import UpdatedRecord
from app.models.exceptions.crud_exception import (
    NotFoundException,
    DuplicateDataException,
)

from . import crud


async def fn_create_queue_user(
    coporate_name: str,
    admin_name: str,
    user: NewQueueUser,
    requesters_repo: RequestersRepository,
    requester_administrators_repo: RequesterAdministratorsRepository,
    queue_users_repo: QueueUsersRepository,
    duro_users_repo: DuroUsersRepository,
) -> Optional[QueueUser]:
    
    # Validate that the coperate entity and administrator exist
    requester_id,  administrator_id = await validate_coporate_name_and_admin_user_name(
        coporate_name,
        admin_name,
        requesters_repo,
        requester_administrators_repo,
    )
    
    
    # Before you queue the user you have to first confirm that the user location is within the administrator's location
    
    # Also check that the user is not in an existing queue with QueueStatusEnum
    queue_users = await crud.fn_get_queue_users_list(
        user.device_id,
        user.email,
        user.telephone,
        QueueStatusEnum.active,
        queue_users_repo,
    )
    
    # Check if queue user exists
    if queue_users :
        raise DuplicateDataException(current_record_id = uuid.uuid4(), message="A user with these details is on the queue.")

    # Delete the queue with existing device_id 
    _ = await crud.fn_delete_queue_user_device_id(user.device_id, queue_users_repo)

    # Queue the user
    new_queue_user = await crud.fn_create_queue_user(
        requester_id, 
        administrator_id, 
        user,
        queue_users_repo
    )
    
    queue_user = await crud.fn_get_queue_user(
        id=new_queue_user.id,
        status=QueueStatusEnum.active,
        queue_users_repo=queue_users_repo,
    )
    
    # Check if queue user exist as a duro user
    duro_user = await fn_get_duro_user(
        queue_user.email, 
        duro_users_repo,
        raise_not_found_exception = False,
        raise_inactive_status_exception = False,
        raise_not_verified_exception = False,
    )

    if duro_user is None:
        from app.apis.users.crud import fn_create_duro_user
        _ = await fn_create_duro_user(
            requester_id,
            NewDuroUser (
                email=queue_user.email,
                telephone=queue_user.telephone,
            ),
            duro_users_repo,
        )
    
    return queue_user


async def fn_get_queue_user_telephone(
    coporate_name: str,
    admin_name: str,
    telephone: str, 
    queue_users_repo: QueueUsersRepository,
    requesters_repo: RequestersRepository,
    requester_administrators_repo: RequesterAdministratorsRepository,
    status: Optional[QueueStatusEnum] = QueueStatusEnum.active, 
) -> Optional[QueueUser]:
    
    # Validate that the coperate entity and administrator exist
    # Validate that the coperate entity and administrator exist
    requester_id,  administrator_id = await validate_coporate_name_and_admin_user_name(
        coporate_name,
        admin_name,
        requesters_repo,
        requester_administrators_repo,
    )
    queue_user = await crud.fn_get_queue_user_telephone(
        telephone=telephone, 
        status=status, 
        queue_users_repo=queue_users_repo
    ) 

    return queue_user

async def fn_get_queue_users(
    requester_id: uuid.UUID,
    administrator_id: uuid.UUID,
    status: QueueStatusEnum,
    requesters_repo: RequestersRepository,
    requester_administrators_repo: RequesterAdministratorsRepository,
    queue_users_repo: QueueUsersRepository,
    ) -> List[QueueUser]:
    
    _ = await validate_requester_and_admin(
        requester_id, 
        administrator_id,
        requesters_repo, 
        requester_administrators_repo,
        raise_not_found_exception=True
    )
    
    queu_users = await crud.fn_get_queue_users(requester_id, administrator_id, status, queue_users_repo)
    
    return queu_users


async def fn_inactivate_queue_user_telephone(
        coperate_id: uuid.UUID,
        administrator_id: uuid.UUID,
        telephone: str,  
        queue_users_repo: QueueUsersRepository,
        requesters_repo: RequestersRepository, 
        requester_administrators_repo: RequesterAdministratorsRepository, 
        *,
        status = QueueStatusEnum.inactive,
    ) -> Optional[UpdatedRecord]:
    
    _ = await validate_requester_and_admin(
        coperate_id, 
        administrator_id,
        requesters_repo, 
        requester_administrators_repo,
        raise_not_found_exception=True
    )
    
    queue_user = await crud.fn_get_queue_user_telephone(
        telephone=telephone, 
        queue_users_repo=queue_users_repo
    ) 
    if queue_user is None:
        raise NotFoundException(message="Telephone number not queued.")
    
    return await crud.fn_inactivate_queue_user_telephone(
        telephone=telephone, 
        status=status, 
        queue_users_repo=queue_users_repo
    )