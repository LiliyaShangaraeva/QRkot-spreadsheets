# QRKot - Благотворительный фонд поддержки котиков.

## Описание проекта

QRKot — это API-сервис для сбора пожертвований на благотворительные проекты.
Пользователи могут создавать проекты и вносить пожертвования, которые автоматически распределяются между открытыми проектами.

Проект реализован на базе FastAPI и соответствует спецификации OpenAPI (Swagger).
Реализована система управления пользователями.
Анонимный пользователь
- может просматривать список проектов;
- может зарегистрироваться.

Зарегистрированный пользователь
- может создавать пожертвования;
- может просматривать только свои пожертвования.

Суперпользователь
- может создавать, редактировать и удалять проекты;
- может просматривать все пожертвования.

При запуске приложения автоматически создаётся суперпользователь из переменных окружения.
---

## Google Sheets отчёты

Реализована интеграция с Google API.

Суперпользователь может создать Google-таблицу с отчётом по закрытым проектам.
Проекты сортируются по скорости сбора средств — от самых быстро закрытых к самым долгим.

Для работы используется сервисный аккаунт Google Cloud.
---

## Технологический стек

- Python 3.12+
- FastAPI
- FastAPI Users
- SQLAlchemy (async)
- Pydantic
- Alembic
- SQLite
- JWT Authentication
- Google Sheets API
- Google Drive API
- Aiogoogle

---

## Как развернуть проект

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/LiliyaShangaraeva/cat-charity-2.git
cd cat-charity-2
```

### 3. Создайте и активируйте виртуальное окружение

```bash
python -m venv venv
source venv/bin/activate # Linux / Mac 
source venv\Scripts\activate # Windows
```

### 4. Установите зависимости

```bash
pip install -r requirements.txt
```

### 5. Создайте файл .env

```bash
DATABASE_URL=sqlite+aiosqlite:///./qrkot.db
SECRET=your_secret_key
FIRST_SUPERUSER_EMAIL=your_first_superuser_email
FIRST_SUPERUSER_PASSWORD=your_first_superuser_password
TYPE=service_account
PROJECT_ID=your_project_id 
PRIVATE_KEY_ID=your_private_key_id 
PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n" 
CLIENT_EMAIL=your_client_email 
CLIENT_ID=your_client_id 
AUTH_URI=https://accounts.google.com/o/oauth2/auth 
TOKEN_URI=https://oauth2.googleapis.com/token 
AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs 
CLIENT_X509_CERT_URL=your_cert_url 
EMAIL=your_google_email
```

### 6. Примените миграции

```bash
alembic upgrade head
```

### 7. Запустите проект

```bash
uvicorn app.main:app --reload
```

### Документация API

После запуска доступна:

Swagger UI:
http://127.0.0.1:8000/docs
ReDoc:
http://127.0.0.1:8000/redoc

### Примеры запросов

### Создание проекта

POST /charity_project/

```bash
{
    "name": "Помощь котикам",
    "description": "Сбор средств на корм",
    "full_amount": 10000
}
```

### Создание пожертвования

POST /donation/

```bash
{
    "full_amount": 500,
    "comment": "Для котиков"
}
```

### Автор:
[Лилия Шангараева](https://github.com/LiliyaShangaraeva)
