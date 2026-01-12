.PHONY: help build up down logs clean dev-up dev-down ps restart

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build all Docker images
	docker compose build

up: ## Start all services
	docker compose up -d

down: ## Stop all services
	docker compose down

logs: ## Show logs from all services
	docker compose logs -f

clean: ## Stop and remove all containers, networks, and volumes
	docker compose down -v

dev-up: ## Start only infrastructure services (PostgreSQL, Redis, RabbitMQ)
	docker compose -f docker-compose.dev.yml up -d

dev-down: ## Stop infrastructure services
	docker compose -f docker-compose.dev.yml down

ps: ## Show status of all services
	docker compose ps

restart: ## Restart all services
	docker compose restart

rebuild: ## Rebuild and restart all services
	docker compose up -d --build

test-api: ## Test API Gateway health
	@curl -s http://localhost:8080/ | jq .

test-storage: ## Test Storage Service health
	@curl -s http://localhost:5000/articles | jq . | head -20
