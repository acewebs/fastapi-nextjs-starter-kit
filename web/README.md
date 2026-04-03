# Web Service (Next.js)

Frontend application for the starter template.

## What it does

- Renders the UI using React Server Components + App Router
- Provides CRUD interface for managing Records
- Displays API health status and app configuration
- Communicates with the API service via REST

## Pages

| Path | Description |
|------|-------------|
| `/` | Welcome / dashboard page |
| `/records` | CRUD table for records |
| `/status` | API health check |
| `/settings` | App info and config display |

## How it connects

- **Browser requests**: `/api/*` routes are proxied server-side to the API via `BACKEND_URL`
- **Server-side requests**: Next.js calls the API directly via `BACKEND_URL`

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `BACKEND_URL` | `http://localhost:8000` | API URL (used by the proxy and server-side requests) |

## Local Development

```bash
cp .env.example .env.local
npm install
npm run dev
```

Or use docker-compose from the root directory.

## How to Extend

- Add new pages in `src/app/`
- Add new components in `src/components/`
- Add shadcn/ui components: `npx shadcn@latest add <component>`
- Update the API client in `src/lib/api.ts`
