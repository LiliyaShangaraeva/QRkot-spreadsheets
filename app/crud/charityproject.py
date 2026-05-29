from datetime import timedelta
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


def get_project_duration(project: CharityProject):
    if project.close_date is None:
        return timedelta.max
    return project.close_date - project.create_date


class CRUDCharityProject(CRUDBase):
    """CRUD-операции для модели CharityProject."""

    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        """Получает id по имени."""
        result = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        db_project_id = result.scalars().first()
        return db_project_id

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession
    ) -> list[CharityProject]:
        result = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested
            )
        )

        projects = result.scalars().all()

        projects = sorted(
            projects,
            key=get_project_duration
        )

        return projects


charity_project_crud = CRUDCharityProject(CharityProject)
