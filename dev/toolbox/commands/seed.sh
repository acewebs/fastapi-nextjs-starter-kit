#!/bin/bash

case "$1" in
    seed)
        info "Creating sample records..."
        echo ""

        names=("Project Alpha" "Database Migration" "API Integration" "Frontend Redesign" "Performance Audit")
        descriptions=(
            "Initial project setup and configuration"
            "Migrate legacy data to new schema"
            "Connect to third-party payment API"
            "Redesign dashboard with new components"
            "Profile and optimize slow queries"
        )

        for i in "${!names[@]}"; do
            response=$(curl -sf -X POST http://localhost:8000/api/v1/records \
                -H "Content-Type: application/json" \
                -d "{\"name\": \"${names[$i]}\", \"description\": \"${descriptions[$i]}\"}" 2>/dev/null)

            if [ $? -eq 0 ]; then
                success "Created: ${names[$i]}"
            else
                error "Failed:  ${names[$i]}"
            fi
        done

        echo ""
        success "Seeding complete — check http://localhost:3000/records"
        exit 0
        ;;
esac
