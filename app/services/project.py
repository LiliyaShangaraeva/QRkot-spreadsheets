from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import charity_project_crud
from app.models.charity_project import CharityProject


async def get_project_or_404(project_id, session):
    """Проверяет, что проект существует."""
    project = await charity_project_crud.get(project_id, session)

    if project is None:
        raise HTTPException(404, "Проект не найден.")

    return project


async def check_charity_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    """Проверяет, что проект не закрыт."""
    project = await get_project_or_404(project_id, session)

    if project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail="Закрытый проект нельзя редактировать!"
        )

    return project


async def check_charity_project_before_delete(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    """Проверяет, что в проект не инвестировали."""
    project = await get_project_or_404(project_id, session)

    if project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail="В проект были внесены средства, не подлежит удалению!"
        )

    return project
