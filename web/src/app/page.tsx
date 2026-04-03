import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export default function HomePage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Welcome</h1>
        <p className="text-muted-foreground mt-2">
          A production-ready starter template with FastAPI, Next.js, and background workers.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle>API Service</CardTitle>
            <CardDescription>FastAPI backend</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              REST API with CRUD endpoints, PostgreSQL database, and Redis integration.
              Async SQLAlchemy with Alembic migrations.
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Web Service</CardTitle>
            <CardDescription>Next.js frontend</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              Server-rendered React app with App Router, TypeScript, Tailwind CSS,
              and shadcn/ui components.
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Worker Service</CardTitle>
            <CardDescription>ARQ background jobs</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              Async background job processor using ARQ and Redis.
              Processes records and runs async workflows.
            </p>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Getting Started</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3 text-sm text-muted-foreground">
          <p>
            <strong>Records</strong> — Go to the Records page to create, view, update, and delete records.
            New records are automatically enqueued for background processing.
          </p>
          <p>
            <strong>Status</strong> — Check the health of the API service and verify all connections are working.
          </p>
          <p>
            <strong>Settings</strong> — View application configuration and environment details.
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
