# Deployment (Railway)

## Overview

This template deploys as **5 services** on Railway:

- 3 application services (API, Web, Worker) from this repo
- 2 managed services (Postgres, Redis) provisioned by Railway

The Web service proxies all `/api/*` requests to the API over Railway's private network, so the API does not need a public domain.

## One-Click Deploy

Click the **Deploy on Railway** button in the README. Railway will:

1. Fork this repo to your GitHub account
2. Create a project with all services configured
3. Deploy everything automatically

After deployment, clone your fork and start building on top of it.

## Manual Setup

If you prefer to set things up manually:

### 1. Push to GitHub

Push this repository to a public GitHub repo.

### 2. Create Railway Project

1. Go to [Railway](https://railway.app) and create a new project
2. Add a **PostgreSQL** database (click "New" → "Database" → "PostgreSQL")
3. Add a **Redis** database (click "New" → "Database" → "Redis")

### 3. Deploy the API Service

1. Click "New" → "GitHub Repo" → select your repo
2. In service settings:
   - **Root Directory**: `api`
3. Add environment variables:

| Variable | Value |
|----------|-------|
| `DATABASE_URL` | `postgresql+asyncpg://${{postgres.PGUSER}}:${{postgres.PGPASSWORD}}@${{postgres.PGHOST}}:${{postgres.PGPORT}}/${{postgres.PGDATABASE}}` |
| `REDIS_URL` | `redis://${{redis.REDISUSER}}:${{redis.REDISPASSWORD}}@${{redis.REDISHOST}}:${{redis.REDISPORT}}` |
| `SECRET_KEY` | `${{ secret(64, "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") }}` |
| `CORS_ORIGINS` | `https://${{web.RAILWAY_PUBLIC_DOMAIN}}` |
| `APP_ENV` | `production` |
| `APP_NAME` | `starter-api` |
| `LOG_LEVEL` | `info` |
| `PORT` | `8000` |
| `HOST` | `0.0.0.0` |

4. **No public domain needed** — the Web service proxies API requests over the private network.

### 4. Deploy the Worker Service

1. Click "New" → "GitHub Repo" → select the same repo
2. In service settings:
   - **Root Directory**: `worker`
3. Add environment variables:

| Variable | Value |
|----------|-------|
| `DATABASE_URL` | `postgresql+asyncpg://${{postgres.PGUSER}}:${{postgres.PGPASSWORD}}@${{postgres.PGHOST}}:${{postgres.PGPORT}}/${{postgres.PGDATABASE}}` |
| `REDIS_URL` | `redis://${{redis.REDISUSER}}:${{redis.REDISPASSWORD}}@${{redis.REDISHOST}}:${{redis.REDISPORT}}` |
| `APP_ENV` | `production` |
| `LOG_LEVEL` | `info` |

4. **No public domain needed** — the worker has no HTTP endpoints.

### 5. Deploy the Web Service

1. Click "New" → "GitHub Repo" → select the same repo
2. In service settings:
   - **Root Directory**: `web`
3. Add environment variables:

| Variable | Value |
|----------|-------|
| `BACKEND_URL` | `http://${{api.RAILWAY_PRIVATE_DOMAIN}}:8000` |

4. Generate a **public domain** for this service (Settings → Networking → Generate Domain).

### 6. Verify

1. Open the Web service's public URL
2. Navigate to `/status` — should show API as healthy
3. Navigate to `/records` — create a record, verify it appears
4. Check worker logs — should show job processing

## Railway Reference Variables

Railway lets you reference variables from other services using `${{ServiceName.VARIABLE}}` syntax. This keeps credentials in sync automatically.

## Internal Networking

Railway services can communicate internally using:
```
http://<service-name>.railway.internal:<port>
```

The Web service uses this to proxy API requests to the backend:
```
BACKEND_URL=http://api.railway.internal:8000
```

Browser requests to `/api/*` are forwarded by Next.js to the API over the private network. This means the API never needs a public domain.

## Custom Domain

1. Go to your Web service → Settings → Networking
2. Add a custom domain
3. Update DNS records as instructed by Railway

## Production Considerations

- Set `APP_ENV=production` on API and Worker
- Use a strong random `SECRET_KEY`
- Set `LOG_LEVEL=warn` to reduce noise
- Monitor worker logs for failed jobs
- Railway auto-scales horizontally — add replicas in service settings if needed
