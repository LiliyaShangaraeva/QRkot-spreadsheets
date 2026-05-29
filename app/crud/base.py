from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class CRUDBase:
    """Класс с универсальными методами."""

    def __init__(self, model):
        """Инициализатор класса."""
        self.model = model

    async def get(
        self,
        obj_id: int,
        session: AsyncSession,
    ):
        """Метод для получения объекта по его id."""
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_multi(
        self,
        session: AsyncSession
    ):
        """Метод для получения всех объектов заданной модели."""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def get_open(
            self,
            session: AsyncSession,
    ):
        """Получает все незакрытые объекты."""
        result = await session.execute(
            select(self.model).where(
                self.model.fully_invested.is_(False)
            ).order_by(self.model.create_date)
        )
        return result.scalars().all()

    async def create(
        self,
        obj_in,
        session: AsyncSession,
        user: Optional[User] = None
    ):
        """Метод для добавления записи в базу."""
        obj_in_data = obj_in.model_dump()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.flush()
        return db_obj

    async def update(
        self,
        db_obj,
        obj_in,
        session: AsyncSession,
    ):
        """Метод для обновления записи по id."""
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.model_dump(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        db_obj,
        session: AsyncSession,
    ):
        """Метод для удаления объекта из базы."""
        await session.delete(db_obj)
        await session.commit()
        return db_obj
