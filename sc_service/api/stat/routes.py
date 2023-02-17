from datetime import date
from typing import Optional, Literal

from fastapi import APIRouter, Depends
from fastapi_pagination import Page, paginate
from starlette import status

from sc_service.api.depends import get_stat_storage_pg
from sc_service.api.stat.schemas import RespStat, ReqStat, RespAgrStat
from sc_service.db.postgre.models import DBStat
from sc_service.db.postgre.storage.stat import StatStoragePG

router = APIRouter(prefix="/stat")


QUERY_PARAMS_STAT = Literal[
    "date",
    "-date",
    "views",
    "-views",
    "clicks",
    "-clicks",
    "cost",
    "-cost",
    "cpc",
    "-cpc",
    "cpm",
    "-cpm"
]


@router.post(
    "",
    tags=["stat"],
    summary="Save statistics",
    response_model=RespStat,
    status_code=status.HTTP_201_CREATED,
)
async def create_stat(
        req: ReqStat,
        stat_storage: StatStoragePG = Depends(get_stat_storage_pg),
):
    obj = await stat_storage.insert_one(obj=DBStat(**req.dict(exclude_unset=True)))
    return RespStat.from_orm(obj)


@router.get(
    "",
    tags=["stat"],
    summary="Show statistics",
    response_model=Page[RespAgrStat],
    status_code=status.HTTP_200_OK
)
async def get_stat(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        orders: QUERY_PARAMS_STAT = None,
        limit: Optional[str] = None,
        offset: Optional[str] = None,
        stat_storage: StatStoragePG = Depends(get_stat_storage_pg),
):
    filters = {}
    if date_from:
        filters.update({"date_from": date_from})
    if date_to:
        filters.update({"date_to": date_to})
    objs = await stat_storage.get_many(
        date_from=date_from,
        date_to=date_to,
        orders=orders,
        limit=limit,
        offset=offset
    )
    resp_data = [RespAgrStat.from_orm(obj) for obj in objs]
    return paginate(resp_data)


@router.delete(
    "",
    tags=["stat"],
    summary="Clear all statistics",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def clear_stat(
    stat_storage: StatStoragePG = Depends(get_stat_storage_pg),
):
    await stat_storage.clear_all()
    return
