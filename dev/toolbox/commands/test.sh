#!/bin/bash

case "$1" in
    test)
        shift
        info "Running API tests..."
        run_in_service api pytest tests/ -v "$@"
        exit 0
        ;;
    test:api)
        shift
        info "Running API tests..."
        run_in_service api pytest tests/ -v "$@"
        exit 0
        ;;
esac
