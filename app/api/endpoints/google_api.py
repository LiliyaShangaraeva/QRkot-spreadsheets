from http import HTTPStatus

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charityproject import charity_project_crud
from app.services.google_api import (
    create_spreadsheets,
    set_user_permissions,
    update_spreadsheets_value,
)

router = APIRouter()


@router.post(
    '/',
    dependencies=[Depends(current_superuser)],
)
async def get_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service),
):
    projects = await charity_project_crud.get_projects_by_completion_rate(
        session
    )

    result = await create_spreadsheets(wrapper_services)

    spreadsheet_id = result['spreadsheetId']
    spreadsheet_url = result['spreadsheetUrl']

    await set_user_permissions(
        spreadsheet_id,
        wrapper_services
    )
    try:
        await update_spreadsheets_value(
            spreadsheet_id,
            projects,
            wrapper_services
        )
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail='Не удалось сформировать отчёт.',
        )

    return {
        'spreadsheetId': spreadsheet_id,
        'spreadsheetUrl': spreadsheet_url,
        'url': spreadsheet_url,
    }
