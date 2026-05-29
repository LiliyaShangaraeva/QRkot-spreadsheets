from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import charity_project_crud


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
        project_id: int | None = None,
) -> None:
    """Проверяет, что нет проекта с таким названием."""
    existing_project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session)
    if (
        existing_project_id is not None and
        existing_project_id != project_id
    ):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )
