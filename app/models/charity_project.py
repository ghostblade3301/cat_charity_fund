from sqlalchemy import Column, String, Text

from .abstract import Investment
from app.core.consts import CHARITY_PROJECT_NAME_LENGHT


class CharityProject(Investment):
    name = Column(
        String(CHARITY_PROJECT_NAME_LENGHT),
        unique=True,
        nullable=False,
    )
    description = Column(
        Text,
        nullable=False,
    )

    def __repr__(self):
        return self.name
