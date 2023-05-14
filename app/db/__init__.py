import os

from databases import Database
from fastapi import FastAPI
from loguru import logger

from app.core.global_config import app_config


async def connect_to_db(app: FastAPI) -> None:
    db_username, db_password = (app_config.POSTGRES_USER, app_config.POSTGRES_PASSWORD)
    # db_username, db_password = (
    #     (app_config.POSTGRES_OP_USER, app_config.POSTGRES_OP_PASSWORD)
    #     if app_config.POSTGRES_OP_USER
    #     else (app_config.POSTGRES_USER, app_config.POSTGRES_PASSWORD)
    # )
    database_url = (
        f"postgresql+asyncpg://{db_username}:{db_password}@{app_config.POSTGRES_SERVER}"
        f":{app_config.POSTGRES_PORT}/{app_config.POSTGRES_DB}"
    )
    if os.environ.get("TEST"):
        database_url += "_test"

    database = Database(
        database_url, min_size=2, max_size=10
    )  # these can be app_configured in app_config as well
    try:
        await database.connect()
        app.state.db = database
        logger.info(
            "--- DB CONNECTION ESTABLISHED TO {}---".format(app_config.POSTGRES_SERVER)
        )
    except Exception as e:
        logger.warning("--- DB CONNECTION ERROR ---")
        logger.warning(e)
        logger.warning("--- DB CONNECTION ERROR ---")


async def close_db_connection(app: FastAPI) -> None:
    try:
        await app.state.db.disconnect()
    except Exception as e:
        logger.warning("--- DB DISCONNECT ERROR ---")
        logger.warning(e)
        logger.warning("--- DB DISCONNECT ERROR ---")
