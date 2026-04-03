# Local Development

## Prerequisites

- Docker and Docker Compose
- Node.js 20+ (for web linting/type checks)
- Git

## Quick Start

```bash
git clone <repo-url>
cd fastapi-nextjs-starter-kit

# Start all services
./dev/toolbox/run up

# Seed sample data
./dev/toolbox/run seed

# Verify everything works
./dev/toolbox/run health
```

Open http://localhost:3000 in your browser.

## Dev Toolbox

The project includes a CLI at `./dev/toolbox/run` for common tasks. Add a shell alias for convenience:

```bash
alias d='bash ./dev/toolbox/run'
```

### Available Commands

| Command | Description |
|---------|-------------|
| `up` | Start all services |
| `down` | Stop and remove all services |
| `restart` | Restart all services |
| `rebuild [service]` | Rebuild one or all containers |
| `logs [service]` | Tail logs |
| `ps` | Show running containers |
| `shell:api` | Bash into API container |
| `shell:worker` | Bash into worker container |
| `shell:web` | Shell into web container |
| `shell:db` | Open psql shell |
| `migrate` | Run database migrations |
| `migrate:status` | Show current migration |
| `health` | Check all services |
| `status` | Show URLs and ports |
| `test` | Run API tests |
| `lint` | Run all linters |
| `lint:api` | Lint API only |
| `lint:worker` | Lint worker only |
| `lint:web` | Lint web only |
| `format` | Auto-format Python code |
| `seed` | Create sample records |

## Service URLs

| Service | URL |
|---------|-----|
| Web | http://localhost:3000 |
| API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |
| PostgreSQL | localhost:5432 (user: `app`, pass: `app`, db: `app`) |
| Redis | localhost:6379 |

## Working on Individual Services

### API

```bash
# View logs
./dev/toolbox/run logs api

# Open shell
./dev/toolbox/run shell:api

# Run tests
./dev/toolbox/run test

# Create a new migration after model changes
./dev/toolbox/run shell:api
alembic revision --autogenerate -m "add new table"
exit
./dev/toolbox/run migrate
```

### Web

The web container runs a production build. For hot-reload development:

```bash
cd web
cp .env.example .env.local
npm install
npm run dev
```

This starts the Next.js dev server at http://localhost:3000 with hot reloading. Make sure the API is running via docker compose.

### Worker

```bash
# View worker logs (watch jobs being processed)
./dev/toolbox/run logs worker

# Open shell to inspect
./dev/toolbox/run shell:worker
```

## Running Tests

```bash
# Run all API tests
./dev/toolbox/run test

# Run specific test file
./dev/toolbox/run test -k test_records

# Run with verbose output
./dev/toolbox/run test -vv
```

Tests use SQLite in-memory, so they don't need Postgres.

## Linting

```bash
# Run all linters
./dev/toolbox/run lint

# Auto-format Python code
./dev/toolbox/run format
```

### What gets checked

| Service | Tool | What it checks |
|---------|------|---------------|
| API | ruff | Python linting + import sorting |
| API | ruff format | Code formatting |
| API | mypy | Type checking |
| Worker | ruff | Python linting + import sorting |
| Worker | ruff format | Code formatting |
| Worker | mypy | Type checking |
| Web | ESLint | TypeScript/React linting |
| Web | tsc | Type checking |

## Database

### Connecting directly

```bash
./dev/toolbox/run shell:db
# Now in psql:
\dt              -- list tables
SELECT * FROM records;
\q               -- quit
```

### Reset database

```bash
./dev/toolbox/run down
docker volume rm fastapi-nextjs-starter-kit_pgdata
./dev/toolbox/run up
```

## Troubleshooting

### Services won't start
```bash
./dev/toolbox/run down
./dev/toolbox/run rebuild
```

### API can't connect to database
Check that Postgres is healthy:
```bash
./dev/toolbox/run health
```

### Worker not processing jobs
Check Redis is running and worker logs:
```bash
./dev/toolbox/run health
./dev/toolbox/run logs worker
```
