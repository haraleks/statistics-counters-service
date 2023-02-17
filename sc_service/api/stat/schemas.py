from datetime import date
from typing import Optional, Any

from pydantic import BaseModel, PositiveInt

from sc_service.db.postgre.models import DBStat


class ReqStat(BaseModel):
    date: date
    views: Optional[PositiveInt]
    clicks: Optional[PositiveInt]
    cost: Optional[float]

    def dict(self, *args, **kwargs):
        dct = super().dict(*args, **kwargs)
        if dct.get("cost"):
            dct["cost"] = int(dct.get("cost") * 100)
        return dct


class RespStat(BaseModel):
    id: int
    date: date
    views: Optional[PositiveInt]
    clicks: Optional[PositiveInt]
    cost: Optional[float]

    class Config:
        orm_mode = True

    @staticmethod
    def from_orm(obj: DBStat):
        return RespStat(
            id=obj.id,
            date=obj.date,
            views=obj.views,
            clicks=obj.clicks,
            cost=obj.cost / 100 if obj.cost else 0
        )


class RespAgrStat(BaseModel):
    date: date
    views: Optional[PositiveInt]
    clicks: Optional[PositiveInt]
    cost: Optional[float]
    cpc: Optional[float]
    cpm: Optional[float]

    @staticmethod
    def from_orm(obj: Any):
        return RespAgrStat(
            date=obj.date,
            views=obj.views,
            clicks=obj.clicks,
            cost=obj.cost / 100 if obj.cost else 0,
            cpc=obj.cpc / 100 if obj.cpc else 0,
            cpm=obj.cpm / 100 if obj.cpm else 0,
        )
