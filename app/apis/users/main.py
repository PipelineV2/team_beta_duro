from __future__ import annotations


import uuid
from typing import Optional, Tuple

from app.db import repositories as repo
from app.apis.requesters import fn_get_requester
from app.models.core import BooleanResponse, RecordStatus
from app.models.domains.duro_user import (
    DuroUser,
    DuroUserStatusEnum,
    NewDuroUser,
)
from app.models.entities.core.email import Email
from app.models.exceptions.auth_exception import InactiveStatusException
from app.models.exceptions.crud_exception import (
    DuplicateAccountException,
    InvalidUserAccountStateException,
    NotFoundException,
)

from . import crud, link


async def fn_create_duro_user(
    requester_id: uuid.UUID,
    email: Email,
    duro_users_repo: repo.DuroUsersRepository,
    status: Optional[DuroUserStatusEnum] = DuroUserStatusEnum.active,
) -> Tuple[uuid.UUID, str]:
    # This is structured this way so that no user can be in more than one queue at a time.
    duro_user = await crud.fn_get_duro_user_by_email(
        email.email, status, duro_users_repo, 
    )

    if duro_user is None:
        new_user = await crud.fn_create_duro_user(
            requester_id,
            NewDuroUser(email=email.email),
            duro_users_repo,
        )

        return new_user.id

    else:
        message = (
            "Duro User already exists and is active."
            if duro_user.status == DuroUserStatusEnum.active
            else "Duro User already exists but is inactive."
        )
        raise DuplicateAccountException(duro_user.id, message=message)


async def fn_get_duro_user(
    account_identifier: str,
    duro_users_repo: repo.DuroUsersRepository,
    *,
    raise_not_found_exception: bool = True,
    raise_inactive_status_exception: bool = False,
    raise_not_verified_exception: bool = False,
) -> DuroUser:
    async def find_duro_user():
        try:
            user_id = uuid.UUID(account_identifier)
            return await crud.fn_get_duro_user(user_id, duro_users_repo)
        except ValueError:
            return await crud.fn_get_duro_user_by_email(
                account_identifier, duro_users_repo
            )

    duro_user = await find_duro_user()
    if duro_user is None and raise_not_found_exception:
        raise NotFoundException(message="Duro User not found.")

    if (
        duro_user is not None
        and raise_inactive_status_exception
        and duro_user.status == DuroUserStatusEnum.inactive
    ):
        raise InactiveStatusException()

    if (
        duro_user is not None
        and raise_not_verified_exception
        and duro_user.verified_at is None
    ):
        raise InvalidUserAccountStateException(
            message="Duro User Identity not set/valid."
        )

    return duro_user


# async def fn_delete_duro_user(
#     duro_user_id: uuid.UUID,
#     duro_users_repo: repo.DuroUsersRepository,
#     requester_duro_users_repo: repo.RequesterDuroUsersRepository,
# ) -> DeletedCount:
#     has_links = await link.fn_duro_user_has_links(
#         duro_user_id, requester_duro_users_repo
#     )

#     if has_links.value:
#         raise InvalidDeleteStateException(
#             message="Duro User has existing links."
#         )

#     deleted_count = await crud.fn_delete_duro_user(
#         duro_user_id, duro_users_repo
#     )

#     if deleted_count.count == 0:
#         raise NotFoundException(message="Duro User not found.")

#     return deleted_count


async def fn_activate_duro_user(
    duro_user_id: uuid.UUID,
    duro_users_repo: repo.DuroUsersRepository,
) -> RecordStatus:
    return await crud.fn_activate_duro_user(
        duro_user_id, duro_users_repo, raise_not_found_exception=True
    )

# async def fn_inactivate_duro_user(
#     duro_user_id: uuid.UUID,
#     duro_users_repo: repo.DuroUsersRepository,
#     requester_duro_users_repo: repo.RequesterDuroUsersRepository,
# ) -> RecordStatus:
#     has_links = await link.fn_duro_user_has_links(
#         duro_user_id, requester_duro_users_repo
#     )

#     if has_links.value:
#         raise InvalidInactivateStateException(
#             message="Duro User has existing links."
#         )

#     return await crud.fn_inactivate_duro_user(
#         duro_user_id, duro_users_repo, raise_not_found_exception=True
#     )



# async def fn_link_requester_to_duro_user(
#     requester_id: uuid.UUID,
#     duro_user_id: uuid.UUID,
#     requesters_repo: repo.RequestersRepository,
#     duro_users_repo: repo.DuroUsersRepository,
#     requester_duro_users_repo: repo.RequesterDuroUsersRepository,
# ) -> UpdatedRecord:
#     # check requester_id
#     await fn_get_requester(
#         requester_id, requesters_repo, raise_not_found_exception=True
#     )

#     # check duro_user_id
#     duro_user = await fn_get_duro_user(
#         str(duro_user_id), duro_users_repo
#     )
#     if duro_user.status == DuroUserStatusEnum.inactive:
#         raise InvalidUserAccountStateException()

#     return await link.fn_link_requester_to_duro_user(
#         requester_id, duro_user.id, requester_duro_users_repo
#     )


# async def fn_unlink_requester_from_duro_user(
#     requester_id: uuid.UUID,
#     duro_user_id: uuid.UUID,
#     requesters_repo: repo.RequestersRepository,
#     duro_users_repo: repo.DuroUsersRepository,
#     requester_duro_users_repo: repo.RequesterDuroUsersRepository,
# ) -> DeletedCount:
#     # check requester_id
#     await fn_get_requester(
#         requester_id, requesters_repo, raise_not_found_exception=True
#     )

#     # check duro_user_id
#     duro_user = await fn_get_duro_user(
#         str(duro_user_id), duro_users_repo
#     )
#     if duro_user.status == DuroUserStatusEnum.inactive:
#         raise InvalidUserAccountStateException()

#     return await link.fn_unlink_requester_from_duro_user(
#         requester_id, duro_user.id, requester_duro_users_repo
#     )


async def fn_validate_duro_user_active(
    account_identifier: str,
    duro_users_repo: repo.DuroUsersRepository,
) -> BooleanResponse:
    duro_user = await fn_get_duro_user(
        account_identifier,
        duro_users_repo,
        raise_not_found_exception=True,
        raise_inactive_status_exception=True,
    )

    return BooleanResponse(
        value=(duro_user.status == DuroUserStatusEnum.active)
    )


async def fn_check_duro_user_verified(
    id: uuid.UUID,
    duro_users_repo: repo.DuroUsersRepository,
    *,
    raise_not_verified_exception: Optional[bool] = True,
) -> BooleanResponse:
    user = await fn_get_duro_user(
        str(id),
        duro_users_repo,
        raise_not_found_exception=True,
        raise_inactive_status_exception=True,
        raise_not_verified_exception=raise_not_verified_exception,
    )

    return BooleanResponse(value=(user.verified_at is not None))

