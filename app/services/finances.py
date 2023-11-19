from datetime import datetime
from typing import List, Type, TypeVar, Union

from sqlalchemy import false, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


ModelType = TypeVar('ModelType', CharityProject, Donation)


async def to_close(
    object: Union[CharityProject, Donation],
) -> None:
    object.fully_invested = True
    object.close_date = datetime.now()


async def get_all_open_projects(
    model: Type[ModelType],
    session: AsyncSession,
) -> List[Union[CharityProject, Donation]]:
    open_objects = await session.execute(
        select(model).where(
            model.fully_invested == false()
        ).order_by(model.create_date)
    )
    open_objects = open_objects.scalars().all()
    return open_objects


async def to_invest_free_donates(
    object: Union[CharityProject, Donation],
    session: AsyncSession,
) -> None:
    '''Распределения свободных пожертвований среди открытых проектов'''
    MODELS = (CharityProject, Donation)
    model = MODELS[isinstance(object, CharityProject)]
    open_objects = await get_all_open_projects(model, session)
    if open_objects:
        amount_to_invest = object.full_amount
        for open_object in open_objects:
            amount = open_object.full_amount - open_object.invested_amount
            invested_amount = min(amount, amount_to_invest)
            open_object.invested_amount += invested_amount
            object.invested_amount += invested_amount
            amount_to_invest -= invested_amount
            if open_object.full_amount == open_object.invested_amount:
                await to_close(open_object)
            if not amount_to_invest:
                await to_close(object)
                break
        await session.commit()
