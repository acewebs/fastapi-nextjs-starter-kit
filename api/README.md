# API Service (FastAPI)

REST API backend for the starter template.

## What it does

- Exposes CRUD endpoints for the `Record` model
- Manages database interactions via async SQLAlchemy
- Enqueues background jobs to Redis (via ARQ)
- Runs database migrations with Alembic

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/api/v1/records` | List records |
| POST | `/api/v1/records` | Create record |
| GET | `/api/v1/records/{id}` | Get record |
| PATCH | `/api/v1/records/{id}` | Update record |
| DELETE | `/api/v1/records/{id}` | Delete record |
| GET | `/api/v1/app` | App info |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `8000` | Server port |
| `HOST` | `0.0.0.0` | Server host |
| `DATABASE_URL` | — | PostgreSQL connection string |
| `REDIS_URL` | — | Redis connection string |
| `SECRET_KEY` | — | Application secret |
| `CORS_ORIGINS` | `http://localhost:3000` | Comma-separated allowed origins |
| `APP_ENV` | `development` | Environment name |
| `APP_NAME` | `starter-api` | Application name |
| `LOG_LEVEL` | `info` | Log level |

## Local Development

```bash
cp .env.example .env
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

Or use docker-compose from the root directory.

## How to Extend

- Add new models in `app/models/`
- Add new schemas in `app/schemas/`
- Add new routes in `app/api/routes/`
- Add new service logic in `app/services/`
- Create migrations: `alembic revision --autogenerate -m "description"`
