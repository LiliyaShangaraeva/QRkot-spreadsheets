from copy import deepcopy
from datetime import datetime

from aiogoogle import Aiogoogle
from app.core.config import settings
from app.core.constants import SPREADSHEET_BODY_TEMPLATE
from app.crud.charityproject import get_project_duration


FORMAT = "%Y/%m/%d %H:%M:%S"


async def create_spreadsheets(wrapper_services: Aiogoogle) -> dict[str, str]:
    """Создает документ с таблицами."""
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body: dict = deepcopy(
        SPREADSHEET_BODY_TEMPLATE
    )
    spreadsheet_body['properties']['title'] = (
        f'Отчёт от {now_date_time}'
    )
    response = dict(
        await wrapper_services.as_service_account(
            service.spreadsheets.create(json=spreadsheet_body)
        )
    )
    spreadsheet_url = (
        f"https://docs.google.com/spreadsheets/d/"
        f"{response['spreadsheetId']}"
    )

    return {
        'spreadsheetId': response['spreadsheetId'],
        'spreadsheetUrl': spreadsheet_url,
    }


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    """Предоставляет права доступа аккаунту к документу."""
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields="id"
        ))


async def update_spreadsheets_value(
        spreadsheet_id: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    """Записывает данные в Google таблицу."""
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    project_rows = [
        [
            project.name,
            str(get_project_duration(project)),
            project.description,
        ]
        for project in projects
    ]

    table_values = [
        ['Отчёт от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание'],
        *project_rows,
    ]

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range='A1:C30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
