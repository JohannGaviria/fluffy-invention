PYTHON=python3
PIP=pip

EXCLUDE=.venv venv
EXCLUDE_REGEX=$(shell echo $(EXCLUDE) | sed 's/ /|/g')
EXCLUDE_COMMA=$(shell echo $(EXCLUDE) | sed 's/ /,/g')

# Colors for output
GREEN=\033[0;32m
BLUE=\033[0;34m
YELLOW=\033[1;33m
RED=\033[0;31m
NC=\033[0m # No Color

.PHONY: help setup format lint test pre-commit install up down check

help: ## Show this help message
	@echo "$(YELLOW)=== Available Commands ===$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-16s$(NC) %s\n", $$1, $$2}"

setup: ## Install development dependencies and git hooks
	$(PIP) install -r requirements.txt
	pre-commit install

up: ## Start docker containers with build
	docker compose up --build

down: ## Stop docker containers
	docker compose down

test: ## Run tests with pytest
	@echo "$(BLUE)Running tests...$(NC)"
	pytest -q

format: ## Format code (Ruff formatter)
	@echo "$(BLUE)Formatting code...$(NC)"
	ruff format .
	@echo "$(BLUE)Fixing auto-fixable lint issues...$(NC)"
	ruff check --fix .

lint: ## Lint code with Ruff and type-check with mypy
	@echo "$(BLUE)Running Ruff lint...$(NC)"
	ruff check .
	@echo "$(BLUE)Running mypy...$(NC)"
	mypy --explicit-package-bases app/

pre-commit: ## Run all pre-commit hooks on all files
	@pre-commit run --all-files

check: ## Check code formatting and linting without making changes
	@echo "$(BLUE)Checking formatting...$(NC)"
	ruff format --check .
	@echo "$(BLUE)Checking lint...$(NC)"
	ruff check .
	@echo "$(BLUE)Checking types...$(NC)"
	mypy --explicit-package-bases app/
