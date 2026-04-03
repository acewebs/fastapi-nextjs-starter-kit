# API Reference

Base URL: `http://localhost:8000` (local) or your Railway API domain.

Interactive docs available at `/docs` (Swagger UI).

## Health

### `GET /health`

Returns API health status.

**Response** `200`
```json
{
  "status": "ok"
}
```

## App Info

### `GET /api/v1/app`

Returns application metadata.

**Response** `200`
```json
{
  "name": "starter-api",
  "env": "development",
  "version": "1.0.0"
}
```

## Records

### `GET /api/v1/records`

List all records with pagination.

**Query Parameters**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `skip` | int | 0 | Records to skip |
| `limit` | int | 50 | Max records to return (1-100) |

**Response** `200`
```json
{
  "items": [
    {
      "id": "019d52d7-37d4-7882-93c8-9a3e24723ec0",
      "name": "Project Alpha",
      "description": "Initial project setup",
      "status": "completed",
      "created_at": "2025-01-01T00:00:00Z",
      "updated_at": "2025-01-01T00:00:03Z"
    }
  ],
  "total": 1
}
```

### `POST /api/v1/records`

Create a new record. Automatically enqueues a background job for processing.

**Request Body**
```json
{
  "name": "My Record",
  "description": "Optional description",
  "status": "pending"
}
```

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `name` | string | yes | 1-255 characters |
| `description` | string | no | max 5000 characters |
| `status` | string | no | max 50 characters, defaults to `"pending"` |

**Response** `201`
```json
{
  "item": {
    "id": "019d52d7-37d4-7882-93c8-9a3e24723ec0",
    "name": "My Record",
    "description": "Optional description",
    "status": "pending",
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-01T00:00:00Z"
  }
}
```

### `GET /api/v1/records/{id}`

Get a single record by ID.

**Response** `200`
```json
{
  "item": { ... }
}
```

**Response** `404`
```json
{
  "detail": "Record not found"
}
```

### `PATCH /api/v1/records/{id}`

Update a record. Only provided fields are updated.

**Request Body** (all fields optional)
```json
{
  "name": "Updated Name",
  "status": "completed"
}
```

**Response** `200`
```json
{
  "item": { ... }
}
```

### `DELETE /api/v1/records/{id}`

Delete a record.

**Response** `204` No Content

**Response** `404`
```json
{
  "detail": "Record not found"
}
```

## Response Formats

### List responses
```json
{
  "items": [],
  "total": 0
}
```

### Single item responses
```json
{
  "item": {}
}
```

### Validation errors `422`
```json
{
  "detail": [
    {
      "loc": ["body", "name"],
      "msg": "String should have at least 1 character",
      "type": "string_too_short"
    }
  ]
}
```

## Data Model

### Record

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID (v7) | Auto-generated, sortable |
| `name` | string (1-255) | Record name |
| `description` | text (nullable) | Optional description |
| `status` | string (max 50) | Lifecycle status |
| `created_at` | datetime (UTC) | Auto-set on creation |
| `updated_at` | datetime (UTC) | Auto-updated on changes |

### Status Lifecycle

```
pending → processing → completed
```

- `pending` — set on creation
- `processing` — set by worker when job starts
- `completed` — set by worker when job finishes
