from datetime import date

from sqlalchemy import text
from sqlalchemy.orm import Session

from sc_service.db.postgre.models import DBStat
from sc_service.db.postgre.pg_storage import DBPostgresStorage


class StatStoragePG(DBPostgresStorage[DBStat]):
    model_cls: DBStat = DBStat

    def __init__(self, db: Session):
        super().__init__(db)

    async def get_many(
            self,
            date_from: date = None,
            date_to: date = None,
            orders: str = None,
            limit: int = None,
            offset: int = None,

    ):
        q = ("SELECT date, "
             "sum(views) as views, "
             "sum(clicks) as clicks, "
             "sum(cost) as cost, "
             "sum(cost) / sum(clicks) as cpc, "
             "sum(cost) / sum(views) * 1000 as cpm "
             "FROM stat GROUP BY date")
        if limit is None:
            limit = 10
        if offset is None:
            offset = 0
        if orders is None:
            orders = "-date"
        args = {"limit": limit, "offset": offset}
        if date_from or date_to:
            q += " HAVING"
        if date_from:
            q += " date >= :date_from"
            args["date_from"] = date_from
        if date_from and date_to:
            q += " and"
        if date_to:
            q += " date <= :date_to"
            args["date_to"] = date_to
        if orders:
            order_postfix = "ASC"
            if orders[0] == "-":
                order_postfix = "DESC"
                orders = orders[1:]
            q += f" ORDER BY {orders} {order_postfix}"

        query = text(f"{q} LIMIT :limit OFFSET :offset;")
        results = await self._db.execute(query, args)
        return results.all()

    async def clear_all(self):
        query = text("DELETE FROM stat;")
        await self._db.execute(query)
        await self._db.commit()
