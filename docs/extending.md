# Extending the Starter Kit

This guide covers common customization patterns.

## Replace the Record Model

The template uses a generic `Record` model. To replace it with your own domain model:

### 1. Update the SQLAlchemy model

Edit `api/app/models/record.py` or create a new file:

```python
# api/app/models/product.py
from sqlalchemy import String, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from uuid_utils import uuid7
from app.db.base import Base

class Product(Base):
    __tablename__ = "products"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid7)
    title: Mapped[str] = mapped_column(String(255))
    price: Mapped[int] = mapped_column(Integer)
    # ... your fields
```

### 2. Update schemas

Edit `api/app/schemas/record.py` with matching Pydantic models.

### 3. Update service layer

Edit `api/app/services/record.py` with your business logic.

### 4. Update routes

Edit `api/app/api/routes/records.py` with new endpoints.

### 5. Create migration

```bash
./dev/toolbox/run shell:api
alembic revision --autogenerate -m "replace records with products"
exit
./dev/toolbox/run migrate
```

### 6. Update frontend

Update `web/src/lib/api.ts` types and components in `web/src/components/records/`.

## Add a New Model

### 1. Create model, schema, service, and route files

```
api/app/models/comment.py
api/app/schemas/comment.py
api/app/services/comment.py
api/app/api/routes/comments.py
```

### 2. Register the model

```python
# api/app/models/__init__.py
from app.models.record import Record
from app.models.comment import Comment
```

### 3. Register the route

```python
# api/app/main.py
from app.api.routes import health, records, app_info, comments

app.include_router(comments.router)
```

### 4. Create and run migration

```bash
./dev/toolbox/run shell:api
alembic revision --autogenerate -m "add comments table"
exit
./dev/toolbox/run migrate
```

## Add a New Page

Create a new directory in `web/src/app/`:

```
web/src/app/dashboard/page.tsx
```

Add it to the sidebar in `web/src/components/layout/sidebar.tsx`:

```typescript
const navItems = [
  // ... existing items
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
];
```

## Add a New Background Job

### 1. Create the job function

```python
# worker/app/jobs/send_notification.py
async def send_notification(ctx: dict, user_id: str, message: str) -> str:
    # Your async work here
    return f"Notified {user_id}"
```

### 2. Register it in the worker

```python
# worker/app/worker.py
from app.jobs.send_notification import send_notification

class WorkerSettings:
    functions = [process_record, send_notification]
```

### 3. Enqueue from the API

```python
pool = get_arq_pool()
await pool.enqueue_job("send_notification", user_id, "Hello!")
```

## Add Authentication

A common pattern for adding auth:

### 1. Add dependencies

```
# api/requirements.txt
python-jose[cryptography]
passlib[bcrypt]
```

### 2. Create auth module

```
api/app/core/auth.py     # JWT creation/validation
api/app/core/security.py  # Password hashing
api/app/models/user.py    # User model
api/app/schemas/user.py   # User schemas
api/app/api/routes/auth.py # Login/register endpoints
```

### 3. Create a dependency

```python
# api/app/core/auth.py
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

async def get_current_user(token = Depends(HTTPBearer())):
    # Validate JWT, return user
    ...
```

### 4. Protect routes

```python
@router.get("/protected")
async def protected_route(user = Depends(get_current_user)):
    return {"user": user.email}
```

## Add Environment Variables

### API or Worker

1. Add to `api/app/core/config.py` (or `worker/app/config.py`):
   ```python
   MY_NEW_VAR: str = "default"
   ```
2. Add to `.env.example`
3. Add to `docker-compose.yml` under the service's `environment` section
4. Document in the service's `README.md`

### Web

1. Add to `web/.env.example`
2. Prefix with `NEXT_PUBLIC_` if needed client-side
3. Access via `process.env.NEXT_PUBLIC_MY_VAR`

## Environment Variables Reference

### API

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `PORT` | no | `8000` | Server port |
| `HOST` | no | `0.0.0.0` | Server host |
| `DATABASE_URL` | yes | — | PostgreSQL connection string |
| `REDIS_URL` | yes | — | Redis connection string |
| `SECRET_KEY` | yes | — | Application secret key |
| `CORS_ORIGINS` | no | `http://localhost:3000` | Comma-separated allowed origins |
| `APP_ENV` | no | `development` | Environment name |
| `APP_NAME` | no | `starter-api` | Application name |
| `LOG_LEVEL` | no | `info` | Log level |

### Worker

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | yes | — | PostgreSQL connection string |
| `REDIS_URL` | yes | — | Redis connection string |
| `APP_ENV` | no | `development` | Environment name |
| `LOG_LEVEL` | no | `info` | Log level |

### Web

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `BACKEND_URL` | no | `http://localhost:8000` | API URL (used by proxy and server-side requests) |
