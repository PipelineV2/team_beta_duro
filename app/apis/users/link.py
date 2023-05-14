from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.repositories import RequesterDuroUsersRepository

import uuid

from app.models.core import BooleanResponse, DeletedCount, UpdatedRecord


async def fn_link_requester_to_duro_user(
    requester_id: uuid.UUID,
    duro_user_id: uuid.UUID,
    requester_duro_users_repo: RequesterDuroUsersRepository,
) -> UpdatedRecord:
    return await requester_duro_users_repo.link_requester_to_duro_user(
        requester_id=requester_id, duro_user_id=duro_user_id
    )


async def fn_unlink_requester_from_duro_user(
    requester_id: uuid.UUID,
    duro_user_id: uuid.UUID,
    requester_duro_users_repo: RequesterDuroUsersRepository,
) -> DeletedCount:
    return (
        await requester_duro_users_repo.unlink_requester_from_duro_user(
            requester_id=requester_id, duro_user_id=duro_user_id
        )
    )


async def fn_requester_duro_user_exists(
    requester_id: uuid.UUID,
    duro_user_id: uuid.UUID,
    requester_duro_users_repo: RequesterDuroUsersRepository,
) -> BooleanResponse:
    return await requester_duro_users_repo.requester_duro_user_exists(
        requester_id=requester_id, duro_user_id=duro_user_id
    )


async def fn_duro_user_has_links(
    duro_user_id: uuid.UUID,
    requester_duro_users_repo: RequesterDuroUsersRepository,
) -> BooleanResponse:
    return await requester_duro_users_repo.duro_user_has_links(
        duro_user_id=duro_user_id
    )
