from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.repositories import UsersRepository

from app.core.global_config import app_config
from app.models.core import BooleanResponse, DeletedCount, IDModelMixin, UpdatedRecord
from app.models.domains.platform_user import PlatformUserRoleTypeEnum
from app.models.exceptions.crud_exception import DuplicateDataException
from app.modules.mailer.mailer import send_mail_with_template


async def fn_email_exists_in_users(
    email: str,
    users_repo: UsersRepository,
    *,
    raise_duplicate_data_exception: bool = True,
) -> BooleanResponse:
    user = await users_repo.get_user(email=email)
    if user is not None and raise_duplicate_data_exception:
        raise DuplicateDataException(
            current_record_id=user.id,
            error_code="duplicate-administrator",
            message="An Administrator with that email already exists.",
        )

    return user is not None


async def fn_create_user(
    email: str,
    role_type: PlatformUserRoleTypeEnum,
    role_reference_id: uuid.UUID,
    users_repo: UsersRepository,
) -> IDModelMixin:
    return await users_repo.create_user(
        email=email, role_type=role_type, role_reference_id=role_reference_id
    )


async def fn_update_user_email(
    email: str,
    role_reference_id: uuid.UUID,
    users_repo: UsersRepository,
) -> UpdatedRecord:
    return await users_repo.update_user_email(
        email=email, role_reference_id=role_reference_id
    )


