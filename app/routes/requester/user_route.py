import uuid
from enum import Enum
from typing import List, Optional, Union

from fastapi import APIRouter, Depends, Request, Response, status

from app.apis.users import (
    fn_activate_duro_user,
    fn_create_duro_user,
    # fn_delete_duro_user,
    fn_get_duro_user,
    fn_get_duro_users,
    # fn_inactivate_duro_user,
    # fn_link_requester_to_duro_user,
    # fn_unlink_requester_from_duro_user,
)

from app.db.dependency import get_repository
from app.db.repositories import (
    DuroUsersRepository,
    UsersRepository,
    RequestersRepository,
)
from app.models.core import DeletedCount, RecordStatus, UpdatedRecord
from app.models.domains.duro_user import DuroUser
from app.models.entities.core.email import Email
from app.models.exceptions.crud_exception import (
    DuplicateAccountError,
    InvalidStateError,
    NotFoundError,
)
# This will enable us authenticate requesters via Oauth2 and JWT authentication/authorization method
# from app.security.requester_auth import get_requester 

router = APIRouter()
router.prefix = f"/api/requester"


class StatusActionEnum(str, Enum):
    activate = "activate"
    inactivate = "inactivate"


class LinkActionEnum(str, Enum):
    link = "link"
    unlink = "unlink"


@router.get(
    "/{requester_id}/users",
    tags=["requester-users"],
    name="requester:users:list",
    operation_id="requester_users_list",
    responses={status.HTTP_200_OK: {"model": List[DuroUser]}},
)
async def get_users(
    request: Request,
    requester_id: uuid.UUID,
    duro_users_repo: DuroUsersRepository = Depends(
        get_repository(DuroUsersRepository)
    ),
    # auth=Depends(get_requester),
) -> List[DuroUser]:
    return await fn_get_duro_users(requester_id, duro_users_repo)


@router.post(
    "/{requester_id}/users",
    tags=["requester-users"],
    name="requester:users:create",
    operation_id="requester_users_create",
    responses={
        status.HTTP_201_CREATED: {"model": DuroUser},
        status.HTTP_403_FORBIDDEN: {"model": DuplicateAccountError},
    },
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    request: Request,
    requester_id: uuid.UUID,
    email: Email,
    autolink: Optional[bool] = None,
    requesters_repo: RequestersRepository = Depends(
        get_repository(RequestersRepository)
    ),
    duro_users_repo: DuroUsersRepository = Depends(
        get_repository(DuroUsersRepository)
    ),
    requester_duro_users_repo: UsersRepository = Depends(
        get_repository(UsersRepository)
    ),
   
    # auth=Depends(get_requester),
) -> DuroUser:
    """

    """

    # requester, *_ = auth

    user_id = await fn_create_duro_user(
        requester_id, email, duro_users_repo
    )
    # if autolink:
    #     await fn_link_requester_to_duro_user(
    #         requester_id,
    #         user_id,
    #         requesters_repo,
    #         duro_users_repo,
    #         requester_duro_users_repo,
    #     )


    return await fn_get_duro_user(str(user_id), duro_users_repo)


@router.get(
    "/{requester_id}/users/{account_identifier}",
    tags=["requester-users"],
    name="requester:users:get",
    operation_id="requester_users_get",
    responses={
        status.HTTP_200_OK: {"model": DuroUser},
        status.HTTP_404_NOT_FOUND: {"model": NotFoundError},
    },
)
async def get_user(
    request: Request,
    requester_id: uuid.UUID,
    account_identifier: str,
    duro_users_repo: DuroUsersRepository = Depends(
        get_repository(DuroUsersRepository)
    ),
    # auth=Depends(get_requester),
) -> DuroUser:
    """
    """
    return await fn_get_duro_user(account_identifier, duro_users_repo)


