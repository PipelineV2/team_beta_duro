import uuid
from typing import List, Optional

from app.db.repositories import DuroUsersRepository
from app.models.core import DeletedCount, IDModelMixin, RecordStatus, UpdatedRecord
from app.models.domains.duro_user import DuroUser, NewDuroUser, DuroUserStatusEnum
from app.models.exceptions.crud_exception import NotFoundException


async def fn_create_duro_user(
    requester_id: uuid.UUID,
    new_duro_user: NewDuroUser,
    duro_users_repo: DuroUsersRepository,
) -> IDModelMixin:
    return await duro_users_repo.create_duro_user(
        requester_id=requester_id, new_duro_user=new_duro_user
    )


async def fn_get_duro_users(
    requester_id: uuid.UUID,
    duro_users_repo: DuroUsersRepository,
) -> List[DuroUser]:
    return await duro_users_repo.get_duro_users(requester_id)


async def fn_get_duro_user(
    id: uuid.UUID, status: DuroUserStatusEnum, duro_users_repo: DuroUsersRepository
) -> Optional[DuroUser]:
    return await duro_users_repo.get_duro_user(id=id, status=status)


async def fn_get_duro_user_by_email(
    email: str, 
    duro_users_repo: DuroUsersRepository, 
    status: Optional[DuroUserStatusEnum] = DuroUserStatusEnum.active, 
) -> Optional[DuroUser]:
    return await duro_users_repo.get_duro_user_by_email(email=email, status=status)


async def fn_get_duro_user_requester_id(
    id: uuid.UUID, status: DuroUserStatusEnum, duro_users_repo: DuroUsersRepository
) -> Optional[DuroUser]:
    return await duro_users_repo.get_duro_user(id=id, status=status)


async def fn_get_duro_user_by_email_requester_id(
    email: str, status: DuroUserStatusEnum, duro_users_repo: DuroUsersRepository, 
) -> Optional[DuroUser]:
    return await duro_users_repo.get_duro_user_by_email(email=email, status=status)

async def fn_delete_duro_user(
    id: uuid.UUID, duro_users_repo: DuroUsersRepository
) -> DeletedCount:
    return await duro_users_repo.delete_duro_user(id=id)


async def fn_activate_duro_user(
    id: uuid.UUID,
    duro_users_repo: DuroUsersRepository,
    *,
    raise_not_found_exception: bool = False,
) -> Optional[RecordStatus]:
    record_status = await duro_users_repo.activate_duro_user(id=id)
    if record_status is None and raise_not_found_exception:
        raise NotFoundException(message="Duro User not found.")

    return record_status


async def fn_inactivate_duro_user(
    id: uuid.UUID,
    duro_users_repo: DuroUsersRepository,
    *,
    raise_not_found_exception: bool = False,
) -> Optional[RecordStatus]:
    record_status = await duro_users_repo.inactivate_duro_user(id=id)
    if record_status is None and raise_not_found_exception:
        raise NotFoundException(message="Duro User not found.")

    return record_status


async def fn_set_duro_user_verified(
    id: uuid.UUID,
    duro_users_repo: DuroUsersRepository,
    *,
    raise_not_found_exception: bool = False,
) -> Optional[UpdatedRecord]:
    updated_record = await duro_users_repo.set_duro_user_verified(id=id)
    if updated_record is None and raise_not_found_exception:
        raise NotFoundException(message="Duro User not found.")

    return updated_record
