from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer

from app.core.consts import INVESTED_AMOUNT_DEFAULT_CONST
from app.core.db import Base


class Investment(Base):
    """Класс-родитель для CharityProject и Donation."""
    __abstract__ = True

    full_amount = Column(
        Integer,
        nullable=False,
    )
    invested_amount = Column(
        Integer,
        default=INVESTED_AMOUNT_DEFAULT_CONST,
    )
    fully_invested = Column(
        Boolean,
        default=False,
    )
    create_date = Column(
        DateTime,
        default=datetime.now,
    )
    close_date = Column(DateTime)
