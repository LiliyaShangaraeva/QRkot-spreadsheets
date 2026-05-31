NAME_MAX_LENGTH = 100
JWT_LIFETIME_SECONDS = 3600
MIN_PASSWORD_LENGTH = 3
GOOGLE_API_PREFIX = 'https://www.googleapis.com/auth/'
SPREADSHEETS_SCOPE = f'{GOOGLE_API_PREFIX}spreadsheets'
DRIVE_SCOPE = f'{GOOGLE_API_PREFIX}drive'
SPREADSHEET_BODY_TEMPLATE = {
    'properties': {'title': '',
                   'locale': 'ru_RU'},
    'sheets': [{'properties': {'sheetType': 'GRID',
                               'sheetId': 0,
                               'title': 'Лист1',
                               'gridProperties': {'rowCount': 100,
                                                  'columnCount': 11}}}]
}
