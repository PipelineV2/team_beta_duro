from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.repositories import RequesterAdministratorsRepository

import uuid
from typing import List

from app.models.core import IDModelMixin
from app.models.domains.requester_administrator import RequesterAdministrator
from app.models.entities.person import PersonBase


async def fn_create_requester_administrator(
    new_administrator: PersonBase,
    requester_id: uuid.UUID,
    requester_administrators_repo: RequesterAdministratorsRepository,
) -> IDModelMixin:
    return await requester_administrators_repo.create_requester_administrator(
        new_administrator=new_administrator,
        requester_id=requester_id,
    )


async def fn_list_requester_administrators_by_request_id(
    requester_id: uuid.UUID,
    requester_administrators_repo: RequesterAdministratorsRepository,
) -> List[RequesterAdministrator]:
    return (
        await requester_administrators_repo.list_requester_administrators_by_request_id(
            requester_id=requester_id
        )
    )


async def fn_update_requester_administrator(
    update_administrator: PersonBase,
    requester_id: uuid.UUID,
    requester_administrators_repo: RequesterAdministratorsRepository,
) -> IDModelMixin:
    return await requester_administrators_repo.update_requester_administrator(
        update_administrator=update_administrator,
        requester_id=requester_id,
    )
