from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.repositories import RequestersRepository

import uuid
from typing import List

from app.models.exceptions.crud_exception import DuplicateDataException


# Check that Requester 'email' does not exists, else raise exception
async def fn_email_not_exists_in_requesters(
    email: str,
    requesters_repo: RequestersRepository,
    *,
    raise_duplicate_data_exception: bool = True,
):
    requester_id = await requesters_repo.get_requester_id_by_email(email=email)

    if requester_id is not None and raise_duplicate_data_exception:
        raise DuplicateDataException(
            current_record_id=requester_id.id,
            error_code="duplicate-corporate",
            message="A Requester Company with that email already exists.",
        )

    return requester_id is None


async def fn_filter_exists(
    requester_ids: List[uuid.UUID], requesters_repo: RequestersRepository
) -> List[uuid.UUID]:
    return await requesters_repo.filter_exists(requester_ids=requester_ids)
