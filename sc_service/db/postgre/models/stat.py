from sqlalchemy import Column, DATE, Integer, BigInteger

from sc_service.db import Base


class DBStat(Base):
    __tablename__ = "stat"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    date = Column(DATE)
    views = Column(Integer, nullable=True)
    clicks = Column(Integer, nullable=True)
    cost = Column(Integer, nullable=True)
