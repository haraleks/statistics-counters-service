from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from sc_service.settings import app_config

Base = declarative_base()


def create_sessions(uri_postgresql: str = None):
    if uri_postgresql is None:
        uri_postgresql = f"{app_config.uri_engine}/{app_config.db_name}"
    engine = create_async_engine(uri_postgresql, echo=True)

    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    return async_session


session = create_sessions()


async def get_db() -> AsyncSession:
    async with session() as db:
        yield db
