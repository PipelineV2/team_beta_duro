import uuid
from typing import List, Optional

from app.db.base import BaseRepository
from app.db.repositories.helpers.crud_helper import delete_by_id
from app.models.core import DeletedCount, IDModelMixin, UpdatedRecord
from app.models.domains.requester import Requester, UpdateRequester
from app.models.entities.corporation import Corporation

NEW_REQUESTER_SQL = """
    INSERT INTO requesters(email, name, description, legal_name, duns, telephone, url, tax_id, vat_id)
    VALUES(:email, :name, :description, :legal_name, :duns, :telephone, :url, :tax_id, :vat_id)
    RETURNING id;
"""

LIST_REQUESTERS_SQL = """
    SELECT * FROM requesters;
"""

LIST_FILTERED_REQUESTERS_SQL = """
    SELECT * FROM requesters WHERE name ilike '%{}%';
"""

GET_REQUESTER_SQL = """
    SELECT * FROM requesters WHERE id=:id;
"""

GET_REQUESTER_ID_BY_EMAIL_SQL = """
    SELECT id FROM requesters WHERE email=:email;
"""

DELETE_REQUESTER_SQL = """
    DELETE FROM requesters WHERE id=:id RETURNING id;
"""

FILTER_EXISTS_SQL = """
    SELECT id FROM requesters WHERE id in ({requester_ids});
"""

UPDATE_REQUESTER_SQL = """
    UPDATE requesters
    SET
    email=:email,
    name=:name,
    description=:description,
    legal_name=:legal_name,
    duns=:duns,
    telephone=:telephone,
    url=:url,
    tax_id=:tax_id,
    vat_id=:vat_id,
    status=:status,
    updated_at=now()
    WHERE id=:id
    RETURNING id, updated_at;
"""


class RequestersRepository(BaseRepository):
    async def create_requester(self, *, new_requester: Corporation) -> IDModelMixin:
        query_values = new_requester.dict()
        created_requester = await self.db.fetch_one(
            query=NEW_REQUESTER_SQL, values=query_values
        )
        return IDModelMixin(**created_requester)

    async def get_requesters(self, *, name: Optional[str]) -> List[Requester]:
        query = (
            LIST_REQUESTERS_SQL
            if name is None
            else LIST_FILTERED_REQUESTERS_SQL.format(name)
        )
        requesters = await self.db.fetch_all(query=query, values={})
        return [Requester(**requester) for requester in requesters]

    async def get_requester(self, *, id: uuid.UUID) -> Optional[Requester]:
        query_values = {"id": id}
        requester = await self.db.fetch_one(
            query=GET_REQUESTER_SQL, values=query_values
        )
        return None if requester is None else Requester(**requester)

    async def get_requester_id_by_email(self, *, email: str) -> Optional[IDModelMixin]:
        query_values = {"email": email}
        requester = await self.db.fetch_one(
            query=GET_REQUESTER_ID_BY_EMAIL_SQL, values=query_values
        )
        return None if requester is None else IDModelMixin(**requester)

    async def delete_requester(self, *, id: uuid.UUID) -> DeletedCount:
        return await delete_by_id(id, DELETE_REQUESTER_SQL, self.db)

    # returns a list of uuids where record exists in table
    async def filter_exists(self, *, requester_ids: List[uuid.UUID]) -> List[uuid.UUID]:
        requester_ids_array = ", ".join(
            ["'{}'".format(str(requester_id)) for requester_id in requester_ids]
        )
        filtered_ids = await self.db.fetch_all(
            query=FILTER_EXISTS_SQL.format(requester_ids=requester_ids_array)
        )
        return [IDModelMixin(**filtered_id).id for filtered_id in filtered_ids]

    async def update_requester(
        self,
        *,
        id: uuid.UUID,
        update_requester: UpdateRequester,
    ) -> UpdatedRecord:
        query_values = update_requester.dict()
        query_values["id"] = id
        requester = await self.db.fetch_one(
            query=UPDATE_REQUESTER_SQL, values=query_values
        )
        return None if requester is None else UpdatedRecord(**requester)
