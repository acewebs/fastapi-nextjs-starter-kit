"use client";

import { useCallback, useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

export default function StatusPage() {
  const [health, setHealth] = useState<{ status: string } | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const checkHealth = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.health();
      setHealth(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to reach API");
      setHealth(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    checkHealth();
  }, [checkHealth]);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Status</h1>
        <p className="text-muted-foreground mt-2">
          Check the health of connected services.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            API Service
            {loading ? (
              <Badge variant="secondary">Checking...</Badge>
            ) : health?.status === "ok" ? (
              <Badge variant="default">Healthy</Badge>
            ) : (
              <Badge variant="destructive">Unreachable</Badge>
            )}
          </CardTitle>
        </CardHeader>
        <CardContent>
          {error ? (
            <p className="text-sm text-destructive">{error}</p>
          ) : health ? (
            <p className="text-sm text-muted-foreground">
              API is responding normally.
            </p>
          ) : (
            <p className="text-sm text-muted-foreground">Checking connection...</p>
          )}
          <Button variant="outline" size="sm" className="mt-4" onClick={checkHealth}>
            Refresh
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
