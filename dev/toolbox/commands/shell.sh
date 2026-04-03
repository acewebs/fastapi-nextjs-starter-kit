#!/bin/bash

case "$1" in
    shell:api)
        info "Opening shell in API container..."
        run_in_service api bash
        exit 0
        ;;
    shell:worker)
        info "Opening shell in worker container..."
        run_in_service worker bash
        exit 0
        ;;
    shell:web)
        info "Opening shell in web container..."
        run_in_service web sh
        exit 0
        ;;
    shell:db)
        info "Opening psql shell..."
        run_in_service db psql -U app -d app
        exit 0
        ;;
esac
