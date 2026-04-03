# Architecture

## Overview

This starter kit follows a **service-oriented architecture** with five components:

```
[ Browser ]
     |
   web (Next.js :3000)
     |
   api (FastAPI :8000)
     |
   db (Postgres :5432)

worker (Python/ARQ)
     |
   redis (:6379)
```

## Services

### Web (Next.js)

The public-facing frontend. Renders pages server-side using React Server Components and handles client-side interactivity for forms and data tables.

- **Framework**: Next.js 16 with App Router
- **Styling**: Tailwind CSS v4 + shadcn/ui
- **Output**: Standalone build for Docker deployment
- **Communication**: Calls API via REST (server-side uses internal URL, client-side uses public URL)

### API (FastAPI)

The backend service handling business logic, database access, and job enqueueing.

- **Framework**: FastAPI with async endpoints
- **ORM**: SQLAlchemy 2.0 (async) with asyncpg driver
- **Migrations**: Alembic
- **Queue**: Enqueues jobs to Redis via ARQ
- **Docs**: Auto-generated OpenAPI at `/docs`

### Worker (ARQ)

Background job processor that consumes tasks from Redis.

- **Queue**: ARQ (async Redis queue)
- **Database**: Direct async connection to Postgres
- **Jobs**: Processes records asynchronously (updates status from pending → processing → completed)

### Database (PostgreSQL 16)

Primary data store. Managed by Railway in production, runs as a Docker container locally.

### Redis 7

Queue backend for ARQ. Used for job dispatch between API and Worker. Can also be used for caching.

## Data Flow

### Record Creation

```
1. User fills form in browser
2. Web sends POST /api/v1/records to API
3. API validates input, creates record in Postgres (status: pending)
4. API enqueues "process_record" job to Redis via ARQ
5. API returns created record to Web
6. Worker picks up job from Redis
7. Worker processes record (simulated work)
8. Worker updates record status in Postgres (pending → processing → completed)
```

### Networking

| Route | Protocol | URL Pattern |
|-------|----------|-------------|
| Browser → Web | HTTPS (public) | `https://your-app.railway.app` |
| Web → API (proxy) | HTTP (internal) | `http://api.railway.internal:8000` |
| API → Postgres | TCP | `DATABASE_URL` |
| API → Redis | TCP | `REDIS_URL` |
| Worker → Redis | TCP | `REDIS_URL` |
| Worker → Postgres | TCP | `DATABASE_URL` |

### Public vs Private Services

In Railway:
- **Web** is the only public service (has a domain) — it proxies `/api/*` requests to the API
- **API**, **Worker**, **Postgres**, and **Redis** are all private

## Directory Structure

```
.
├── api/                    # FastAPI backend
│   ├── app/
│   │   ├── api/routes/     # HTTP endpoint handlers
│   │   ├── core/           # Config, Redis connection
│   │   ├── db/             # SQLAlchemy engine + session
│   │   ├── models/         # ORM models
│   │   ├── schemas/        # Pydantic request/response models
│   │   ├── services/       # Business logic
│   │   └── main.py         # FastAPI app entrypoint
│   ├── alembic/            # Database migrations
│   └── tests/              # API tests (pytest)
├── web/                    # Next.js frontend
│   └── src/
│       ├── app/            # Pages (App Router)
│       ├── components/     # React components
│       └── lib/            # API client, utilities
├── worker/                 # Background job processor
│   └── app/
│       ├── jobs/           # Job functions
│       ├── worker.py       # ARQ worker entrypoint
│       └── config.py       # Settings
├── dev/toolbox/            # Development CLI
├── docs/                   # Documentation
├── .github/workflows/      # CI pipeline
└── docker-compose.yml      # Local development orchestration
```
