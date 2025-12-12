.PHONY: help build run stop logs clean test

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build Docker image
	docker build -t dmcompverify-api .

run: ## Run Docker container
	docker-compose up -d

stop: ## Stop Docker container
	docker-compose down

logs: ## View Docker logs
	docker-compose logs -f

clean: ## Remove Docker images and containers
	docker-compose down -v
	docker rmi dmcompverify-api || true

test: ## Test the API
	curl http://localhost:8000/health

install: ## Install dependencies locally
	pip install -r requirements.txt

dev: ## Run in development mode
	python main.py --host 0.0.0.0 --port 8000

