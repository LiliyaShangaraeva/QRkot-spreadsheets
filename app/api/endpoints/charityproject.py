from datetime import datetime
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_name_duplicate
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charityproject import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charityproject import (CharityProjectCreate, CharityProjectDB,
                                        CharityProjectUpdate)
from app.services.investment import investment
from app.services.project import (check_charity_project_exists,
                                  check_charity_project_before_delete)

router = APIRouter()
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: SessionDep,
):
    """Создать целевой проект.

    Только для суперюзеров.
    """
    await check_name_duplicate(charity_project.name, session)
    new_project = await charity_project_crud.create(charity_project, session)
    donations = await donation_crud.get_open(session)

    updated_objects = investment(new_project, donations)

    session.add_all(updated_objects)
    await session.commit()

    return new_project


@router.get(
    '/',
    response_model=list[CharityProjectDB]
)
async def get_all_charity_projects(session: SessionDep):
    """Показать список всех целевых проектов."""
    return await charity_project_crud.get_multi(session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: SessionDep,
):
    """
    Редактировать целевой проект.

    Только для суперюзеров.
    Закрытый проект нельзя редактировать;
    нельзя установить требуемую сумму меньше уже вложенной.
    """
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session, project_id=project_id)

    if (
        obj_in.full_amount is not None and
        obj_in.full_amount < charity_project.invested_amount
    ):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                "Нельзя установить значение full_amount "
                "меньше уже вложенной суммы."
            )
        )

    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )
    if charity_project.full_amount == charity_project.invested_amount:
        charity_project.fully_invested = True
        charity_project.close_date = datetime.utcnow()
        await session.commit()

    return charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
        project_id: int,
        session: SessionDep,
):
    """
    Удалить целевой проект.

    Только для суперюзеров.
    Нельзя удалить проект, в который уже были инвестированы средства.
    """
    charity_project = await check_charity_project_before_delete(
        project_id,
        session
    )

    charity_project = await charity_project_crud.remove(
        charity_project, session
    )
    return charity_project
