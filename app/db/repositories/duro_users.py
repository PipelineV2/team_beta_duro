import uuid
from typing import List, Optional

from app.db.base import BaseRepository
from app.db.repositories.helpers.crud_helper import delete_by_id
from app.models.core import DeletedCount, IDModelMixin, RecordStatus, UpdatedRecord
from app.models.domains.duro_user import (
    DuroUser,
    DuroUserStatusEnum,
    NewDuroUser,
)

NEW_Duro_USER_SQL = """
    INSERT INTO users(email, telephone, hashed_password, is_active, is_superuser, is_verified, role_reference_id)
    VALUES(:email, :telephone, :hashed_password, :is_active, :is_superuser, :is_verified, :role_reference_id)
    RETURNING id;
"""

LIST_Duro_USERS_SQL = """
    SELECT id, email, telephone,  created_at, updated_at, deleted_at, role_reference_id
    FROM users WHERE role_reference_id=:role_reference_id;
"""

GET_Duro_USER_SQL = """
    SELECT id, email, telephone, created_at, updated_at, deleted_at FROM users WHERE id=:id;
"""

GET_Duro_USER_BY_EMAIL_SQL = """
    SELECT id, email, telephone, created_at, updated_at, deleted_at FROM users WHERE email=:email;
"""

DELETE_Duro_USER_SQL = """
    DELETE FROM users WHERE id=:id RETURNING id;
"""


SET_Duro_USER_VERIFIED_SQL = """
    UPDATE users SET now(), updated_at=now() WHERE id=:id RETURNING id, updated_at;
"""


class DuroUsersRepository(BaseRepository):
    async def create_duro_user(
        self, *, requester_id: uuid.UUID, new_duro_user: NewDuroUser
    ) -> IDModelMixin:
        query_values = new_duro_user.dict()
        query_values["role_reference_id"] = str(requester_id)
        query_values["hashed_password"] = str(requester_id)
        query_values["is_active"] = True
        query_values["is_superuser"] = False
        query_values["is_verified"] = True
        created_Duro_user = await self.db.fetch_one(
            query=NEW_Duro_USER_SQL, values=query_values
        )
        return IDModelMixin(**created_Duro_user)

    async def get_duro_users(self,*, requester_id: uuid.UUID,) -> List[DuroUser]:
        query_values = {"role_reference_id": str(requester_id)}
        duro_users = await self.db.fetch_all(
            query=LIST_Duro_USERS_SQL, values=query_values
        )
        return [
            DuroUser(**duro_user)
            for duro_user in duro_users
        ]

    async def get_duro_user(
        self, *, email: str, status: DuroUserStatusEnum,
    ) -> Optional[DuroUser]:
        query_values = {"email": email}
        return await self._get_duro_user_impl(
            GET_Duro_USER_SQL, query_values
        )

    async def get_duro_user_by_email(
        self, *, email: str, status: DuroUserStatusEnum,
    ) -> Optional[DuroUser]:
        query_values = {"email": email}
        return await self._get_duro_user_impl(
            GET_Duro_USER_BY_EMAIL_SQL, query_values
        )

    async def delete_duro_user(
        self,
        *,
        id: uuid.UUID,
    ) -> DeletedCount:
        return await delete_by_id(id, DELETE_Duro_USER_SQL, self.db)

    async def _get_duro_user_impl(
        self, query: str, query_values: dict
    ) -> Optional[DuroUser]:
        Duro_user = await self.db.fetch_one(query=query, values=query_values)
        return (
            None if Duro_user is None else DuroUser(**Duro_user)
        )

    # async def activate_duro_user(
    #     self, *, id: uuid.UUID
    # ) -> Optional[RecordStatus]:
    #     return await self._set_duro_user_status_impl(
    #         id, DuroUserStatusEnum.active
    #     )

    # async def inactivate_duro_user(
    #     self, *, id: uuid.UUID
    # ) -> Optional[RecordStatus]:
    #     return await self._set_duro_user_status_impl(
    #         id, DuroUserStatusEnum.inactive
    #     )

    # async def _set_duro_user_status_impl(
    #     self,
    #     id: uuid.UUID,
    #     status: DuroUserStatusEnum,
    # ) -> Optional[RecordStatus]:
    #     query_values = {"id": id, "status": status}

    #     record_status = await self.db.fetch_one(
    #         query=SET_Duro_USER_STATUS_SQL, values=query_values
    #     )
    #     return None if record_status is None else RecordStatus(**record_status)

    async def set_duro_user_verified(
        self,
        *,
        id: uuid.UUID,
    ) -> Optional[UpdatedRecord]:
        query_values = {"id": id}

        record_status = await self.db.fetch_one(
            query=SET_Duro_USER_VERIFIED_SQL, values=query_values
        )
        return None if record_status is None else UpdatedRecord(**record_status)
