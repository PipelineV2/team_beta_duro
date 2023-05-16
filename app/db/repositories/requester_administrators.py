import uuid
from typing import List, Optional

from app.db.base import BaseRepository
from app.models.core import IDModelMixin
from app.models.domains.requester_administrator import RequesterAdministrator
from app.models.entities.person import PersonBase

NEW_REQUESTER_ADMINISTRATOR_SQL = """
    INSERT INTO requester_administrators(email, given_name, family_name, display_name, telephone, job_title, requester_id)
    VALUES(:email, :given_name, :family_name, :display_name, :telephone, :job_title, :requester_id)
    RETURNING id;
"""

LIST_REQUESTER_ADMINISTRATORS_BY_REQUEST_ID_SQL = """
    SELECT * FROM requester_administrators WHERE requester_id=:requester_id;
"""

GET_REQUESTER_ADMINISTRATOR_ID_BY_EMAIL_SQL = """
    SELECT id FROM requester_administrators WHERE email=:email;
"""

UPDATE_REQUESTER_ADMINISTRATOR_SQL = """
    UPDATE requester_administrators
    SET
    email=:email,
    given_name=:given_name,
    family_name=:family_name,
    display_name=:display_name,
    telephone=:telephone,
    job_title=:job_title,
    updated_at=now()
    WHERE requester_id=:requester_id
    RETURNING requester_id, updated_at;
"""


class RequesterAdministratorsRepository(BaseRepository):
    async def create_requester_administrator(
        self, *, new_administrator: PersonBase, requester_id: uuid.UUID
    ) -> IDModelMixin:
        query_values = new_administrator.dict()
        query_values["requester_id"] = requester_id
        created_requester_administrator = await self.db.fetch_one(
            query=NEW_REQUESTER_ADMINISTRATOR_SQL, values=query_values
        )
        return IDModelMixin(**created_requester_administrator)

    async def list_requester_administrators_by_request_id(
        self, *, requester_id: uuid.UUID
    ) -> List[RequesterAdministrator]:
        query_values = {"requester_id": requester_id}
        requester_administrators = await self.db.fetch_all(
            query=LIST_REQUESTER_ADMINISTRATORS_BY_REQUEST_ID_SQL, values=query_values
        )
        
        admins = [
            RequesterAdministrator(**requester_administrator)
            for requester_administrator in requester_administrators
        ]
        
        return admins
    
    async def get_requester_administrator_id_by_email(
        self, *, email: str
    ) -> Optional[IDModelMixin]:
        query_values = {"email": email}
        requester_administrator = await self.db.fetch_one(
            query=GET_REQUESTER_ADMINISTRATOR_ID_BY_EMAIL_SQL, values=query_values
        )
        return (
            None
            if requester_administrator is None
            else IDModelMixin(**requester_administrator)
        )

    async def update_requester_administrator(
        self, *, update_administrator: PersonBase, requester_id: uuid.UUID
    ) -> IDModelMixin:
        query_values = update_administrator.dict()
        query_values["requester_id"] = requester_id
        updated_requester_administrator = await self.db.fetch_one(
            query=UPDATE_REQUESTER_ADMINISTRATOR_SQL, values=query_values
        )
        return IDModelMixin(**updated_requester_administrator)
