from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class BaseCharityModel(Base):
    """Абстрактная модель, чтобы избежать дублирования."""

    __abstract__ = True

    __table_args__ = (
        CheckConstraint(
            'full_amount > 0',
            name='check_full_amount_positive'
        ),
        CheckConstraint(
            'invested_amount <= full_amount',
            name='check_invested_not_exceed_full'
        ),
    )

    full_amount: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    invested_amount: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )
    fully_invested: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    create_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    close_date: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    def __repr__(self):
        return (
            f'<{self.__class__.__name__}('
            f'id={self.id}, '
            f'full_amount={self.full_amount}, '
            f'invested_amount={self.invested_amount}, '
            f'fully_invested={self.fully_invested})>'
        )
