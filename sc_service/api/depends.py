from fastapi import Depends

from sc_service.db.postgre.pg import get_db
from sc_service.db.postgre.storage.stat import StatStoragePG


def get_stat_storage_pg(db=Depends(get_db)) -> StatStoragePG:
    return StatStoragePG(db)
