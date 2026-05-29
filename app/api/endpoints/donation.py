from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charityproject import charity_project_crud
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB, DonationResponse
from app.services.investment import investment

router = APIRouter()
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.post(
    '/',
    response_model=DonationResponse,
    response_model_exclude_none=True,
)
async def create_new_donation(
        donation: DonationCreate,
        session: SessionDep,
        user: Annotated[User, Depends(current_user)]
):
    """Создать пожертвование."""
    new_donation = await donation_crud.create(donation, session, user)
    projects = await charity_project_crud.get_open(session)

    updated_projects = investment(new_donation, projects)

    session.add_all(updated_projects)
    await session.commit()

    return new_donation


@router.get(
    '/',
    response_model=list[DonationDB],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(session: SessionDep):
    """Показать список всех пожертвований.

    Только для суперюзеров.
    """
    donations = await donation_crud.get_multi(session)
    return donations


@router.get(
    '/my',
    response_model=list[DonationResponse],
)
async def get_my_donations(
        session: SessionDep,
        user: Annotated[User, Depends(current_user)]
):
    """Показать список пожертвований пользователя, выполняющего запрос.

    Только для зарегистрированных пользователей.
    """
    donations = await donation_crud.get_by_user(
        session=session, user=user
    )
    return donations
