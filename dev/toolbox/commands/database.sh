#!/bin/bash

case "$1" in
    migrate)
        info "Running migrations..."
        run_in_service api alembic upgrade head
        success "Migrations complete"
        exit 0
        ;;
    migrate:status)
        info "Current migration revision:"
        run_in_service api alembic current
        exit 0
        ;;
    migrate:history)
        info "Migration history:"
        run_in_service api alembic history
        exit 0
        ;;
esac