# @router.delete(
#     "/{requester_id}/{user_id}",
#     tags=["requester-users"],
#     name="requester:users:delete",
#     operation_id="requester_users_delete",
#     responses={
#         status.HTTP_200_OK: {"model": DeletedCount},
#         status.HTTP_404_NOT_FOUND: {"model": NotFoundError},
#         status.HTTP_409_CONFLICT: {"model": InvalidStateError},
#     },
# )
# async def delete_user(
#     request: Request,
#     requester_id: uuid.UUID,
#     user_id: uuid.UUID,
#     autounlink: Optional[bool] = None,
#     requesters_repo: RequestersRepository = Depends(
#         get_repository(RequestersRepository)
#     ),
#     duro_users_repo: DuroUsersRepository = Depends(
#         get_repository(DuroUsersRepository)
#     ),
#     requester_duro_users_repo: UsersRepository = Depends(
#         get_repository(UsersRepository)
#     ),
#     # auth=Depends(get_requester),
# ) -> DeletedCount:
#     """
#     """
#     # requester, *_ = auth
#     if autounlink:
#         await fn_unlink_requester_from_duro_user(
#             requester_id,
#             user_id,
#             requesters_repo,
#             duro_users_repo,
#             requester_duro_users_repo,
#         )

#     return await fn_delete_duro_user(
#         user_id,
#         duro_users_repo,
#         requester_duro_users_repo,
#     )


# @router.get(
#     "/{user_id}/status/{status_action}",
#     tags=["requester-users"],
#     name="requester:users:status:activate_inactivate",
#     operation_id="requester_users_status_activate_inactivate",
#     responses={
#         status.HTTP_200_OK: {"model": RecordStatus},
#         status.HTTP_404_NOT_FOUND: {"model": NotFoundError},
#         status.HTTP_409_CONFLICT: {"model": InvalidStateError},
#     },
# )
# async def update_user_status(
#     request: Request,
#     user_id: uuid.UUID,
#     status_action: StatusActionEnum,
#     duro_users_repo: DuroUsersRepository = Depends(
#         get_repository(DuroUsersRepository)
#     ),
#     requester_duro_users_repo: UsersRepository = Depends(
#         get_repository(UsersRepository)
#     ),
#     # auth=Depends(get_requester),
# ) -> RecordStatus:
#     """

#     """
#     return (
#         await fn_activate_duro_user(
#             user_id,
#             duro_users_repo,
#         )
#         if status_action == StatusActionEnum.activate
#         else await fn_inactivate_duro_user(
#             user_id,
#             duro_users_repo,
#             requester_duro_users_repo,
#         )
#     )


# @router.get(
#     "/{user_id}/{link_action}",
#     tags=["requester-users"],
#     name="requester:users:link",
#     operation_id="requester_users_link",
#     responses={
#         status.HTTP_200_OK: {"model": Union[UpdatedRecord, DeletedCount]},
#         status.HTTP_201_CREATED: {"model": UpdatedRecord},
#         status.HTTP_404_NOT_FOUND: {"model": NotFoundError},
#         status.HTTP_409_CONFLICT: {"model": InvalidStateError},
#     },
# )
# async def update_user_link(
#     request: Request,
#     response: Response,
#     user_id: uuid.UUID,
#     link_action: LinkActionEnum,
#     requesters_repo: RequestersRepository = Depends(
#         get_repository(RequestersRepository)
#     ),
#     duro_users_repo: DuroUsersRepository = Depends(
#         get_repository(DuroUsersRepository)
#     ),
#     requester_duro_users_repo: UsersRepository = Depends(
#         get_repository(UsersRepository)
#     ),

#     # auth=Depends(get_requester),
# ) -> Union[UpdatedRecord, DeletedCount]:
#     """
  
#     """
#     # requester, *_ = auth

#     if link_action == LinkActionEnum.link:
#         link_record = await fn_link_requester_to_duro_user(
#             requester.id,
#             user_id,
#             requesters_repo,
#             duro_users_repo,
#             requester_duro_users_repo,
#         )

#         response.status_code = (
#             status.HTTP_201_CREATED
#             if link_record.updated_at is None
#             else status.HTTP_200_OK
#         )
#         return link_record
#     else:
#         return await fn_unlink_requester_from_duro_user(
#             requester.id,
#             user_id,
#             requesters_repo,
#             duro_users_repo,
#             requester_duro_users_repo,
#         )
