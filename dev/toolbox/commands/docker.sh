#!/bin/bash

case "$1" in
    up)
        info "Starting all services..."
        dk-c up -d --build
        echo ""
        success "Services are starting up"
        echo ""
        info "Web:      http://localhost:3000"
        info "API:      http://localhost:8000"
        info "API Docs: http://localhost:8000/docs"
        exit 0
        ;;
    down)
        info "Stopping all services..."
        dk-c down --remove-orphans
        success "All services stopped"
        exit 0
        ;;
    stop)
        dk-c stop
        exit 0
        ;;
    start)
        dk-c start
        exit 0
        ;;
    restart)
        info "Restarting services..."
        dk-c restart
        success "Services restarted"
        exit 0
        ;;
    rebuild)
        service="${2:-}"
        if [ -n "$service" ]; then
            info "Rebuilding $service..."
            dk-c build --no-cache "$service"
            dk-c up -d "$service"
        else
            info "Rebuilding all services..."
            dk-c down --remove-orphans
            dk-c build --no-cache
            dk-c up -d
        fi
        success "Rebuild complete"
        exit 0
        ;;
    logs)
        service="${2:-}"
        if [ -n "$service" ]; then
            dk-c logs -f "$service"
        else
            dk-c logs -f
        fi
        exit 0
        ;;
    ps)
        dk-c ps
        exit 0
        ;;
esac
