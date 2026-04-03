#!/bin/bash

run_web_cmd() {
    (cd "$project_dir/web" && "$@")
}

case "$1" in
    lint|lint:all)
        info "Linting all services..."
        echo ""

        step "API — ruff check"
        run_in_service api ruff check app/ tests/
        step "API — ruff format check"
        run_in_service api ruff format --check app/ tests/
        step "API — mypy"
        run_in_service api mypy app/ --ignore-missing-imports
        echo ""

        step "Worker — ruff check"
        run_in_service worker ruff check app/
        step "Worker — ruff format check"
        run_in_service worker ruff format --check app/
        step "Worker — mypy"
        run_in_service worker mypy app/ --ignore-missing-imports
        echo ""

        step "Web — eslint"
        run_web_cmd npx eslint src/
        step "Web — typecheck"
        run_web_cmd npx tsc --noEmit
        echo ""

        success "All lint checks passed"
        exit 0
        ;;
    lint:api)
        info "Linting API..."
        run_in_service api ruff check app/ tests/
        run_in_service api ruff format --check app/ tests/
        run_in_service api mypy app/ --ignore-missing-imports
        success "API lint passed"
        exit 0
        ;;
    lint:worker)
        info "Linting Worker..."
        run_in_service worker ruff check app/
        run_in_service worker ruff format --check app/
        run_in_service worker mypy app/ --ignore-missing-imports
        success "Worker lint passed"
        exit 0
        ;;
    lint:web)
        info "Linting Web..."
        run_web_cmd npx eslint src/
        run_web_cmd npx tsc --noEmit
        success "Web lint passed"
        exit 0
        ;;
    format)
        info "Formatting all Python code..."
        run_in_service api ruff format app/ tests/
        run_in_service api ruff check --fix app/ tests/
        run_in_service worker ruff format app/
        run_in_service worker ruff check --fix app/
        success "Formatting complete"
        exit 0
        ;;
esac
