import random
import string
import uuid
from typing import Optional

from app.db.base import BaseRepository
from app.models.core import DeletedCount, IDModelMixin, UpdatedRecord
from app.models.domains.platform_user import PlatformUser, PlatformUserRoleTypeEnum

GET_USER_SQL = """
    SELECT id, email, is_active, is_verified, role_type FROM users WHERE email=:email;
"""

NEW_USER_SQL = """
    INSERT INTO users (email, hashed_password, is_active, is_verified, is_superuser, role_type, role_reference_id)
    VALUES (:email, crypt(:password, gen_salt('bf', 10)), true, false, false, :role_type, :role_reference_id)
    RETURNING id;
"""

UPDATE_USER_EMAIL_SQL = """
    UPDATE users SET email=:email, updated_at=now(), is_verified=false
    WHERE role_reference_id=:role_reference_id AND email!=:email
    RETURNING id, updated_at;
"""

DELETE_USER_BY_REFERENCE_SQL = """
    DELETE FROM users
    WHERE role_reference_id=:role_reference_id
    RETURNING id;
"""


class UsersRepository(BaseRepository):
    async def get_user(self, *, email: str) -> Optional[PlatformUser]:
        query_values = {
            "email": email,
        }
        user = await self.db.fetch_one(query=GET_USER_SQL, values=query_values)
        return None if user is None else PlatformUser(**user)

    async def create_user(
        self,
        *,
        email: str,
        role_type: PlatformUserRoleTypeEnum,
        role_reference_id: uuid.UUID
    ) -> IDModelMixin:
        query_values = {
            "email": email,
            "role_type": role_type,
            "password": "".join(
                random.choices(string.ascii_letters + string.digits, k=10)
            ),
            "role_reference_id": role_reference_id,
        }
        created_user = await self.db.fetch_one(query=NEW_USER_SQL, values=query_values)
        return IDModelMixin(**created_user)

    async def update_user_email(
        self, *, email: str, role_reference_id: uuid.UUID
    ) -> UpdatedRecord:
        query_values = {
            "email": email,
            "role_reference_id": role_reference_id,
        }
        record_status = await self.db.fetch_one(
            query=UPDATE_USER_EMAIL_SQL, values=query_values
        )
        return None if record_status is None else UpdatedRecord(**record_status)

    async def delete_users_by_reference(
        self, *, role_reference_id: uuid.UUID
    ) -> DeletedCount:
        query_values = {
            "role_reference_id": role_reference_id,
        }
        deleted_count = await self.db.fetch_one(
            query=DELETE_USER_BY_REFERENCE_SQL, values=query_values
        )
        count = 0 if deleted_count is None else len(deleted_count)
        return DeletedCount(count=count)
