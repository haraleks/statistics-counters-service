from sc_service.db import Base
from .stat import DBStat

metadata = Base.metadata

__all__ = [
    "DBStat",
    "metadata",
]