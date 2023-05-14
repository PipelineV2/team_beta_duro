from __future__ import annotations

from typing import TYPE_CHECKING

# from app.apis.platform.users import fn_send_verification_email
from app.models.core import DeletedCount

if TYPE_CHECKING:
    from app.db.repositories import (
        RequesterAdministratorsRepository,
        RequestersRepository,
        UsersRepository,
    )

import uuid
from typing import Optional

from app.apis.platform import (
    fn_create_user,
    fn_email_exists_in_users,
    fn_update_user_email,
)
from app.models.domains.platform_user import PlatformUserRoleTypeEnum
from app.models.domains.requester import (
    NewRequester,
    Requester,
    UpdateRequester,
    UpdateRequesterWithAdministrator,
)

from . import administrators, crud, validator



async def fn_create_requester(
    new_requester: NewRequester,
    requesters_repo: RequestersRepository,
    requester_administrators_repo: RequesterAdministratorsRepository,
    users_repo: UsersRepository,
    is_testing: bool = False,
) -> Optional[Requester]:
    requester = new_requester.corporation
    administrator = new_requester.administrator

    if await validator.fn_email_not_exists_in_requesters(
        requester.email, requesters_repo
    ) and not await fn_email_exists_in_users(administrator.email, users_repo):
        created_requester = await crud.fn_create_requester(requester, requesters_repo)

        _ = await administrators.fn_create_requester_administrator(
            administrator, created_requester.id, requester_administrators_repo
        )

        requester_full = await crud.fn_get_requester(
            created_requester.id, requesters_repo
        )
        requester_administrators = (
            await administrators.fn_list_requester_administrators_by_request_id(
                created_requester.id, requester_administrators_repo
            )
        )

        requester_full.administrators = requester_administrators

        created_user = await fn_create_user(
            administrator.email,
            PlatformUserRoleTypeEnum.requester,
            created_requester.id,
            users_repo,
        )

        # if not is_testing:
        #     await fn_send_verification_email(created_user.id, administrator.email)

        return requester_full

    return None


async def fn_get_requesters(
    name: Optional[str],
    requesters_repo: RequestersRepository,
) -> Optional[Requester]:
    return await requesters_repo.get_requesters(name=name)


async def fn_get_requester_full(
    id: uuid.UUID,
    requesters_repo: RequestersRepository,
    requester_administrators_repo: RequesterAdministratorsRepository,
    *,
    raise_not_found_exception: bool = True,
    raise_inactive_status_exception: bool = False,
) -> Optional[Requester]:
    requester_full = await crud.fn_get_requester(
        id,
        requesters_repo,
        raise_not_found_exception=raise_not_found_exception,
        raise_inactive_status_exception=raise_inactive_status_exception,
    )
    requester_administrators = (
        await administrators.fn_list_requester_administrators_by_request_id(
            requester_full.id, requester_administrators_repo
        )
    )

    requester_full.administrators = requester_administrators
    return requester_full


async def fn_update_requester_with_administrator(
    id: uuid.UUID,
    update_requester_with_admin: UpdateRequesterWithAdministrator,
    requesters_repo: RequestersRepository,
    requester_administrators_repo: RequesterAdministratorsRepository,
    users_repo: UsersRepository,
    *,
    raise_not_found_exception: bool = True,
    raise_inactive_status_exception: bool = False,
) -> Optional[Requester]:

    requester = await crud.fn_get_requester(
        id,
        requesters_repo,
        raise_not_found_exception=raise_not_found_exception,
        raise_inactive_status_exception=raise_inactive_status_exception,
    )

    update_administrator = update_requester_with_admin.administrator
    update_requester_with_admin = update_requester_with_admin.dict()
    del update_requester_with_admin["administrator"]

    # Check for requester email update
    if requester.email != update_requester_with_admin["email"]:
        update_email = update_requester_with_admin["email"]
        _ = await validator.fn_email_not_exists_in_requesters(
            update_email, requesters_repo
        )

    # Check for Administrator email update
    requester_administrators_list = (
        await administrators.fn_list_requester_administrators_by_request_id(
            requester.id, requester_administrators_repo
        )
    )
    administrators_email = [
        administratior.email for administratior in requester_administrators_list
    ]
    # If the email is not in the list, it means that the administrator's email is to be updated
    if update_administrator.email not in administrators_email:
        update_email = update_administrator.email
        _ = await fn_email_exists_in_users(update_email, users_repo)

    update_prequester = UpdateRequester(**update_requester_with_admin)

    _ = await crud.fn_update_requester(requester.id, update_prequester, requesters_repo)

    _ = await administrators.fn_update_requester_administrator(
        update_administrator, requester.id, requester_administrators_repo
    )

    requester_full = await fn_get_requester_full(
        id=requester.id,
        requesters_repo=requesters_repo,
        requester_administrators_repo=requester_administrators_repo,
    )

    updated_record = await fn_update_user_email(
        update_administrator.email, requester.id, users_repo
    )
    # if updated_record:
    #     await fn_send_verification_email(updated_record.id, update_administrator.email)

    return requester_full
