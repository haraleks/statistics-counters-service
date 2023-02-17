import os
import warnings

import asyncpg
import pytest
from alembic.config import Config
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine

from sc_service.db.postgre.models import metadata
from sc_service.db.postgre.pg import session
from sc_service.manage import db_upgrade
from sc_service.settings import app_config


@pytest.fixture(scope="session", autouse=True)
async def create_or_clean_db():
    engine = create_async_engine(
        f"{app_config.uri_engine}/{app_config.db_name}",
        echo=True,
        isolation_level="AUTOCOMMIT"
    )
    try:
        async with engine.connect() as con:
            await con.run_sync(metadata.drop_all)
            await con.run_sync(metadata.create_all)

    except asyncpg.exceptions.InvalidCatalogNameError:
        engine = create_async_engine(
            f"{app_config.uri_engine}", echo=True, isolation_level="AUTOCOMMIT"
        )
        async with engine.begin() as con:
            await con.run_sync(metadata.create_all)


@pytest.fixture(scope="session")
async def fx_db_pg():
    db = session()
    try:
        yield db
    finally:
        await db.close()


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session", autouse=True)
def test_app() -> FastAPI:
    from sc_service.main import app as app_

    return app_


@pytest.fixture(autouse=True)
async def fx_apply_migrations():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    ALEMBIC_CONFIG_TEST = Config(
        f"{os.path.dirname(os.path.abspath(__file__))[:-6]}/alembic.ini"
    )
    ALEMBIC_CONFIG_TEST.set_main_option(
        "sqlalchemy.url", f"{app_config.uri_postgresql}/{app_config.db_name}"
    )

    await db_upgrade(ALEMBIC_CONFIG_TEST)
    yield


@pytest.fixture(scope="session")
async def fx_client(test_app: FastAPI) -> AsyncClient:
    kwargs = {
        "app": test_app,
        "base_url":"http://testserver",
        "headers": {
            "SECURE-TOKEN": app_config.secure_token
            }
        }

    async with AsyncClient(**kwargs) as client, LifespanManager(test_app):
        yield client

@pytest.fixture(scope="session")
async def fx_client_unauth(test_app: FastAPI) -> AsyncClient:
    kwargs = {"app": test_app, "base_url":"http://testserver",}
    async with AsyncClient(**kwargs) as client, LifespanManager(test_app):
        yield client
