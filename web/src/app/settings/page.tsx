"use client";

import { useCallback, useEffect, useState } from "react";
import { api } from "@/lib/api";
import type { AppInfo } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export default function SettingsPage() {
  const [appInfo, setAppInfo] = useState<AppInfo | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchInfo = useCallback(async () => {
    setLoading(true);
    try {
      const data = await api.appInfo();
      setAppInfo(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch app info");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchInfo();
  }, [fetchInfo]);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Settings</h1>
        <p className="text-muted-foreground mt-2">
          Application configuration and environment info.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Application Info</CardTitle>
        </CardHeader>
        <CardContent>
          {loading ? (
            <p className="text-sm text-muted-foreground">Loading...</p>
          ) : error ? (
            <p className="text-sm text-destructive">{error}</p>
          ) : appInfo ? (
            <dl className="space-y-3">
              <div className="flex items-center justify-between">
                <dt className="text-sm font-medium">Name</dt>
                <dd className="text-sm text-muted-foreground">{appInfo.name}</dd>
              </div>
              <div className="flex items-center justify-between">
                <dt className="text-sm font-medium">Environment</dt>
                <dd>
                  <Badge variant={appInfo.env === "production" ? "default" : "secondary"}>
                    {appInfo.env}
                  </Badge>
                </dd>
              </div>
              <div className="flex items-center justify-between">
                <dt className="text-sm font-medium">Version</dt>
                <dd className="text-sm text-muted-foreground">{appInfo.version}</dd>
              </div>
            </dl>
          ) : null}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Frontend Config</CardTitle>
        </CardHeader>
        <CardContent>
          <dl className="space-y-3">
            <div className="flex items-center justify-between">
              <dt className="text-sm font-medium">API Base URL</dt>
              <dd className="text-sm text-muted-foreground font-mono">
                {process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000"}
              </dd>
            </div>
          </dl>
        </CardContent>
      </Card>
    </div>
  );
}
