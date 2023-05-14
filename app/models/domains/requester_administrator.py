import uuid

from app.models.entities.person import PersonDBModel


class RequesterAdministratorDBModel(PersonDBModel):
    requester_id: uuid.UUID


RequesterAdministrator = RequesterAdministratorDBModel
