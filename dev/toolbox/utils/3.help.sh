#!/bin/bash

HELP_TEXT="
${BLUE}FastAPI + Next.js Starter Kit — Dev Toolbox${NC}

Usage: ./dev/toolbox/run <command> [args]

${GREEN}Docker${NC}
  up                 Start all services
  down               Stop and remove all services
  stop               Stop services (keep containers)
  start              Start stopped services
  restart            Restart all services
  rebuild [service]  Rebuild containers (no cache)
  logs [service]     Tail logs (default: all)
  ps                 Show running containers

${GREEN}Shell${NC}
  shell:api          Open bash in API container
  shell:worker       Open bash in worker container
  shell:web          Open sh in web container
  shell:db           Open psql shell

${GREEN}Database${NC}
  migrate            Run alembic migrations (upgrade head)
  migrate:status     Show current migration revision
  migrate:history    Show migration history

${GREEN}Health & Status${NC}
  health             Check health of all services
  status             Show service ports and URLs

${GREEN}Linting & Formatting${NC}
  lint               Run all linters (ruff, mypy, eslint, tsc)
  lint:api           Lint API only
  lint:worker        Lint worker only
  lint:web           Lint web only
  format             Auto-format all Python code

${GREEN}Testing${NC}
  test               Run API tests
  test:api           Run API tests (alias)

${GREEN}Utilities${NC}
  seed               Create sample records via API
  help               Show this help message
"
