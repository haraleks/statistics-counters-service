from typing import List, Generic, TypeVar, Type

import sqlalchemy
from sqlalchemy import select
from sqlalchemy.orm import Session

from sc_service.db.postgre.pg import Base
from sc_service.exceptions.base import BadRequestException

ModelT = TypeVar("ModelT")


class DBPostgresStorage(Generic[ModelT]):
    model_cls: Type[Base] = Base

    def __init__(self, db: Session):
        self._db: Session = db

    async def insert_one(self, obj: ModelT, is_commit=True) -> ModelT:
        try:
            self._db.add(obj)
            await self._db.flush()
            await self._db.refresh(obj)
            self._db.expunge(obj)
            if is_commit:
                await self._db.commit()
        except sqlalchemy.exc.IntegrityError as e:
            raise BadRequestException(detail=str(e))
        return obj

    async def get_many(
        self,
        filters: dict = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[ModelT]:
        if limit > 100:
            limit = 100
        result = await self._db.execute(
            select(self.model_cls).filter_by(**filters).limit(limit).offset(offset)
        )

        return result.scalars().all()
