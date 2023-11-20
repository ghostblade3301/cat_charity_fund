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
    return open_objects.scalars().all()


async def to_invest_free_donates(
    object: Union[CharityProject, Donation],
    session: AsyncSession,
) -> None:
    """Распределения свободных пожертвований среди открытых проектов."""
    MODELS = (CharityProject, Donation)
    model = MODELS[isinstance(object, CharityProject)]
    open_objects = await get_all_open_projects(model, session)
    if not open_objects:
        return
    invest_amount = object.full_amount
    for open_object in open_objects:
        result = open_object.full_amount - open_object.invested_amount
        invested_amount = min(result, invest_amount)
        open_object.invested_amount += invested_amount
        object.invested_amount += invested_amount
        invest_amount -= invested_amount
        if open_object.full_amount == open_object.invested_amount:
            await to_close(open_object)
        if not invest_amount:
            await to_close(object)
            break
    await session.commit()
