# Makefile for common development tasks

.PHONY: help setup build up down logs clean deploy test

# Default target
help:
	@echo "Available commands:"
	@echo "  make setup       - Initialize project configuration"
	@echo "  make build       - Build Docker images"
	@echo "  make up          - Start services with docker-compose"
	@echo "  make down        - Stop services"
	@echo "  make logs        - View service logs"
	@echo "  make shell       - Open shell in container"
	@echo "  make clean       - Clean up containers and images"
	@echo "  make deploy      - Deploy to Cloud Run"
	@echo "  make test        - Run tests (customize for your project)"
	@echo "  make lint        - Run linters (customize for your project)"

# Initialize project
setup:
	@chmod +x setup.sh
	@./setup.sh

# Build Docker images
build:
	docker-compose build

# Start services
up:
	docker-compose up

# Start services in background
up-d:
	docker-compose up -d

# Stop services
down:
	docker-compose down

# View logs
logs:
	docker-compose logs -f

# Open shell in API container
shell:
	docker-compose exec api /bin/sh

# Clean up Docker resources
clean:
	docker-compose down -v
	docker system prune -f

# Clean everything including images
clean-all:
	docker-compose down -v --rmi all
	docker system prune -af

# Deploy to Cloud Run
deploy:
	@chmod +x deploy.sh
	@./deploy.sh

# Run tests (customize based on your tech stack)
test:
	@echo "Add your test commands here"
	# docker-compose run --rm api npm test
	# docker-compose run --rm api pytest
	# docker-compose run --rm api go test ./...

# Run linters (customize based on your tech stack)
lint:
	@echo "Add your linting commands here"
	# docker-compose run --rm api npm run lint
	# docker-compose run --rm api flake8
	# docker-compose run --rm api golangci-lint run

# Format code (customize based on your tech stack)
format:
	@echo "Add your formatting commands here"
	# docker-compose run --rm api npm run format
	# docker-compose run --rm api black .
	# docker-compose run --rm api gofmt -w .

# Install dependencies locally (customize based on your tech stack)
install:
	@echo "Add your dependency installation commands here"
	# npm install
	# pip install -r requirements.txt
	# go mod download

# Database migrations (if applicable)
migrate:
	@echo "Add your migration commands here"
	# docker-compose exec api npm run migrate
	# docker-compose exec api alembic upgrade head

# Check environment configuration
check-env:
	@echo "Checking environment configuration..."
	@test -f .env || (echo "❌ .env file not found. Run 'make setup' first" && exit 1)
	@test -f project.config.json || (echo "❌ project.config.json not found" && exit 1)
	@echo "✅ Configuration files found"

# Development mode with hot reload (customize for your project)
dev:
	@echo "Starting development mode with hot reload..."
	docker-compose up --build
	# Add volume mounts in docker-compose.yml for hot reload

# Production build test
prod-build:
	docker build --platform linux/amd64 -t test-build .
	@echo "✅ Production build successful"

# Health check
health:
	@curl -f http://localhost:8080/health || echo "❌ Health check failed"

# Show project info
info:
	@echo "Project Configuration:"
	@cat project.config.json | grep -E '"name"|"displayName"|"port"' || echo "Config not found"
