import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, Request, status

from app.apis.requesters import (
    fn_create_requester,
    # fn_delete_requester,
    fn_get_requester_full,
    fn_get_requesters,
    fn_update_requester_with_administrator,
)
from app.core import global_state
from app.db.dependency import get_repository
from app.db.repositories import (
    RequesterAdministratorsRepository,
    RequestersRepository,
    UsersRepository,
)
from app.models.core import DeletedCount
from app.models.domains.requester import (
    NewRequester,
    Requester,
    UpdateRequesterWithAdministrator,
)
from app.models.exceptions.crud_exception import DuplicateDataError, NotFoundError

router = APIRouter()
router.prefix = "/api/platform/requesters"

# platform_user = global_state.system_users.current_user(active=True, verified=True)


@router.get(
    "",
    tags=["platform-requesters"],
    name="platform:requesters:list",
    operation_id="platform_requesters_list",
    responses={
        status.HTTP_200_OK: {"model": List[Requester]},
    },
)
async def list(
    request: Request,
    name: Optional[str] = None,
    requesters_repo: RequestersRepository = Depends(
        get_repository(RequestersRepository)
    ),
    #_=Depends(platform_user),
) -> List[Requester]:
    """

    """
    return await fn_get_requesters(name, requesters_repo)


@router.post(
    "",
    tags=["platform-requesters"],
    name="platform:requesters:requester:create",
    operation_id="platform_requesters_requester_create",
    responses={
        status.HTTP_201_CREATED: {"model": Requester},
        status.HTTP_403_FORBIDDEN: {"model": DuplicateDataError},
    },
    status_code=status.HTTP_201_CREATED,
)
async def create_requester(
    request: Request,
    requester: NewRequester,
    requesters_repo: RequestersRepository = Depends(
        get_repository(RequestersRepository)
    ),
    requester_administrators_repo: RequesterAdministratorsRepository = Depends(
        get_repository(RequesterAdministratorsRepository)
    ),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    #_=Depends(platform_user),
) -> Optional[Requester]:
    """

    """
    return await fn_create_requester(
        requester, requesters_repo, requester_administrators_repo, users_repo
    )


@router.get(
    "/{corporate_id}",
    tags=["platform-requesters"],
    name="platform:requesters:requester:get",
    operation_id="platform_requesters_requester_get",
    responses={
        status.HTTP_200_OK: {"model": Requester},
        status.HTTP_404_NOT_FOUND: {"model": NotFoundError},
    },
)
async def get_requester(
    request: Request,
    corporate_id: uuid.UUID,
    requesters_repo: RequestersRepository = Depends(
        get_repository(RequestersRepository)
    ),
    requester_administrators_repo: RequesterAdministratorsRepository = Depends(
        get_repository(RequesterAdministratorsRepository)
    ),
    #_=Depends(platform_user),
) -> Requester:
    """

    """
    return await fn_get_requester_full(
        corporate_id,
        requesters_repo,
        requester_administrators_repo,
        raise_not_found_exception=True,
    )


# @router.delete(
#     "/{corporate_id}",
#     tags=["platform-requesters"],
#     name="platform:requesters:requester:delete",
#     operation_id="platform_requesters_requester_delete",
#     responses={
#         status.HTTP_200_OK: {"model": DeletedCount},
#     },
# )
# async def delete_requester(
#     request: Request,
#     corporate_id: uuid.UUID,
#     requesters_repo: RequestersRepository = Depends(
#         get_repository(RequestersRepository)
#     ),
#     users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
#     #_=Depends(platform_user),
# ) -> DeletedCount:
#     """

#     """
#     return await fn_delete_requester(corporate_id, requesters_repo, users_repo)


@router.put(
    "/{corporate_id}",
    tags=["platform-requesters"],
    name="platform:requesters:requester:update",
    operation_id="platform_requesters_requester_update",
    responses={
        status.HTTP_200_OK: {"model": Requester},
        status.HTTP_404_NOT_FOUND: {"model": NotFoundError},
    },
)
async def update_requester_with_administrator(
    request: Request,
    corporate_id: uuid.UUID,
    updated_requester_with_admin: UpdateRequesterWithAdministrator,
    requesters_repo: RequestersRepository = Depends(
        get_repository(RequestersRepository)
    ),
    requester_administrators_repo: RequesterAdministratorsRepository = Depends(
        get_repository(RequesterAdministratorsRepository)
    ),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    #_=Depends(platform_user),
) -> Optional[Requester]:
    """

    """
    return await fn_update_requester_with_administrator(
        corporate_id,
        updated_requester_with_admin,
        requesters_repo,
        requester_administrators_repo,
        users_repo,
    )
