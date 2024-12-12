.PHONY: help install test test-cov test-parallel clean lint format test-build

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	poetry install

test-build:
	docker-compose build

test: test-build
	docker-compose up --abort-on-container-exit --exit-code-from tests

test-cov:  ## Run tests with coverage report
	poetry run pytest --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"

test-parallel:  ## Run tests in parallel
	poetry run pytest -n auto

test-watch:  ## Run tests in watch mode
	poetry run pytest-watch

clean:  ## Clean cache files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

lint:  ## Run linting
	poetry run mypy ai_toolkit
	poetry run flake8 ai_toolkit tests
	poetry run black --check ai_toolkit tests

format:  ## Format code
	poetry run black utils tests

# Add linting dependencies to pyproject.toml
setup-dev:  ## Setup development environment
	poetry add --group dev black flake8 mypy pytest-watch 