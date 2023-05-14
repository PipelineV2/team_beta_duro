from fastapi import APIRouter, Depends, Request, status

from app.apis.requesters import fn_get_requester
from app.apis.requesters.api_keys import fn_get_inbound_requester_api_key
from app.clients import auth_helper
from app.db.dependency import get_repository
from app.db.repositories import RequesterApiKeysRepository, RequestersRepository
from app.models.entities.webapi import BearerAccessToken
from app.security.oauth2_client_form import OAuth2ClientForm
from app.security.requester_auth import get_requester

router = APIRouter()
router.prefix = "/api/requester/auth"


@router.post(
    "/login",
    tags=["requester-auth"],
    name="requester:auth:login",
    operation_id="requester_auth_login",
    responses={status.HTTP_200_OK: {"model": BearerAccessToken}},
)
async def login(
    request: Request,
    credentials: OAuth2ClientForm = Depends(),
    requesters_repo: RequestersRepository = Depends(
        get_repository(RequestersRepository)
    ),
    requester_api_keys_repo: RequesterApiKeysRepository = Depends(
        get_repository(RequesterApiKeysRepository)
    ),
) -> BearerAccessToken:
   
    client_id = credentials.client_id

    requester_api_key = await fn_get_inbound_requester_api_key(
        client_id, requester_api_keys_repo
    )

    await fn_get_requester(
        requester_api_key.requester_id,
        requesters_repo,
        raise_not_found_exception=True,
        raise_inactive_status_exception=True,
    )

    await auth_helper.check_client_secret(
        credentials.client_secret, requester_api_key.client_secret
    )

    access_token = auth_helper.generate_jwt_token(
        client_id, requester_api_key.client_secret
    )
    return BearerAccessToken(
        access_token=access_token, identifier=requester_api_key.requester_id
    )


@router.get(
    "/test/token",
    tags=["requester-auth"],
    name="requester:auth:test:token",
    operation_id="requester_auth_test_token",
)
async def test_token(request: Request, auth=Depends(get_requester)):
    requester, *_ = auth

    return requester
