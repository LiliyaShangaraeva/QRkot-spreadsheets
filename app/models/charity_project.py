from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.constants import NAME_MAX_LENGTH
from app.core.db import CommonMixin
from app.models.base import BaseCharityModel


class CharityProject(CommonMixin, BaseCharityModel):
    """Модель Проект."""

    name: Mapped[str] = mapped_column(
        String(NAME_MAX_LENGTH),
        unique=True,
        nullable=False
    )
    description: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
