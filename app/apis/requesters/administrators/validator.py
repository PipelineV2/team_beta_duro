from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.repositories import RequesterAdministratorsRepository

from app.models.exceptions.crud_exception import DuplicateDataException


# Check that Administrator 'email' does not exists, else raise exception
async def fn_email_not_exists_in_requester_administrators(
    email: str,
    requester_administrators_repo: RequesterAdministratorsRepository,
    *,
    raise_duplicate_data_exception: bool = True,
):
    requester_administrator_id = (
        await requester_administrators_repo.get_requester_administrator_id_by_email(
            email=email
        )
    )

    if requester_administrator_id is not None and raise_duplicate_data_exception:
        raise DuplicateDataException(
            current_record_id=requester_administrator_id.id,
            error_code="duplicate-administrator",
            message="An Administrator with that email already exists.",
        )

    return requester_administrator_id is None
