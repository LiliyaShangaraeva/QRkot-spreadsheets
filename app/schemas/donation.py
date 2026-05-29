from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class DonationBase(BaseModel):
    """Базовая схема, чтобы избежать дублирования."""

    full_amount: Optional[int] = Field(None, gt=0)
    comment: Optional[str] = None


class DonationCreate(DonationBase):
    """Схема для создания пожертвования."""

    full_amount: int = Field(..., gt=0)


class DonationDB(DonationBase):
    """Схема для описания объекта, полученного из БД."""

    full_amount: int
    id: int
    create_date: datetime
    user_id: Optional[int] = None
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class DonationResponse(DonationBase):
    """Схема отображения пожертвования для пользователя."""

    full_amount: int
    id: int
    create_date: datetime
