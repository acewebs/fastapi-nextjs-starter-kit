#!/bin/bash

case "$1" in
    health)
        echo ""
        step "Checking API..."
        api_response=$(curl -sf http://localhost:8000/health 2>/dev/null)
        if [ $? -eq 0 ]; then
            success "API:    healthy — $api_response"
        else
            error "API:    unreachable"
        fi

        step "Checking Web..."
        web_response=$(curl -sf -o /dev/null -w "%{http_code}" http://localhost:3000 2>/dev/null)
        if [ "$web_response" = "200" ]; then
            success "Web:    healthy (HTTP $web_response)"
        else
            error "Web:    unreachable"
        fi

        step "Checking Postgres..."
        dk-c exec -T db pg_isready -U app > /dev/null 2>&1
        if [ $? -eq 0 ]; then
            success "DB:     healthy"
        else
            error "DB:     unreachable"
        fi

        step "Checking Redis..."
        dk-c exec -T redis redis-cli ping > /dev/null 2>&1
        if [ $? -eq 0 ]; then
            success "Redis:  healthy"
        else
            error "Redis:  unreachable"
        fi

        step "Checking Worker..."
        worker_running=$(dk-c ps --status running worker 2>/dev/null | grep -c worker)
        if [ "$worker_running" -gt 0 ]; then
            success "Worker: running"
        else
            error "Worker: not running"
        fi

        echo ""
        exit 0
        ;;
    status)
        echo ""
        info "Service URLs:"
        echo "  Web:      http://localhost:3000"
        echo "  API:      http://localhost:8000"
        echo "  API Docs: http://localhost:8000/docs"
        echo "  Postgres: localhost:5432"
        echo "  Redis:    localhost:6379"
        echo ""
        dk-c ps
        exit 0
        ;;
esac
