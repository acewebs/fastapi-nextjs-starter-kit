# Worker Service

Background job processor using ARQ (async Redis queue).

## What it does

- Consumes jobs enqueued by the API service via Redis
- Processes records asynchronously (simulates work, updates status)
- Connects directly to the database to update record state

## How it connects

- **Redis**: Receives jobs from the API service queue
- **Database**: Updates record status after processing

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | — | PostgreSQL connection string |
| `REDIS_URL` | — | Redis connection string |
| `APP_ENV` | `development` | Environment name |
| `LOG_LEVEL` | `info` | Log level |

## Local Development

```bash
cp .env.example .env
pip install -r requirements.txt
python -m app.worker
```

Or use docker-compose from the root directory.

## How to Extend

- Add new job functions in `app/jobs/`
- Register them in `WorkerSettings.functions` in `app/worker.py`
- Enqueue from the API using `await pool.enqueue_job("job_name", *args)`
