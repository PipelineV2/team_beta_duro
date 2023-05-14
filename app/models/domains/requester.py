from enum import Enum
from typing import List, Optional

from app.models.core import CoreModel
from app.models.domains.requester_administrator import RequesterAdministrator
from app.models.entities.corporation import Corporation, CorporationDBModel
from app.models.entities.person import PersonBase


class RequesterStatusEnum(str, Enum):
    active = "active"
    inactive = "inactive"


class NewRequester(CoreModel):
    corporation: Corporation
    administrator: PersonBase


class Requester(CorporationDBModel):
    administrators: Optional[List[RequesterAdministrator]]
    status: RequesterStatusEnum


class UpdateRequester(Corporation):
    status: RequesterStatusEnum


class UpdateRequesterWithAdministrator(UpdateRequester):
    administrator: PersonBase
