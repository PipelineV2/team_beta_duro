from __future__ import annotations


import uuid
from typing import Optional, Tuple

from app.db.repositories import (
    QueueUsersRepository,
    UsersRepository,
    RequestersRepository,
    RequesterAdministratorsRepository,
    DuroUsersRepository,
)
from app.apis.requesters import fn_get_requester
from app.apis.requesters.administrators import fn_list_requester_administrators_by_request_id
from app.apis.users import fn_get_duro_user, fn_create_duro_user
from app.models.domains.queue_user import (
    QueueUser,
    QueueStatusEnum,
    NewQueueUser,
)
from app.models.exceptions.crud_exception import (
    NotFoundException,
)

from . import crud


async def fn_create_queue_user(
    requester_id: uuid.UUID,
    administrator_id: uuid.UUID,
    user: NewQueueUser,
    requesters_repo: RequestersRepository,
    requester_administrators_repo: RequesterAdministratorsRepository,
    queue_users_repo: QueueUsersRepository,
    duro_users_repo: DuroUsersRepository,
) -> Optional[QueueUser]:
    
    # Check that the queue requester exist
    _ = await fn_get_requester(
        requester_id, 
        requesters_repo,
        raise_not_found_exception=True
        )
    
    # Get registered administrators for this requester
    admins = await fn_list_requester_administrators_by_request_id(
        requester_id,
        requester_administrators_repo,
    )
    
    # Get admins ids
    admin_ids = [admin.id for admin in admins]
    
    # Check that administrator's id exists
    if administrator_id not in admin_ids:
        raise NotFoundException(message="Requester administrator not found.")
    
    # Before you queue the user you have to first confirm that the user location is withing the administrator's location
    
    # Also check that the user is not in an existing queue with QueueStatusEnum
    
    # Queue the user
    new_queue_user = await crud.fn_create_queue_user(
        requester_id, 
        administrator_id, 
        user,
        queue_users_repo
    )
    
    print("queue users created: ", new_queue_user)
    
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
        _ = await fn_create_duro_user(
            requester_id,
            queue_user.email,
            duro_users_repo,
        )
    
    return queue_user


async def fn_get_queue_user_telephone(
    telephone: uuid.UUID, 
    queue_users_repo: QueueUsersRepository,
    status: Optional[QueueStatusEnum] = QueueStatusEnum.active, 
) -> Optional[QueueUser]:
    queue_user = await crud.fn_get_queue_user_telephone(
        telephone=telephone, 
        status=status, 
        queue_users_repo=queue_users_repo
    ) 

    # if queue_user is None:
    #     raise NotFoundException(message="Telephone number not found.")
    
    return queue_user