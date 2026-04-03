# Full-Stack Starter Kit — FastAPI + Next.js + Worker

A production-ready starter template designed for [Railway](https://railway.app) deployment.

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/deploy/nextjs-fastapi-full-stack-starter)

## What You Get

- **Working full-stack app** — frontend, API, background worker, database, and cache
- **End-to-end async flow** — create a record in the UI, API writes to Postgres and enqueues a job, worker processes it, UI auto-updates
- **Production structure** — not a toy demo, but a real architecture you can build on
- **One command to run** — `./dev/toolbox/run up` starts everything locally

## Architecture

```
[ Browser ]
     |
   web (Next.js)          :3000  ← proxy /api/* to backend
     |
   api (FastAPI)           :8000  ← private, no public domain needed
     |
   db (Postgres)           :5432

worker (Python/ARQ)
     |
   redis                   :6379
```

## Services

| Service | Tech | Description |
|---------|------|-------------|
| **web** | Next.js 16, TypeScript, Tailwind, shadcn/ui | Frontend with CRUD UI |
| **api** | FastAPI, SQLAlchemy, Alembic | REST API with DB + Redis |
| **worker** | Python, ARQ | Background job processor |
| **db** | PostgreSQL 16 | Primary data store |
| **redis** | Redis 7 | Queue backend + cache |

## Deploy on Railway

1. Click the **Deploy on Railway** button above
2. Railway forks this repo to your GitHub account and deploys all services
3. Once deployed, you have a working app at your Railway URL

### After Deploying — Make It Yours

1. Clone your forked repo locally
2. Replace the `Record` model with your own domain model ([guide](docs/extending.md))
3. Push changes — Railway auto-deploys from your fork

See [docs/deployment.md](docs/deployment.md) for detailed configuration.

## Quick Start (Local)

```bash
git clone <your-fork-url>
cd fastapi-nextjs-starter-kit

# Start everything
./dev/toolbox/run up

# Seed sample data
./dev/toolbox/run seed

# Check all services are healthy
./dev/toolbox/run health

# See all available commands
./dev/toolbox/run help
```

- **Web**: http://localhost:3000
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

**Tip**: Add a shell alias for convenience:
```bash
alias d='bash ./dev/toolbox/run'
# Then use: d up, d logs api, d health, d seed, etc.
```

## Project Structure

```
.
├── api/              # FastAPI backend
├── web/              # Next.js frontend
├── worker/           # ARQ background worker
├── dev/toolbox/      # Dev CLI commands
├── docs/             # Documentation
└── docker-compose.yml
```

## Documentation

| Guide | Description |
|-------|-------------|
| [Architecture](docs/architecture.md) | Service diagram, data flow, directory structure |
| [Local Development](docs/development.md) | Setup, toolbox commands, testing, linting |
| [Deployment](docs/deployment.md) | Step-by-step Railway deployment guide |
| [API Reference](docs/api-reference.md) | Endpoints, request/response formats, data model |
| [Extending](docs/extending.md) | Add models, pages, jobs, auth, env vars |

## Data Model

The template includes a single `Record` model to demonstrate the full stack:

| Field | Type |
|-------|------|
| id | UUID (v7) |
| name | string (1-255) |
| description | text (optional) |
| status | string (pending → processing → completed) |
| created_at | timestamp |
| updated_at | timestamp |

When you create a record, the API saves it and enqueues a background job. The worker picks it up, processes it, and updates the status. The UI polls and reflects the change automatically.

## CI

GitHub Actions runs on every PR:
- **API**: ruff lint + format check + mypy + pytest (12 tests)
- **Worker**: ruff lint + format check + mypy
- **Web**: ESLint + TypeScript check + production build

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Whether it's a bug fix, new feature, documentation improvement, or just a question — feel free to open an issue or PR.

## License

[MIT](LICENSE)
