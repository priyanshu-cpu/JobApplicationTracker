# Job Application Tracker API

A REST API for tracking job applications, built with FastAPI, PostgreSQL and SQLAlchemy. Each user registers, logs in with a JWT, and manages their own private list of applications.

## Features

- User registration and login with JWT bearer tokens
- Passwords hashed with Argon2
- Create, list, view, update and delete job applications
- Partial updates with PATCH
- Each user can only access their own applications
- Database migrations with Alembic
- Interactive API docs (Swagger UI) at `/docs`

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy 2.0 |
| Migrations | Alembic |
| Auth | python-jose (JWT), pwdlib (Argon2) |
| Config | pydantic-settings |
| Package manager | uv |
| Python | 3.13+ |

## Project Structure

```
JobApplicationTracker/
├── alembic/                # Migration environment and versions
├── app/
│   ├── main.py             # FastAPI app and router registration
│   ├── database.py         # Engine, session and Base
│   ├── settings.py         # Environment-based settings
│   ├── dependencies/
│   │   └── auth.py         # get_current_user dependency
│   ├── models/             # SQLAlchemy models (User, Application)
│   ├── routers/            # Route handlers (auth, application)
│   ├── schemas/            # Pydantic schemas and enums
│   └── utils/
│       └── security.py     # Password hashing and JWT helpers
├── pyproject.toml
└── uv.lock
```

## Getting Started

### Prerequisites

- Python 3.13 or newer
- PostgreSQL
- [uv](https://docs.astral.sh/uv/)

### 1. Clone and install

```bash
git clone <your-repo-url>
cd JobApplicationTracker
uv sync
```

### 2. Create the database

```sql
CREATE DATABASE "JobApplicationTracker";
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
DB_CONNECTION=postgresql://<user>:<password>@localhost:5432/JobApplicationTracker
SECRET_KEY=<a-long-random-string>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Generate a secret key with:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 4. Configure Alembic

`alembic.ini` is not committed because it contains the database URL. Create it in the project root with at least:

```ini
[alembic]
script_location = alembic
sqlalchemy.url = postgresql://<user>:<password>@localhost:5432/JobApplicationTracker
```

### 5. Run migrations

```bash
uv run alembic upgrade head
```

### 6. Start the server

```bash
uv run fastapi dev app/main.py
```

The API runs at `http://127.0.0.1:8000` and the interactive docs at `http://127.0.0.1:8000/docs`.

## API Reference

### Auth

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/auth/register` | Create a new user | No |
| POST | `/auth/login` | Get an access token | No |
| GET | `/auth/me` | Get the current user | Yes |

### Applications

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/application/create` | Create an application | Yes |
| GET | `/application/get` | List your applications | Yes |
| GET | `/application/get/{id}` | Get one application | Yes |
| PUT | `/application/update/{id}` | Update the status | Yes |
| PATCH | `/application/update/{id}` | Update any subset of fields | Yes |
| DELETE | `/application/delete/{id}` | Delete an application | Yes |

Protected endpoints require the header:

```
Authorization: Bearer <access_token>
```

### Application status values

`applied`, `interview`, `offer`, `rejected`, `withdrawn`

## Usage Examples

### Register

```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "email": "john@example.com", "password": "secret123"}'
```

### Login

Login takes form data, not JSON:

```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -d "username=john&password=secret123"
```

```json
{
  "access_token": "<token>",
  "token_type": "bearer"
}
```

### Create an application

```bash
curl -X POST http://127.0.0.1:8000/application/create \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "company": "Acme Corp",
    "job_title": "Backend Developer",
    "location": "Remote",
    "salary": 1200000,
    "status": "applied",
    "notes": "Referred by a friend"
  }'
```

```json
{
  "message": "application created",
  "data": {
    "id": 1,
    "user_id": 1,
    "company": "Acme Corp",
    "status": "applied",
    "job_title": "Backend Developer",
    "location": "Remote",
    "salary": 1200000,
    "created_at": "2026-10-04 11:40:07",
    "applied_at": "2026-10-04 11:40:07",
    "notes": "Referred by a friend"
  }
}
```

`applied_at` is optional and defaults to the current time.

### Partially update an application

```bash
curl -X PATCH http://127.0.0.1:8000/application/update/1 \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"status": "interview", "notes": "Call scheduled for Monday"}'
```

## Database Migrations

After changing a model:

```bash
uv run alembic revision --autogenerate -m "describe the change"
uv run alembic upgrade head
```

To roll back one migration:

```bash
uv run alembic downgrade -1
```

