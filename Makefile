.PHONY: prod-up prod-down prod-logs

# Start production environment
prod-up:
    docker-compose -f docker-compose.prod.yml up -d

# Stop production environment
prod-down:
    docker-compose -f docker-compose.prod.yml down

# View logs
prod-logs:
    docker-compose -f docker-compose.prod.yml logs -f