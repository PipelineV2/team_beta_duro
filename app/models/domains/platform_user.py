from enum import Enum

from app.models.core import IDModelMixin


class PlatformUserRoleTypeEnum(str, Enum):
    platform = "platform" # Duro app admin
    requester = "requester" # Duro app client (coperate organization)
    waiting = "waiting" # Duro app person in queue (From coperate organization)


class PlatformUser(IDModelMixin):
    email: str
    is_active: bool
    is_verified: bool
    role_type: PlatformUserRoleTypeEnum
