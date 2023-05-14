import os
from distutils.util import strtobool
from typing import List, Optional

from pydantic import BaseSettings

INIT_API_VERSION = "0.0.1"
INIT_API_ALGORITHM = "HS256"
INIT_API_ACCESS_TOKEN_EXPIRY = 3600
INIT_APPLICATION_ID = "team-beta-duro"
INIT_APPLICATION_NAMESPACE = "duro"


class GlobalConfig(BaseSettings):
    """Global configurations."""

    ENV_STATE: Optional[str] = os.environ.get("ENV_STATE", "dev")

    SECRET_KEY: Optional[str] = os.environ.get("SECRET_KEY", None)
    POSTGRES_USER: Optional[str] = os.environ.get("POSTGRES_USER", None)
    POSTGRES_PASSWORD: Optional[str] = os.environ.get("POSTGRES_PASSWORD", None)
    POSTGRES_OP_USER: Optional[str] = os.environ.get("POSTGRES_OP_USER", None)
    POSTGRES_OP_PASSWORD: Optional[str] = os.environ.get("POSTGRES_OP_PASSWORD", None)
    POSTGRES_SERVER: Optional[str] = os.environ.get("POSTGRES_SERVER", None)
    POSTGRES_PORT: Optional[str] = os.environ.get("POSTGRES_PORT", None)
    POSTGRES_DB: Optional[str] = os.environ.get("POSTGRES_DB", None)
    APPLICATION_ID: Optional[str] = os.environ.get("APPLICATION_ID", INIT_APPLICATION_ID)
    APPLICATION_CALLBACK_URL: Optional[str] = os.environ.get(
        "APPLICATION_CALLBACK_URL", ""
    )
    API_VERSION: Optional[str] = os.environ.get("API_VERSION", INIT_API_VERSION)
    API_ALGORITHM: Optional[str] = os.environ.get("API_ALGORITHM", INIT_API_ALGORITHM)
    API_ACCESS_TOKEN_EXPIRY: Optional[int] = os.environ.get(
        "API_ACCESS_TOKEN_EXPIRY", INIT_API_ACCESS_TOKEN_EXPIRY
    )
    APPLICATION_NAMESPACE: Optional[str] = os.environ.get(
        "APPLICATION_NAMESPACE", INIT_APPLICATION_NAMESPACE
    )
    APPLICATION_ROOT: Optional[str] = os.environ.get(
        "APPLICATION_ROOT", "http://localhost:3000"
    )
    APPLICATION_NAME: Optional[str] = os.environ.get(
        "APPLICATION_NAME", "duro"
    )
    APPLICATION_LOGO: Optional[str] = os.environ.get("APPLICATION_LOGO", "")

    MAILER_FROM: Optional[str] = os.environ.get("MAILER_FROM", "root@localhost")
    IP_LOGGING: bool = strtobool(os.environ.get("IP_LOGGING", "False"))

    # SES Email
    AWS_ACCESS_KEY_ID: Optional[str] = os.environ.get("AWS_ACCESS_KEY_ID", None)
    AWS_SECRET_ACCESS_KEY: Optional[str] = os.environ.get("AWS_SECRET_ACCESS_KEY", None)
    AWS_REGION: Optional[str] = os.environ.get("AWS_REGION", None)
    SENDER_NAME: Optional[str] = os.environ.get("SENDER_NAME", "Duro")
    SENDER_EMAIL: Optional[str] = os.environ.get("SENDER_EMAIL", None)

    
app_config = GlobalConfig()
# print(config.__repr__())
