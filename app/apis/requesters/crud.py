from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.repositories import RequestersRepository

import uuid
from typing import List, Optional

from app.models.core import DeletedCount, IDModelMixin, UpdatedRecord
from app.models.domains.requester import Requester, RequesterStatusEnum, UpdateRequester
from app.models.entities.corporation import Corporation
from app.models.exceptions.auth_exception import InactiveStatusException
from app.models.exceptions.crud_exception import NotFoundException


async def fn_create_requester(
    new_requester: Corporation, requesters_repo: RequestersRepository
) -> IDModelMixin:
    return await requesters_repo.create_requester(new_requester=new_requester)


async def fn_get_requesters(
    name: Optional[str], requesters_repo: RequestersRepository
) -> List[Requester]:
    return await requesters_repo.get_requesters(name=name)


async def fn_get_requester(
    id: uuid.UUID,
    requesters_repo: RequestersRepository,
    *,
    raise_not_found_exception: bool = False,
    raise_inactive_status_exception: bool = False,
) -> Optional[Requester]:
    requester = await requesters_repo.get_requester(id=id)

    if requester is None:
        if raise_not_found_exception:
            raise NotFoundException(message="Queue Requester not found.")
    else:
        if (
            requester.status == RequesterStatusEnum.inactive
            and raise_inactive_status_exception
        ):
            raise InactiveStatusException()

    return requester


async def fn_delete_requester(
    id: uuid.UUID,
    requesters_repo: RequestersRepository,
    *,
    raise_not_found_exception: bool = True,
) -> DeletedCount:
    deleted_count = await requesters_repo.delete_requester(id=id)
    if deleted_count.count == 0 and raise_not_found_exception:
        raise NotFoundException(message="Queue Requester not found.")

    return deleted_count


async def fn_update_requester(
    id: uuid.UUID,
    update_requester: UpdateRequester,
    requesters_repo: RequestersRepository,
) -> UpdatedRecord:
    return await requesters_repo.update_requester(
        id=id, update_requester=update_requester
    )
