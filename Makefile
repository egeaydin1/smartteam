.PHONY: up down build logs restart clean

## Start all services (build if needed)
up:
	docker compose up --build

## Start in detached mode
up-d:
	docker compose up --build -d

## Stop all services
down:
	docker compose down

## Stop and remove volumes (wipes the database)
down-v:
	docker compose down -v

## Rebuild images without cache
build:
	docker compose build --no-cache

## Follow logs for all services
logs:
	docker compose logs -f

## Follow logs for a specific service: make logs-api | make logs-frontend
logs-api:
	docker compose logs -f api

logs-frontend:
	docker compose logs -f frontend

logs-db:
	docker compose logs -f db

## Restart a service: make restart s=api
restart:
	docker compose restart $(s)

## Open a shell in a running container: make sh s=api
sh:
	docker compose exec $(s) sh

## Run backend tests inside the api container
test:
	docker compose exec api pytest --tb=short -q

## Remove all stopped containers, dangling images, and build cache
clean:
	docker system prune -f
