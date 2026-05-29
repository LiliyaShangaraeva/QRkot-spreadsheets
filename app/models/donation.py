from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import CommonMixin
from app.models.base import BaseCharityModel


class Donation(CommonMixin, BaseCharityModel):
    """Модель Пожертвование."""

    comment: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('user.id', name='fk_donation_user_id_user'),
        nullable=True
    )
