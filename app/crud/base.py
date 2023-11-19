from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class CRUDBase:
    def __init__(self, model):
        self.model = model

    async def get_by_attribute(
        self,
        attribute_name: str,
        attribute_value: str,
        session: AsyncSession,
    ):
        attribute = getattr(self.model, attribute_name)
        db_object = await session.execute(
            select(self.model).where(attribute == attribute_value)
        )
        return db_object.scalars().first()

    async def get_multi(
        self,
        session: AsyncSession,
    ):
        db_objects = await session.execute(select(self.model))
        return db_objects.scalars().all()

    async def create(
        self,
        object_in,
        session: AsyncSession,
        user: Optional[User] = None
    ):
        object_in_data = object_in.dict()
        if user:
            object_in_data['user_id'] = user.id
        db_obj = self.model(**object_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
