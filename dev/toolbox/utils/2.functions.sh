#!/bin/bash

dk-c() {
  docker compose -f "$project_dir/docker-compose.yml" "$@"
}

ensure_env() {
  if [ -f "$project_dir/.env" ]; then
    set -a
    source "$project_dir/.env"
    set +a
  fi
}

run_in_service() {
  local service="$1"
  shift
  docker compose -f "$project_dir/docker-compose.yml" exec "$service" "$@"
}

wait_for_healthy() {
  local service="$1"
  local url="$2"
  local max_attempts="${3:-30}"
  local attempt=0

  while [ $attempt -lt $max_attempts ]; do
    if curl -sf "$url" > /dev/null 2>&1; then
      return 0
    fi
    attempt=$((attempt + 1))
    sleep 1
  done
  return 1
}
