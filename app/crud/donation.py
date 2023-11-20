from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):
    async def get_by_user(
        self,
        session: AsyncSession,
        user: User,
    ) -> List[Donation]:
        """Получаем список пожертвований пользователя."""
        my_donations = await session.execute(
            select(Donation).filter(
                Donation.user_id == user.id
            )
        )
        return my_donations.scalars().all()


donation_crud = CRUDDonation(Donation)
