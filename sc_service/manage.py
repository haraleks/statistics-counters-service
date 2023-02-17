import argparse
import asyncio
import os

from alembic import command
from alembic.config import Config

from sc_service.settings import app_config

ALEMBIC_CONFIG = Config(f"{os.path.dirname(os.path.abspath(__file__))}/alembic.ini")
ALEMBIC_CONFIG.set_main_option(
    "sqlalchemy.url", f"{app_config.uri_postgresql}/{app_config.db_name}"
)


async def db_upgrade(alembic_config=None):
    if alembic_config is None:
        alembic_config = ALEMBIC_CONFIG
    command.upgrade(alembic_config, "head")


async def db_downgrade(alembic_config=None):
    if alembic_config is None:
        alembic_config = ALEMBIC_CONFIG
    command.downgrade(alembic_config, "base")


async def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="namespace", required=True)

    parser_db = subparsers.add_parser(
        "db",
        help="Synchronizes the database state with the current set of models and migrations.",
    )
    db_subparsers = parser_db.add_subparsers(dest="command", required=True)

    db_subparsers.add_parser("upgrade", help="Upgrade to a later version.")
    db_subparsers.add_parser("downgrade", help="Revert to a previous version.")

    args = parser.parse_args()

    await globals()[f"{args.namespace}_{args.command}"](args)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
