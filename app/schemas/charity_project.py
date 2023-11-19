from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator

from app.core.consts import (
    FIELD_MAX_LENGHT,
    FIELD_MIN_LENGHT,
)


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=FIELD_MIN_LENGHT,
        max_length=FIELD_MAX_LENGHT,
    )
    description: Optional[str] = Field(
        None,
        min_length=FIELD_MIN_LENGHT,
    )
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(
        ...,
        min_length=FIELD_MIN_LENGHT,
        max_length=FIELD_MAX_LENGHT,
    )
    description: str = Field(
        ...,
        min_length=FIELD_MIN_LENGHT,
    )
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):
    @validator('name')
    def name_cannot_be_null(cls, value):
        if not value:
            raise ValueError('Добавьте имя проекта, оно не может быть пустым')
        return value


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
